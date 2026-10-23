import os
import io
import base64
import json
import logging
from typing import Optional, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PIL import Image

import google.generativeai as genai
from groq import Groq
from openai import OpenAI

from curriculum_data import CURRICULUM_DATA

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("OustadDz")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

genai.configure(api_key=GEMINI_API_KEY)
groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
openrouter_client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=OPENROUTER_API_KEY) if OPENROUTER_API_KEY else None

curriculum_text = json.dumps(CURRICULUM_DATA, ensure_ascii=False, indent=2)

GOLDEN_PROMPT = f"""أنت "OustadDz" (أستاذ Dz)، مرافق التعليم الثانوي في الجزائر.
أنت ذكاء اصطناعي عام (مثل ChatGPT)، وتخصصك هو المنظومة التربوية الجزائرية (2026/2027).

# 📚 قاعدة بيانات المنهاج الرسمي:
{curriculum_text}

# 🚨 قاعدة صارمة جداً (تدقيق السؤال):
إذا طلب المستخدم شيئاً تعليمياً (درس، فرض، تمرين، موضوع، حل) **ولم يذكر سنته الدراسية وشعبته بدقة**، يُمنع منعاً باتاً أن تعطيه إجابة عامة أو تخمن. بل يجب أن ترد بذكاء ومسؤولية:
"لأتمكن من تقديم عمل دقيق ومسؤول يطابق المنهاج، يرجى توضيح: هل أنت تلميذ أم أستاذ؟ وما هي سنتك الدراسية (1، 2، أو 3 ثانوي) وشعبتك (علوم، رياضيات، تقني، آداب، لغات، تسيير)؟"
(انتظر حتى يوضح المستخدم، ثم أجب من قاعدة البيانات).

# 🧠 ميزة "الكشف القبلي" (Diagnostic):
إذا لم يفهم الطالب الدرس، اسأله سؤالاً بسيطاً للتأكد من الأساسيات قبل الشرح.

# 🎯 ميزة "المدرب" (Coach):
- **للتلميذ:** دعم نفسي، اقتراح مواضيع بكالوريا، خطة مراجعة.
- **للأستاذ:** مساعدته في بناء الفروض والاختبارات بناءً على الدروس التي أداها.

# 🎯 قواعد:
1. ممنوع الثرثرة والترحيب المكرر.
2. اذكر المصطلحات الفرنسية للمواد العلمية.
3. أجب بنفس لغة المستخدم.
"""

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

def _decode_image(b64: str) -> Image.Image:
    if "," in b64: b64 = b64.split(",", 1)[1]
    raw = base64.b64decode(b64)
    img = Image.open(io.BytesIO(raw))
    return img.convert("RGB") if img.mode not in ("RGB", "L") else img

def _call_openrouter(req: ChatRequest) -> str:
    if openrouter_client is None: raise RuntimeError("OPENROUTER_API_KEY missing")
    messages = [{"role": "system", "content": GOLDEN_PROMPT}]
    if req.history:
        for msg in req.history[-4:]: messages.append({"role": msg.role, "content": msg.content})
    if req.image_base64:
        messages.append({"role": "user", "content": [{"type": "text", "text": req.message}, {"type": "image_url", "image_url": {"url": req.image_base64}}]})
    else:
        messages.append({"role": "user", "content": req.message})
    response = openrouter_client.chat.completions.create(model="openai/gpt-4o-mini", messages=messages, temperature=0.3, max_tokens=2048)
    return (response.choices[0].message.content or "").strip()

def _call_groq(req: ChatRequest) -> str:
    if groq_client is None: raise RuntimeError("GROQ_API_KEY missing")
    messages = [{"role": "system", "content": GOLDEN_PROMPT}]
    if req.history:
        for msg in req.history[-4:]: messages.append({"role": msg.role, "content": msg.content})
    if req.image_base64:
        b64_data = req.image_base64.split(",")[-1]
        messages.append({"role": "user", "content": [{"type": "text", "text": req.message}, {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_data}"}}]})
        model_name = "qwen/qwen3.8-27b"
    else:
        messages.append({"role": "user", "content": req.message})
        model_name = "openai/gpt-oss-120b"
    completion = groq_client.chat.completions.create(model=model_name, messages=messages, temperature=0.3, max_tokens=2048)
    return (completion.choices[0].message.content or "").strip()

def _call_gemini(req: ChatRequest) -> str:
    model_name = "gemini-3.8-flash" if req.image_base64 else "gemini-3.6-flash"
    model = genai.GenerativeModel(model_name=model_name, system_instruction=GOLDEN_PROMPT)
    contents = []
    if req.history:
        for msg in req.history[-4:]: contents.append({"role": "user" if msg.role == "user" else "model", "parts": [msg.content]})
    current_parts = [req.message]
    if req.image_base64: current_parts.append(_decode_image(req.image_base64))
    contents.append({"role": "user", "parts": current_parts})
    response = model.generate_content(contents)
    return (response.text or "").strip()

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    if not req.message and not req.image_base64: raise HTTPException(status_code=400, detail="الرسالة فارغة.")
    if OPENROUTER_API_KEY:
        try: return ChatResponse(reply=_call_openrouter(req))
        except Exception as e: logger.warning(f"OpenRouter failed: {e}")
    if GROQ_API_KEY:
        try: return ChatResponse(reply=_call_groq(req))
        except Exception as e: logger.warning(f"Groq failed: {e}")
    if GEMINI_API_KEY:
        try: return ChatResponse(reply=_call_gemini(req))
        except Exception as e: logger.error(f"Gemini failed: {e}")
    raise HTTPException(status_code=502, detail="الخوادم مشغولة حالياً.")

@app.get("/")
def root(): return {"app": "OustadDz", "status": "running"}

@app.get("/health")
def health(): return {"status": "ok"}

@app.head("/health")
async def health_head(): return {}
