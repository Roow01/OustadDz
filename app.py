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

# استدعاء المحركات الثلاثة
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

# تحويل بيانات المنهاج إلى نص مقروء ومفصل للذكاء الاصطناعي
curriculum_text = json.dumps(CURRICULUM_DATA, ensure_ascii=False, indent=2)

# =========================================================
# البرومبت الذهبي (أستاذ خبير + كشف قبلي + بدون خلط)
# =========================================================
GOLDEN_PROMPT = f"""أنت "OustadDz" (أستاذ Dz). 
أنت ذكاء اصطناعي عام وشامل (بقوة ChatGPT)، وتتقمص شخصية أستاذ خبير ومحترف في المنظومة التربوية الجزائرية للطور الثانوي.

# 📚 قاعدة بيانات المنهاج الرسمي (2026/2027) - مرجعك الوحيد:
{curriculum_text}

# 🧠 قواعد صارمة جداً (الالتزام الحرفي):
1. **الاعتماد الحصري:** اعتمد حصرياً على "قاعدة بيانات المنهاج" أعلاه للإجابة عن أي سؤال يخص الدروس، المحاور، التوزيع الفصلي، أو التغييرات الجديدة.
2. **التمييز بين الشعب (حرج جداً):** لا تخلط بين المواد أو الشعب. إذا سألك طالب، حدد مستواه وشعبته أولاً، ثم أجب من البيانات المخصصة لشعبته فقط. (مثال: مادة الفيزياء في "جذع مشترك آداب" هي "المحلول المائي"، بينما في "علوم" هي "النوع الكيميائي"). لا تعطِ دروساً لشعبة غير موجودة في قاعدة البيانات.
3. **الكشف القبلي:** إذا لاحظت أن الطالب لا يفهم، اسأله سؤالاً بسيطاً للتأكد من المكتسبات القبلية، ثم اصعد معه بالتدريج.
4. **ممنوع الثرثرة:** لا تبدأ بعبارات الترحيب المكررة. ادخل في صلب الموضوع فوراً.
5. **الذاكرة:** أنت في محادثة مستمرة، لا تطلب إعادة الشرح.
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================================================
# دوال المعالجة (المحركات الثلاثة)
# =========================================================
def _decode_image(b64: str) -> Image.Image:
    if "," in b64: b64 = b64.split(",", 1)[1]
    raw = base64.b64decode(b64)
    img = Image.open(io.BytesIO(raw))
    return img.convert("RGB") if img.mode not in ("RGB", "L") else img

def _call_gemini(req: ChatRequest) -> str:
    model_name = "gemini-1.5-flash-latest" if req.image_base64 else "gemini-1.5-pro-latest"
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

def _call_openrouter(req: ChatRequest) -> str:
    if openrouter_client is None: raise RuntimeError("OPENROUTER_API_KEY missing")
    
    messages = [{"role": "system", "content": GOLDEN_PROMPT}]
    if req.history:
        for msg in req.history[-4:]:
            messages.append({"role": msg.role, "content": msg.content})
    
    if req.image_base64:
        messages.append({"role": "user", "content": [{"type": "text", "text": req.message}, {"type": "image_url", "image_url": {"url": req.image_base64}}]})
    else:
        messages.append({"role": "user", "content": req.message})
        
    response = openrouter_client.chat.completions.create(
        model="openai/gpt-4o-mini", messages=messages, temperature=0.3, max_tokens=2048,
    )
    return (response.choices[0].message.content or "").strip()

def _call_groq(req: ChatRequest) -> str:
    if groq_client is None: raise RuntimeError("GROQ_API_KEY missing")
    
    messages = [{"role": "system", "content": GOLDEN_PROMPT}]
    if req.history:
        for msg in req.history[-4:]:
            messages.append({"role": msg.role, "content": msg.content})
    
    if req.image_base64:
        b64_data = req.image_base64.split(",")[-1]
        messages.append({"role": "user", "content": [{"type": "text", "text": req.message}, {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_data}"}}]})
        model_name = "llama-3.2-90b-vision-preview"
    else:
        messages.append({"role": "user", "content": req.message})
        model_name = "openai/gpt-oss-120b"
        
    completion = groq_client.chat.completions.create(
        model=model_name, messages=messages, temperature=0.3, max_tokens=2048,
    )
    return (completion.choices[0].message.content or "").strip()

# =========================================================
# نقطة النهاية
# =========================================================
@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    if not req.message and not req.image_base64:
        raise HTTPException(status_code=400, detail="الرسالة فارغة.")

    if GEMINI_API_KEY:
        try:
            return ChatResponse(reply=_call_gemini(req))
        except Exception as e: logger.warning(f"Gemini failed: {e}")

    if OPENROUTER_API_KEY:
        try:
            return ChatResponse(reply=_call_openrouter(req))
        except Exception as e: logger.warning(f"OpenRouter failed: {e}")

    if GROQ_API_KEY:
        try:
            return ChatResponse(reply=_call_groq(req))
        except Exception as e: logger.error(f"Groq failed: {e}")

    raise HTTPException(status_code=502, detail="عذراً، الخوادم مشغولة حالياً. يرجى المحاولة بعد قليل.")
