import os
import io
import base64
import json
import logging
import urllib.parse
import xml.etree.ElementTree as ET
from typing import Optional, List
from functools import lru_cache
from urllib.parse import urljoin

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PIL import Image

import requests
from bs4 import BeautifulSoup
import pypdf

import google.generativeai as genai
from groq import Groq
from openai import OpenAI

from examdz_data import EXAMDZ_SECONDARY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("OustadDz")

# إعداد المفاتيح
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

genai.configure(api_key=GEMINI_API_KEY)
groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
openrouter_client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=OPENROUTER_API_KEY) if OPENROUTER_API_KEY else None

# =========================================================
# نظام التعلم الذاتي (Knowledge Cache)
# =========================================================
KB_FILE = "knowledge_cache.json"

def load_knowledge():
    if os.path.exists(KB_FILE):
        try:
            with open(KB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except: return {}
    return {}

def save_knowledge(data):
    try:
        with open(KB_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
    except Exception as e:
        logger.warning(f"Failed to save knowledge: {e}")

def _get_or_create_summary(url: str, raw_text: str) -> str:
    kb = load_knowledge()
    if url in kb:
        logger.info(f"Found cached knowledge for {url}")
        return kb[url]
    
    if not raw_text: return ""
    
    logger.info(f"Creating new summary for {url}...")
    try:
        # نستخدم Groq لتلخيص سريع (لأنه سريع جداً ورخيص)
        if groq_client:
            sum_prompt = f"أنت خبير تربوي جزائري. لخص هذا الدرس في نقاط واضحة ومفيدة للطلاب (بدون نسخ النص الأصلي، بل استخرج الزبدة):\n{raw_text[:5000]}"
            res = groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": sum_prompt}],
                temperature=0.3, max_tokens=800
            )
            summary = res.choices[0].message.content
        else:
            summary = raw_text[:2000] # احتياطي
            
        kb[url] = summary
        save_knowledge(kb)
        return summary
    except Exception as e:
        logger.warning(f"Summarization failed: {e}")
        return raw_text[:2000]

def _fetch_web_content(url: str) -> str:
    if not url: return ""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # البحث عن أول ملف PDF
        pdf_link = None
        for a_tag in soup.find_all('a', href=True):
            if a_tag['href'].endswith('.pdf'):
                pdf_link = urljoin(url, a_tag['href'])
                break
        
        if pdf_link:
            try:
                pdf_res = requests.get(pdf_link, headers=headers, timeout=15)
                pdf_file = io.BytesIO(pdf_res.content)
                reader = pypdf.PdfReader(pdf_file)
                extracted = "".join([p.extract_text() for p in reader.pages[:5] if p.extract_text()])
                if extracted.strip(): return extracted
            except: pass
            
        # إذا لم يجد PDF، يقرأ نصوص الصفحة
        for script in soup(["script", "style"]): script.decompose()
        return soup.get_text(separator=' ', strip=True)[:4000]
    except Exception: return ""

def _get_latest_news(query: str = None) -> str:
    try:
        if query: url = f"https://news.google.com/rss/search?q={urllib.parse.quote(query)}&hl=ar&gl=DZ&ceid=DZ:ar"
        else: url = "https://news.google.com/rss?hl=ar&gl=DZ&ceid=DZ:ar"
        res = requests.get(url, timeout=5)
        root = ET.fromstring(res.content)
        items = root.findall('.//item')[:3]
        return "\n".join([f"- {i.find('title').text}" for i in items]) if items else "لا توجد أخبار."
    except Exception: return "تعذر جلب الأخبار."

# =========================================================
# الرادار الذكي (تحليل الطلب)
# =========================================================
def _extract_requested_data(msg: str):
    msg = msg.lower()
    year, stream, subject = None, None, None
    if any(w in msg for w in ["أولى", "اولى", "1as", "1 as"]): year = "1AS"
    elif any(w in msg for w in ["ثانية", "2as", "2 as"]): year = "2AS"
    elif any(w in msg for w in ["ثالثة", "ثالثه", "3as", "3 as"]): year = "3AS"

    if year == "1AS":
        if any(w in msg for w in ["علوم", "science"]): stream = "sciences"
        elif any(w in msg for w in ["آداب", "اداب", "lettres"]): stream = "lettres"
    elif year in ["2AS", "3AS"]:
        if any(w in msg for w in ["علوم", "تجريبية", "science"]): stream = "sciences"
        elif any(w in msg for w in ["رياضيات", "math"]): stream = "math"
        elif any(w in msg for w in ["تقني", "tech"]): stream = "tech"
        elif any(w in msg for w in ["تسيير", "gestion"]): stream = "gestion"
        elif any(w in msg for w in ["آداب", "اداب", "فلسفة", "lettres"]): stream = "lettres"
        elif any(w in msg for w in ["لغات", "langues"]): stream = "langues"

    if any(w in msg for w in ["رياضيات", "math"]): subject = "math"
    elif any(w in msg for w in ["فيزياء", "physique"]): subject = "physics"
    elif any(w in msg for w in ["علوم طبيعية", "svt"]): subject = "sciences"
    elif any(w in msg for w in ["عربية", "arabic"]): subject = "arabic"
    elif any(w in msg for w in ["فرنسية", "french"]): subject = "french"
    elif any(w in msg for w in ["انجليزية", "english"]): subject = "english"
    elif any(w in msg for w in ["فلسفة", "philo"]): subject = "philosophy"
    elif any(w in msg for w in ["تاريخ", "history"]): subject = "history"
    elif any(w in msg for w in ["اسلامية", "islamic"]): subject = "islamic"
    elif any(w in msg for w in ["اعلام", "informatique"]): subject = "informatics"
    elif any(w in msg for w in ["اقتصاد", "eco"]): subject = "eco"
    elif any(w in msg for w in ["قانون", "law"]): subject = "law"

    return year, stream, subject

# =========================================================
# بناء البرومبت
# =========================================================
def _build_smart_prompt(message: str) -> str:
    base_rules = """أنت "OustadDz" (أستاذ Dz)، مرافق التعليم الثانوي الجزائري.
⚠️ لا تذكر من صممك إلا إذا سُئلت صراحةً: "تم تطويري بواسطة Qimah Production بإشراف الباحث مانة رضوان".
تتصرف كذكاء عام للدردشة.
"""
    msg_lower = message.lower()
    is_greeting = any(w in msg_lower for w in ["مرحبا", "أهلا", "سلام", "hello", "hi", "bonjour"])
    is_news = any(w in msg_lower for w in ["أخبار", "خبر", "اليوم", "news"])
    is_edu = any(w in msg_lower for w in ["درس", "شرح", "تمرين", "حل", "رياضيات", "فيزياء", "علوم", "فلسفة", "لغة", "تاريخ", "math", "physique", "1as", "2as", "3as", "أولى", "ثانية", "ثالثة", "فروض", "اختبارات", "كتاب"])

    context = ""
    if is_news: context += f"\n[أخبار اليوم]:\n{_get_latest_news()}\n"
    
    if is_edu:
        year, stream, subject = _extract_requested_data(msg_lower)
        if year and stream and subject:
            url = ""
            if year in EXAMDZ_SECONDARY and stream in EXAMDZ_SECONDARY[year]:
                url = EXAMDZ_SECONDARY[year][stream].get(subject, "")
            
            if url:
                # نبحث في الذاكرة أولاً
                kb = load_knowledge()
                if url in kb:
                    context += f"\n[من ذاكرة الأستاذ - ملخص الدرس المحفوظ]:\n{kb[url]}\n"
                    context += "\nتنبيه: لقد قرأت هذا الدرس سابقاً وحفظت ملخصه. اشرحه للطالب بأسلوبك الآن بناءً على هذا الملخص."
                else:
                    # أول مرة: نجلب ونلخص ونحفظ
                    raw_text = _fetch_web_content(url)
                    summary = _get_or_create_summary(url, raw_text)
                    context += f"\n[محتوى الدرس (تمت قراءته للتو وحفظه)]:\n{summary}\n"
                    context += "\nتنبيه: اشرح هذا الدرس للطالب بأسلوبك التربوي، ولا تنسخ النص."
            else:
                context += "\n[تنبيه]: هذا الرابط غير متوفر. اعتذر بلطف."
        elif year and stream:
            context += "\n[تنبيه]: المستخدم حدد السنة والشعبة، لكنه لم يحدد المادة. اسأله عنها."
        else:
            context += "\n[تنبيه]: لم يحدد (السنة والشعبة). اسأله عنها أولاً بذكاء."

    if is_greeting and not is_edu and not is_news:
         return base_rules + "\nالمستخدم يلقي التحية. رد بترحيب قصير واسأله كيف يمكنك مساعدته."
    return base_rules + context

# =========================================================
# الخادم (FastAPI)
# =========================================================
class ChatMessage(BaseModel):
    role: str
    content: str
class ChatRequest(BaseModel):
    message: str
    image_base64: Optional[str] = None
    history: Optional[List[ChatMessage]] = None
class ChatResponse(BaseModel):
    reply: str

app = FastAPI(title="OustadDz API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=False, allow_methods=["*"], allow_headers=["*"])

def _decode_image(b64: str) -> Image.Image:
    if "," in b64: b64 = b64.split(",", 1)[1]
    return Image.open(io.BytesIO(base64.b64decode(b64))).convert("RGB")

def _call_groq(messages) -> str:
    res = groq_client.chat.completions.create(model="llama-3.1-8b-instant", messages=messages, temperature=0.3, max_tokens=1024)
    return (res.choices[0].message.content or "").strip()

def _call_gemini(contents, final_prompt) -> str:
    model = genai.GenerativeModel(model_name="gemini-1.5-flash", system_instruction=final_prompt)
    res = model.generate_content(contents)
    return (res.text or "").strip()

def _call_openrouter(messages) -> str:
    res = openrouter_client.chat.completions.create(model="openai/gpt-4o-mini", messages=messages, temperature=0.3, max_tokens=1024)
    return (res.choices[0].message.content or "").strip()

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    if not req.message and not req.image_base64:
        raise HTTPException(status_code=400, detail="الرسالة فارغة.")

    final_prompt = _build_smart_prompt(req.message)
    messages = [{"role": "system", "content": final_prompt}]
    
    if req.history:
        for msg in req.history[-2:]: messages.append({"role": msg.role, "content": msg.content})
    
    if req.image_base64:
        messages.append({"role": "user", "content": [{"type": "text", "text": req.message}, {"type": "image_url", "image_url": {"url": req.image_base64}}]})
    else:
        messages.append({"role": "user", "content": req.message})

    if OPENROUTER_API_KEY:
        try: return ChatResponse(reply=_call_openrouter(messages))
        except Exception as e: logger.warning(f"OpenRouter failed: {e}")
    
    if GROQ_API_KEY:
        try: return ChatResponse(reply=_call_groq(messages))
        except Exception as e: logger.warning(f"Groq failed: {e}")
        
    if GEMINI_API_KEY:
        try: 
            contents = []
            for m in messages[1:]:
                if isinstance(m["content"], str): contents.append({"role": "user", "parts": [m["content"]]})
                else: 
                    parts = [{"text": p["text"]} if p["type"]=="text" else _decode_image(p["image_url"]["url"]) for p in m["content"]]
                    contents.append({"role": "user", "parts": parts})
            return ChatResponse(reply=_call_gemini(contents, final_prompt))
        except Exception as e: logger.error(f"Gemini failed: {e}")

    raise HTTPException(status_code=502, detail="عذراً، الحصة المجانية استنفدت لهذا اليوم. يرجى المحاولة غداً.")

@app.get("/")
def root(): return {"app": "OustadDz", "status": "running"}
@app.get("/health")
def health(): return {"status": "ok"}
@app.head("/health")
async def health_head(): return {}
