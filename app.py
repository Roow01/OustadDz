import os
import io
import base64
import json
import logging
import urllib.parse
import xml.etree.ElementTree as ET
from typing import Optional, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PIL import Image

import requests
from bs4 import BeautifulSoup

import google.generativeai as genai
from groq import Groq
from openai import OpenAI

# استدعاء الملفات المستقلة
from curriculum_data import CURRICULUM_DATA
from examdz_data import EXAMDZ_SECONDARY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("OustadDz")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

genai.configure(api_key=GEMINI_API_KEY)
groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
openrouter_client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=OPENROUTER_API_KEY) if OPENROUTER_API_KEY else None

# ضغط البيانات
curriculum_text = json.dumps(CURRICULUM_DATA, ensure_ascii=False, separators=(',', ':'))
examdz_text = json.dumps(EXAMDZ_SECONDARY, ensure_ascii=False, separators=(',', ':'))

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
# نظام التوجيه الذكي (Smart Routing)
# =========================================================
def _build_smart_prompt(message: str) -> str:
    base_rules = """أنت "OustadDz"، مرافق التعليم الثانوي. 
تتصرف كذكاء عام للدردشة، وكأستاذ خبير للمناهج.
- إذا كان السؤال عاماً، أجب بذكاء.
- إذا كان السؤال دراسياً، ويخلو من (السنة والشعبة)، اطلبها بذكاء.
"""
    msg_lower = message.lower()
    
    # كشف النية
    is_greeting = any(w in msg_lower for w in ["مرحبا", "أهلا", "سلام", "hello", "hi", "bonjour", "كيف حالك", "شكرا"])
    is_news = any(w in msg_lower for w in ["أخبار", "خبر", "اليوم", "news", "actualité"])
    is_link = any(w in msg_lower for w in ["رابط", "روابط", "فروض", "كتب", "pdf", "link", "بكالوريا"])
    is_edu = any(w in msg_lower for w in ["درس", "شرح", "تمرين", "حل", "رياضيات", "فيزياء", "علوم", "فلسفة", "لغة", "تاريخ", "math", "physique", "svt", "philo", "1as", "2as", "3as", "أولى", "ثانية", "ثالثة", "علوم تجريبية", "آداب", "تقني", "تسيير", "لغات"])

    context = ""
    
    if is_news: context += f"\n[أخبار اليوم]:\n{_get_latest_news()}\n"
    if is_link: context += f"\n[دليل الروابط DzExams]:\n{examdz_text}\n"
    if is_edu: 
        context += f"\n[المنهاج الدراسي]:\n{curriculum_text}\n"
        context += "\nتنبيه: إذا لم يحدد المستخدم (السنة والشعبة)، اسأله عنها أولاً.\n"

    if is_greeting and not is_edu and not is_news:
         return base_rules + "\nالمستخدم يلقي التحية. رد عليه بترحيب قصير جداً واسأله كيف يمكنك مساعدته (بدون إرسال أي منهاج)."

    return base_rules + context

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
        for msg in req.history[-2:]:
            messages.append({"role": msg.role, "content": msg.content})
    
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

    raise HTTPException(status_code=502, detail="عذراً، الحصة المجانية للذكاء الاصطناعي استنفدت لهذا اليوم. يرجى المحاولة غداً.")

@app.get("/")
def root(): return {"app": "OustadDz", "status": "running"}

@app.get("/health")
def health(): return {"status": "ok"}

@app.head("/health")
async def health_head(): return {}
