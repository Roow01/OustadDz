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

# استدعاء مكتبات المحركات الثلاثة
import google.generativeai as genai
from groq import Groq
from openai import OpenAI

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

# =========================================================
# 1. القاعدة المعرفية: النص الكامل الذي زودتني به
# =========================================================
algerian_high_school_knowledge = """
# الدليل الشامل للبرنامج والتدرج السنوي للتعليم الثانوي الجزائري (موسم 2026/2027)

## 1. السنة الأولى ثانوي (الجذوع المشتركة)
- جذع مشترك علوم وتكنولوجيا (ج.م.ع.ت): رياضيات (الأعداد، الدوال، الهندسة، الإحصاء)، فيزياء (الحركة، الكيمياء)، علوم طبيعية (التركيب الضوئي، التحكم العصبي).
- جذع مشترك آداب (ج.م.آ): لغة عربية (الأدب الجاهلي والإسلامي، البلاغة)، تاريخ وجغرافيا (العالم الإسلامي).

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
# 2. الهيكل المنظم للمواد والمعاملات (لزيادة الدقة)
# =========================================================
OFFICIAL_CURRICULUM = {
    "3AS": {
        "sciences_experimentales": {
            "name": "علوم تجريبية",
            "core_subjects": ["علوم الطبيعة والحياة", "علوم فيزيائية", "رياضيات"],
            "coefficients": {"sciences": 6, "physics": 5, "math": 5, "arabic": 3, "french": 2, "english": 2, "history_geo": 2, "philosophy": 2, "islamic": 2},
            "main_axes": {
                "math": ["النهايات والاستمرارية", "الاشتقاقية", "الدوال الأسية واللوغاريتمية", "المتتاليات", "التكامل", "الأعداد المركبة", "الهندسة الفضائية", "الاحتمالات"],
                "physics": ["المتابعة الزمنية", "التحولات النووية", "الظواهر الكهربائية (RC, RL)", "التوازن الكيميائي", "الميكانيك (نيوتن، الكواكب)"],
                "sciences": ["تركيب البروتين", "التحويلات الطاقوية", "التكتونية"]
            }
        },
        "mathematiques": {
            "name": "رياضيات",
            "core_subjects": ["رياضيات", "علوم فيزيائية"],
            "coefficients": {"math": 7, "physics": 6, "sciences": 2, "arabic": 3, "french": 2, "english": 2, "history_geo": 2, "philosophy": 2, "islamic": 2},
            "main_axes": {
                "math": ["النهايات والاستمرارية", "الاشتقاقية والتزايد المقارن", "التوسع التام", "المعادلات التفاضلية", "المتتاليات والتراجع", "الدوال الأصلية والتكامل الموسع", "الأعداد المركبة والتحويلات النقطية", "الجداء السلمي", "القسمة والموافقات (غوص وغوس)", "الاحتمالات الشرطية والتوزيعات"]
            }
        },
        "technique_mathematique": {
            "name": "تقني رياضي",
            "core_subjects": ["تكنولوجيا", "رياضيات", "علوم فيزيائية"],
            "coefficients": {"technology": 6, "math": 6, "physics": 5, "arabic": 3, "french": 2, "english": 2, "history_geo": 2, "philosophy": 2, "islamic": 2},
            "main_axes": {
                "math": ["النهايات والاستمرارية", "الاشتقاقية", "التوسع التام", "المتتاليات والتراجع", "الدوال الأصلية والتكامل", "الأعداد المركبة والتحويلات", "الجداء السلمي", "القسمة في Z والموافقات", "الاحتمالات الشرطية"]
            }
        },
        "gestion_economie": {
            "name": "تسيير واقتصاد",
            "core_subjects": ["تسيير محاسبي ومالي", "اقتصاد ومناجمنت", "رياضيات", "قانون"],
            "coefficients": {"gestion": 6, "economy": 5, "math": 5, "history_geo": 4, "arabic": 3, "french": 2, "english": 2, "philosophy": 2, "islamic": 2},
            "main_axes": {
                "math": ["الدوال العددية والتزايد (تطبيقات اقتصادية)", "الدالة الأسية واللوغاريتمية", "المتتاليات الحسابية والهندسية (الفوائد)", "الإحصاء لمتغيرين (المربعات الدنيا)", "المصفوفات والأنظمة", "الاحتمالات الشرطية"]
            }
        },
        "lettres_philosophie": {
            "name": "آداب وفلسفة",
            "core_subjects": ["فلسفة", "لغة عربية", "تاريخ وجغرافيا", "لغات"],
            "coefficients": {"philosophy": 6, "arabic": 6, "history_geo": 4, "english": 3, "french": 2, "math": 2, "islamic": 2},
            "main_axes": {
                "math": ["القسمة الإقليدية والموافقات في Z", "المتتاليات الحسابية والهندسية", "الدوال العددية (كثيرة الحدود من الدرجة 2 و 3)"],
                "philosophy": ["إدراك العالم الخارجي", "الأخلاق بين المطلق والنسبي", "فلسفة العلوم"],
                "arabic": ["عصر الضعف والانحطاط", "عصر النهضة والالتزام (الثورة الجزائرية)", "المقالة النقدية"]
            }
        }
    }
}

# تحويل الهيكل إلى نص مقروء للذكاء الاصطناعي
curriculum_json_str = json.dumps(OFFICIAL_CURRICULUM, ensure_ascii=False, indent=2)

# =========================================================
# 3. البرومبت الذهبي (أستاذ خبير + كشف قبلي + ذكاء عام)
# =========================================================
GOLDEN_PROMPT = f"""أنت "OustadDz" (أستاذ Dz). 
أنت ذكاء اصطناعي عام وشامل (بقوة ChatGPT)، وتتقمص شخصية أستاذ خبير ومحترف في المنظومة التربوية الجزائرية للطور الثانوي (جميع المواد، الشعب، والمستويات 1، 2، 3 ثانوي - 2026/2027).

