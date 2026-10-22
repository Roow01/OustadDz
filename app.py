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

# استدعاء ملف المنهاج الموسع
from curriculum_data import CURRICULUM_DATA

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("OustadDz")

# =========================================================
# إعداد المفاتيح
# =========================================================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

genai.configure(api_key=GEMINI_API_KEY)
groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
openrouter_client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=OPENROUTER_API_KEY) if OPENROUTER_API_KEY else None

# تحويل قاموس المنهاج إلى نص للذكاء الاصطناعي
curriculum_text = json.dumps(CURRICULUM_DATA, ensure_ascii=False, indent=2)

# =========================================================
# البرومبت الذهبي
# =========================================================
GOLDEN_PROMPT = f"""أنت "OustadDz" (أستاذ Dz). 
أنت ذكاء اصطناعي عام وشامل (بقوة ChatGPT)، وتتقمص شخصية أستاذ خبير في المنظومة التربوية الجزائرية للطور الثانوي.

# 📚 قاعدة بيانات المنهاج الرسمي (2026/2027) - مرجعك الوحيد:
{curriculum_text}

# 🧠 قواعد صارمة:
1. **الاعتماد الحصري:** اعتمد حصرياً على "قاعدة بيانات المنهاج" أعلاه.
2. **التمييز بين الشعب (حرج):** لا تخلط بين المواد أو الشعب. حدد المستوى والشعبة أولاً ثم أجب.
3. **الكشف القبلي:** إذا لم يفهم الطالب، اسأله سؤالاً بسيطاً للتأكد من الأساسيات ثم اصعد بالتدريج.
4. **ممنوع الثرثرة:** لا تبدأ بعبارات الترحيب المكررة.
5. **الذاكرة:** أنت في محادثة مستمرة.
6. **الأسلوب:** مشجع، واذكر المصطلحات بالفرنسية للمواد العلمية.
7. **الصور:** اقرأ التمرين، حلله، واشرحه.
8. **اللغة:** أجب بنفس لغة المستخدم.
"""

# =========================================================
# إعدادات الخادم
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

# =========================================================
# دوال المعالجة (الترتيب الجديد: OpenRouter -> Groq -> Gemini)
# =========================================================
def _decode_image(b64: str) -> Image.Image:
    if "," in b64: b64 = b64.split(",", 1)[1]
    raw = base64.b64decode(b64)
    img = Image.open(io.BytesIO(raw))
    return img.convert("RGB") if img.mode not in ("RGB", "L") else img

# --- 1. OpenRouter (الخيار الأساسي) ---
def _call_openrouter(req: ChatRequest) -> str:
    if openrouter_client is None: raise RuntimeError("OPENROUTER_API_KEY missing")
    messages = [{"role": "system", "content": GOLDEN_PROMPT}]
    if req.history:
        for msg in req.history[-4:]:
            messages.append({"role": msg.role, "content": msg.content})
    
    if req.image_base64:
        # gpt-4o-mini يدعم الصور
        messages.append({"role": "user", "content": [
            {"type": "text", "text": req.message},
            {"type": "image_url", "image_url": {"url": req.image_base64}}
        ]})
    else:
        messages.append({"role": "user", "content": req.message})
        
    response = openrouter_client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=messages,
        temperature=0.3,
        max_tokens=2048,
    )
    return (response.choices[0].message.content or "").strip()

# --- 2. Groq (الاحتياطي الأول) ---
def _call_groq(req: ChatRequest) -> str:
    if groq_client is None: raise RuntimeError("GROQ_API_KEY missing")
    messages = [{"role": "system", "content": GOLDEN_PROMPT}]
    if req.history:
        for msg in req.history[-4:]:
            messages.append({"role": msg.role, "content": msg.content})
    
    if req.image_base64:
        # النموذج البصري الجديد على Groq
        b64_data = req.image_base64.split(",")[-1]
        messages.append({"role": "user", "content": [
            {"type": "text", "text": req.message},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_data}"}}
        ]})
        model_name = "qwen/qwen3.8-27b" 
    else:
        messages.append({"role": "user", "content": req.message})
        model_name = "openai/gpt-oss-120b" # نموذج نصي قوي ومستقر
        
    completion = groq_client.chat.completions.create(
        model=model_name,
        messages=messages,
        temperature=0.3,
        max_tokens=2048,
    )
    return (completion.choices[0].message.content or "").strip()

# --- 3. Gemini (الاحتياطي الأخير) ---
def _call_gemini(req: ChatRequest) -> str:
    # استخدام النماذج الحديثة المتاحة
    model_name = "gemini-3.8-flash" if req.image_base64 else "gemini-3.6-flash"
    model = genai.GenerativeModel(model_name=model_name, system_instruction=GOLDEN_PROMPT)
    
    contents = []
    if req.history:
        for msg in req.history[-4:]:
            role = "user" if msg.role == "user" else "model"
            contents.append({"role": role, "parts": [msg.content]})
            
    current_parts = [req.message]
    if req.image_base64:
        current_parts.append(_decode_image(req.image_base64))
    contents.append({"role": "user", "parts": current_parts})
    
    response = model.generate_content(contents)
    return (response.text or "").strip()

# =========================================================
# نقطة النهاية (Endpoint)
# =========================================================
@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    if not req.message and not req.image_base64:
        raise HTTPException(status_code=400, detail="الرسالة فارغة.")

    # 1. OpenRouter أولاً (الأكثر استقراراً)
    if OPENROUTER_API_KEY:
        try:
            logger.info("Trying OpenRouter...")
            return ChatResponse(reply=_call_openrouter(req))
        except Exception as e:
            logger.warning(f"OpenRouter failed: {e}")

    # 2. Groq ثانياً
    if GROQ_API_KEY:
        try:
            logger.info("Trying Groq...")
            return ChatResponse(reply=_call_groq(req))
        except Exception as e:
            logger.warning(f"Groq failed: {e}")

    # 3. Gemini أخيراً
    if GEMINI_API_KEY:
        try:
            logger.info("Trying Gemini...")
            return ChatResponse(reply=_call_gemini(req))
        except Exception as e:
            logger.error(f"Gemini failed: {e}")

    raise HTTPException(status_code=502, detail="عذراً، الخوادم مشغولة حالياً. يرجى المحاولة بعد قليل.")

                        
# =========================================================
# مسارات الفحص الأساسية (مهمة جداً لـ UptimeRobot و Render)
# =========================================================
@app.get("/")
def root():
    return {
        "app": "OustadDz",
        "status": "running",
        "signature": "Powered by Qimah Production"
    }

@app.get("/health")
def health():
    return {
        "status": "ok",
        "gemini": bool(GEMINI_API_KEY),
        "groq": bool(GROQ_API_KEY)
    }
