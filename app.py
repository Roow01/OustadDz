# app.py — OustadDz Backend (FastAPI)
# Powered by Qimah Production

import os
import io
import base64
import logging
from typing import Optional, List

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from PIL import Image

import google.generativeai as genai
from groq import Groq

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("OustadDz")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

genai.configure(api_key=GEMINI_API_KEY)
groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

# =========================================================
# البرومبت الذهبي المحدث (شخصية الأستاذ + الذكاء العام)
# =========================================================
GOLDEN_PROMPT = """أنت "OustadDz" (أستاذ Dz)، مساعد ذكاء اصطناعي عام وشامل (مثل ChatGPT في قدراتك)، ولكن تتقمص شخصية محددة بدقة:

# 🎯 هويتك ومهمتك:
1. أنت **ذكاء اصطناعي عام**، يمكنك الإجابة عن أي سؤال (تقني، ثقافي، عام) بذكاء وموضوعية.
2. تخصصك الدقيق: **أستاذ في التربية والتعليم الجزائري للطور الثانوي** (جميع الشعب والمستويات).
3. مرجعيتك: البرنامج والمخططات الرسمية لوزارة التربية الوطنية الجزائرية لسنة **2026/2027**.
4. أنت **مرافق نفسي وبيداغوجي** يدعم الطالب الجزائري، خاصة المقبلين على البكالوريا.

# 🌍 اللغات:
- تتحدث جميع اللغات وتتكيف فوراً مع لغة المستخدم (عربية، فرنسية، إنجليزية، أمازيغية). إذا كتب بالفرنسية أجب بالفرنسية، وإذا كتب بالعربية أجب بالعربية.

# 📚 تخصصاتك (المنهاج الجزائري):
- الرياضيات (جميع الشعب)، الفيزياء، العلوم الطبيعية، اللغات، الفلسفة، التاريخ والجغرافيا، المواد التقنية، التسيير والاقتصاد.
- تمتلك وثائق التدرج السنوي والتوجيهات البيداغوجية الرسمية.

# 🧠 قواعد صارمة:
1. **الدقة العلمية**: لا تختلق معلومات. إذا لم تكن متأكداً قل: "هذه المعلومة تحتاج تحققاً من الأستاذ المختص".
2. **منهجية الحل**: لا تعطِ الحل الجاهز مباشرة. اشرح الخطوات، أرشد الطالب، ثم اعرض الحل الكامل.
3. **الدعم النفسي**: إذا لاحظت قلقاً أو إحباطاً، طمئن الطالب أولاً، واقترح عليه خطة مراجعة واقعية.
4. **الصيغة**: استخدم Markdown للعناوين، وLaTeX للمعادلات (\(x^2\) أو \[x^2\]).
5. **الصور**: إذا أرسل الطالب صورة تمرين، اقرأ محتواها بدقة، لخص المطلوب، ثم اشرح المنهجية خطوة بخطوة.

# ✍️ التوقيع:
في نهاية كل رد مهم، أضف سطراً منفصلاً:
> 🤖 **OustadDz** — Powered by **Qimah Production** 🇩🇿
"""

class ChatRequest(BaseModel):
    message: str
    image_base64: Optional[str] = None
    subject: Optional[str] = None
    level: Optional[str] = None
    history: Optional[List[dict]] = None

class ChatResponse(BaseModel):
    reply: str
    engine: str

app = FastAPI(title="OustadDz API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def _decode_image(b64: str) -> Image.Image:
    if "," in b64:
        b64 = b64.split(",", 1)[1]
    raw = base64.b64decode(b64)
    img = Image.open(io.BytesIO(raw))
    if img.mode not in ("RGB", "L"):
        img = img.convert("RGB")
    return img

def _build_user_prompt(req: ChatRequest) -> str:
    parts = []
    if req.level: parts.append(f"المستوى الدراسي: {req.level}")
    if req.subject: parts.append(f"المادة: {req.subject}")
    parts.append(f"رسالة الطالب: {req.message}")
    return "\n".join(parts)

def _call_gemini(req: ChatRequest) -> str:
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=GOLDEN_PROMPT,
    )
    contents = [_build_user_prompt(req)]
    if req.image_base64:
        contents.append(_decode_image(req.image_base64))
    response = model.generate_content(contents)
    return (response.text or "").strip()

def _call_groq(req: ChatRequest) -> str:
    if groq_client is None:
        raise RuntimeError("GROQ_API_KEY غير مهيأ")
    completion = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": GOLDEN_PROMPT},
            {"role": "user", "content": _build_user_prompt(req)},
        ],
        temperature=0.6,
        max_tokens=2048,
    )
    return (completion.choices[0].message.content or "").strip()

@app.get("/")
def root():
    return {"app": "OustadDz", "status": "running", "signature": "Powered by Qimah Production"}

@app.get("/health")
def health():
    return {"status": "ok", "gemini": bool(GEMINI_API_KEY), "groq": bool(GROQ_API_KEY)}

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    if not req.message and not req.image_base64:
        raise HTTPException(status_code=400, detail="الرسالة فارغة.")

    if req.image_base64:
        if not GEMINI_API_KEY:
            raise HTTPException(status_code=503, detail="Gemini غير مهيأ لمعالجة الصور.")
        try:
            reply = _call_gemini(req)
            return ChatResponse(reply=reply, engine="gemini-1.5-flash")
        except Exception as e:
            logger.exception("فشل Gemini مع صورة")
            raise HTTPException(status_code=502, detail=f"فشل Gemini: {e}")

    if GEMINI_API_KEY:
        try:
            reply = _call_gemini(req)
            return ChatResponse(reply=reply, engine="gemini-1.5-flash")
        except Exception as e:
            logger.warning(f"Gemini فشل، التحويل إلى Groq: {e}")

    if groq_client is not None:
        try:
            reply = _call_groq(req)
            return ChatResponse(reply=reply, engine="llama-3.3-70b-versatile")
        except Exception as e:
            logger.exception("فشل Groq أيضاً")
            raise HTTPException(status_code=502, detail=f"فشل الخادم: {e}")

    raise HTTPException(status_code=503, detail="لا يوجد أي محرك متاح.")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception("خطأ غير متوقع")
    return JSONResponse(status_code=500, content={"detail": "حدث خطأ داخلي غير متوقع في الخادم."})