# 📚 مرجعيتك الأساسية (النص الكامل):
{algerian_high_school_knowledge}

# 🗂️ هيكل المواد والمعاملات الرسمي:
{curriculum_json_str}

# 🧠 ميزة "الكشف القبلي" (Diagnostic Assessment):
أنت أستاذ بيداغوجي. إذا لاحظت أن الطالب لا يفهم الدرس أو التمرين، **يُمنع إعطاؤه الحل مباشرة**. قم بتفعيل الكشف القبلي:
1. اطرح سؤالاً بسيطاً للتأكد من المكتسبات القبلية (مثال: إذا لم يفهم الاشتقاقية، تأكد أولاً أنه يفهم النهايات).
2. إذا كان ينقصه الأساس، اشرح الأساس ببساطة، ثم اصعد بالتدريج للدرس الحالي.

# 🎯 قواعد صارمة:
1. **ممنوع الثرثرة:** لا تبدأ بعبارات الترحيب المكررة. ادخل في صلب الموضوع فوراً. (إذا سلم عليك الطالب، رد بترحيب قصير جداً: "مرحباً! كيف أساعدك في دراستك اليوم؟").
2. **الذاكرة:** أنت في محادثة مستمرة، لا تطلب إعادة الشرح.
3. **الأسلوب:** مشجع، واذكر المصطلحات بالفرنسية للمواد العلمية (مثال: الاشتقاقية (Dérivation)).
4. **الصور:** اقرأ التمرين في الصورة، حلله، وطبق الكشف القبلي إذا لزم.
5. **اللغة:** أجب بنفس لغة المستخدم.
"""

# =========================================================
# 4. إعدادات الخادم والنماذج
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
# 5. دوال المعالجة (المحركات الثلاثة)
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
        for msg in req.history[-4:]: # آخر 4 رسائل للسياق
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
        messages.append({
            "role": "user",
            "content": [
                {"type": "text", "text": req.message},
                {"type": "image_url", "image_url": {"url": req.image_base64}}
            ]
        })
    else:
        messages.append({"role": "user", "content": req.message})
        
    response = openrouter_client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=messages,
        temperature=0.3,
        max_tokens=2048,
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
        content = [
            {"type": "text", "text": req.message},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_data}"}}
        ]
        messages.append({"role": "user", "content": content})
        model_name = "llama-3.2-90b-vision-preview"
    else:
        messages.append({"role": "user", "content": req.message})
        model_name = "openai/gpt-oss-120b"
        
    completion = groq_client.chat.completions.create(
        model=model_name,
        messages=messages,
        temperature=0.3,
        max_tokens=2048,
    )
    return (completion.choices[0].message.content or "").strip()

# =========================================================
# 6. نقطة النهاية (Endpoint)
# =========================================================
@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    if not req.message and not req.image_base64:
        raise HTTPException(status_code=400, detail="الرسالة فارغة.")

    # 1. المحاولة بـ Gemini أولاً
    if GEMINI_API_KEY:
        try:
            reply = _call_gemini(req)
            logger.info("تم الرد بواسطة Gemini")
            return ChatResponse(reply=reply)
        except Exception as e:
            logger.warning(f"Gemini failed: {e}")

    # 2. المحاولة بـ OpenRouter (احتياطي قوي)
    if OPENROUTER_API_KEY:
        try:
            reply = _call_openrouter(req)
            logger.info("تم الرد بواسطة OpenRouter")
            return ChatResponse(reply=reply)
        except Exception as e:
            logger.warning(f"OpenRouter failed: {e}")

    # 3. المحاولة بـ Groq (احتياطي ثالث)
    if GROQ_API_KEY:
        try:
            reply = _call_groq(req)
            logger.info("تم الرد بواسطة Groq")
            return ChatResponse(reply=reply)
        except Exception as e:
            logger.error(f"Groq failed: {e}")

    # إذا فشلت كل المحاولات
    raise HTTPException(status_code=502, detail="عذراً، الخوادم مشغولة حالياً. يرجى المحاولة بعد قليل.")
