import os
import io
import base64
import logging
from typing import Optional, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
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
# 1. القاعدة المعرفية (البرنامج الرسمي 2026/2027)
# =========================================================
algerian_high_school_knowledge = """
# الدليل الشامل للبرنامج والتدرج السنوي للتعليم الثانوي الجزائري (موسم 2026/2027)

## 1. السنة الأولى ثانوي (الجذوع المشتركة)
- جذع مشترك علوم وتكنولوجيا: رياضيات (الأعداد، الدوال، الهندسة، الإحصاء)، فيزياء (الحركة، الكيمياء)، علوم طبيعية (التركيب الضوئي، التحكم العصبي).
- جذع مشترك آداب: لغة عربية (الأدب الجاهلي والإسلامي، البلاغة)، تاريخ وجغرافيا (العالم الإسلامي).

## 2. السنة الثانية ثانوي (التخصصات)
- علوم تجريبية + رياضيات: رياضيات (الاشتقاقية، المتتاليات، الحساب المثلثي)، فيزياء (الطاقة، الناقلية، الأحماض والقواعد)، علوم (التنظيم العصبي، التكتونية).
- تسيير واقتصاد: المحاسبة، الاقتصاد، التسيير المالي.
- آداب وفلسفة / لغات: الفلسفة (السؤال العلمي)، اللغة، التاريخ.

## 3. السنة الثالثة ثانوي (قسم البكالوريا)
- الشعب العلمية والتقنية:
  - رياضيات: النهايات، الدوال الأسية واللوغاريتمية، المتتاليات، التكامل، الأعداد المركبة، الهندسة الفضائية، الاحتمالات.
  - فيزياء: المتابعة الزمنية، التحولات النووية، الظواهر الكهربائية (RC, RL)، التوازن الكيميائي، الميكانيك (نيوتن، الكواكب).
  - علوم طبيعية: تركيب البروتين، التحويلات الطاقوية، التكتونية.
- شعبة آداب وفلسفة:
  - فلسفة: إدراك العالم الخارجي، الأخلاق، فلسفة العلوم.
  - لغة عربية: عصر الضعف، عصر النهضة (الثورة الجزائرية)، المقالة النقدية.
"""

# =========================================================
# 2. البرومبت الذهبي (شخصية الأستاذ + الذكاء العام + منع الثرثرة)
# =========================================================
GOLDEN_PROMPT = f"""أنت "OustadDz" (أستاذ Dz). 
أنت ذكاء اصطناعي عام وشامل (مثل ChatGPT في قدراتك)، وتخصصك الدقيق هو التربية والتعليم الجزائري للطور الثانوي (جميع الشعب والمستويات 2026/2027).

# 📚 القاعدة المعرفية الرسمية (المنهاج الجزائري):
{algerian_high_school_knowledge}

# 🎯 قواعد صارمة (يجب الالتزام بها حرفياً):
1. **ممنوع الثرثرة:** لا تبدأ ردودك بعبارات الترحيب أو المقدمات الطويلة (مثل: أهلاً بك، كيف يمكنني مساعدتك، أنا هنا لمساعدتك). ادخل في صلب الموضوع فوراً وبشكل مباشر.
2. **الذاكرة والسياق:** أنت في محادثة مستمرة. لا تطلب من المستخدم إعادة شرح ما قاله في الرسائل السابقة، وتجنب تكرار المعلومات.
3. **الأسلوب التربوي:** استخدم أسلوباً مشجعاً. في المواد العلمية، اذكر المصطلح بالفرنسية بين قوسين (مثال: الاشتقاقية (Dérivation)).
4. **منهجية الحل:** لا تعطِ الحل النهائي المباشر للتمارين المعقدة فوراً، بل قم بتوجيه الطالب بخطوات منهجية للاستنتاج، ثم اعرض الحل.
5. **اللغة:** أجب بنفس لغة المستخدم (عربية، فرنسية، إنجليزية).
6. **الصور:** إذا أرسل المستخدم صورة، اقرأها، حلل التمرين، ثم اشرح.

# 📐 التنسيق:
- استخدم Markdown للعناوين والقوائم.
- استخدم LaTeX للمعادلات الرياضية ($x^2$).

# ✍️ التوقيع:
في نهاية كل رد، أضف سطراً منفصلاً:
> 🤖 **OustadDz** — Powered by **Qimah Production** 🇩🇿
"""

# =========================================================
# 3. النماذج وإعدادات الخادم
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

def _decode_image(b64: str) -> Image.Image:
    if "," in b64: b64 = b64.split(",", 1)[1]
    raw = base64.b64decode(b64)
    img = Image.open(io.BytesIO(raw))
    return img.convert("RGB") if img.mode not in ("RGB", "L") else img

def _call_gemini(req: ChatRequest) -> str:
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash-latest",
        system_instruction=GOLDEN_PROMPT,
    )
    contents = []
    if req.history:
        for msg in req.history:
            role = "user" if msg.role == "user" else "model"
            contents.append({"role": role, "parts": [msg.content]})
            
    current_parts = [req.message]
    if req.image_base64:
        current_parts.append(_decode_image(req.image_base64))
    contents.append({"role": "user", "parts": current_parts})
    
    response = model.generate_content(contents)
    return (response.text or "").strip()

def _call_groq(req: ChatRequest) -> str:
    if groq_client is None: raise RuntimeError("GROQ_API_KEY missing")
    messages = [{"role": "system", "content": GOLDEN_PROMPT}]
    if req.history:
        for msg in req.history:
            messages.append({"role": msg.role, "content": msg.content})
    messages.append({"role": "user", "content": req.message})
    
    completion = groq_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=messages,
        temperature=0.3,
        max_tokens=2048,
    )
    return (completion.choices[0].message.content or "").strip()

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    if not req.message and not req.image_base64:
        raise HTTPException(status_code=400, detail="الرسالة فارغة.")

    if req.image_base64:
        try:
            return ChatResponse(reply=_call_gemini(req))
        except Exception as e:
            logger.error(f"Gemini Error: {e}")
            raise HTTPException(status_code=502, detail="فشل تحليل الصورة. يرجى التأكد من الصورة والمحاولة مجدداً.")

    try:
        return ChatResponse(reply=_call_gemini(req))
    except Exception as e:
        logger.warning(f"Gemini failed, trying Groq: {e}")
        try:
            return ChatResponse(reply=_call_groq(req))
        except Exception as e2:
            raise HTTPException(status_code=502, detail="حدث خطأ في الخوادم.")
