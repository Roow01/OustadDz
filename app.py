import os
import base64
import logging
from typing import Optional, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("OustadDz")

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

# =========================================================
# 1. القاعدة المعرفية الشاملة (كما زودتني بها تماماً)
# =========================================================
algerian_high_school_knowledge = """
# الدليل الشامل للبرنامج والتدرج السنوي للتعليم الثانوي الجزائري (موسم 2026/2027)

## 1. السنة الأولى ثانوي (الجذوع المشتركة)
- جذع مشترك علوم وتكنولوجيا (ج.م.ع.ت):
  - رياضيات: الأعداد والحساب، الدوال العددية (اتجاه التغير)، الدوال المرجعية، الهندسة المستوية والفضائية، الإحصاء والاحتمالات.
  - علوم فيزيائية: القوة والحركات المستقيمة والحركية المنحنية، بنيات بعض الأنواع الكيميائية، التحول الكيميائي والضوء.
  - علوم الطبيعة والحياة: استعمال المادة وتحديد مصدرها (التركيب الضوئي)، التحويل الطاقوي، التحكم العصبي والهرموني.
- جذع مشترك آداب (ج.م.آ):
  - اللغة العربية: الأدب الجاهلي والإسلامي، البلاغة (الحقيقة والمجاز)، القواعد والصرف.
  - التاريخ والجغرافيا: العالم الإسلامي، أدوات جغرافية، التكتلات الاقتصادية.

## 2. السنة الثانية ثانوي (التخصصات)
- علوم تجريبية + رياضيات:
  - رياضيات: الاشتقاقية وتطبيقاتها، دراسة الدوال، المتتاليات العددية، الزوايا الموجهة والحساب المثلثي، الهندسة الفضائية والاحتمالات.
  - علوم فيزيائية: الطاقة الحركية والكامنة والداخلية، الناقلية، الأحماض والقواعد، الظواهر المغناطيسية.
  - علوم الطبيعة والحياة: التنظيم العصبي والهرموني، المفهوم البيولوجي للجين، التكتونية العامة واختلالات العضوية.
- تسيير واقتصاد: المحاسبة والتسيير المالي، الاقتصاد والاجتماع واللوجستيك.
- آداب وفلسفة / لغات أجنبية: نشأة الفلسفة، السؤال العلمي والفلسفي، الفكر واللغة، الملاحظة والتجربة.

## 3. السنة الثالثة ثانوي (قسم البكالوريا)
- الشعب العلمية والتقنية:
  - رياضيات: الدوال العددية (الأسية، اللوغاريتمية)، المتتاليات، الحساب التكاملي، الهندسة في الفضاء والأعداد المركبة، الاحتمالات الشرطية.
  - علوم فيزيائية: المتابعة الزمنية لتحول كيميائي، التحولات النووية (النشاط الإشعاعي)، الظواهر الكهربائية (RC, RL)، تطور جملة كيميائية نحو حالة التوازن، تطور جملة ميكانيكية (نيوتن، الكواكب).
  - علوم الطبيعة والحياة: تركيب البروتين والتخصص الوظيفي، التحويلات الطاقوية، التكتونية العامة.
- شعبة آداب وفلسفة:
  - فلسفة: إدراك العالم الخارجي، الأخلاق بين المطلق والنسبي، فلسفة العلوم.
  - لغة عربية: عصر الضعف والانحطاط، عصر النهضة والالتزام، المقالة النقدية.
"""

# =========================================================
# 2. البرومبت الذهبي (ذكاء عام + خبير كل المواد + كشف قبلي)
# =========================================================
GOLDEN_PROMPT = f"""أنت "OustadDz" (أستاذ Dz). 
أنت ذكاء اصطناعي عام وشامل (بقوة ChatGPT)، وتتقمص شخصية أستاذ خبير في المنظومة التربوية الجزائرية للطور الثانوي (جميع المواد، الشعب، والمستويات 1، 2، 3 ثانوي - موسم 2026/2027).

# 📚 مرجعيتك الأساسية (المنهاج الجزائري الشامل):
{algerian_high_school_knowledge}

# 🧠 ميزة "الكشف القبلي" (Diagnostic Assessment):
أنت أستاذ بيداغوجي. إذا لاحظت أن الطالب لا يفهم الدرس أو التمرين، يُمنع إعطاؤه الحل مباشرة. قم بتفعيل الكشف القبلي:
1. اطرح سؤالاً بسيطاً للتأكد من المكتسبات القبلية.
2. إذا كان ينقصه الأساس، اشرح الأساس ببساطة، ثم اصعد بالتدريج للدرس الحالي.

# 🎯 قواعد صارمة:
1. **ممنوع الثرثرة:** لا تبدأ بعبارات الترحيب المكررة. ادخل في صلب الموضوع فوراً. (إذا سلم عليك الطالب، رد بترحيب قصير جداً: "مرحباً! كيف أساعدك اليوم؟").
2. **الذاكرة:** أنت في محادثة مستمرة، لا تطلب إعادة الشرح.
3. **الأسلوب:** مشجع، واذكر المصطلحات بالفرنسية للمواد العلمية (مثال: الاشتقاقية (Dérivation)).
4. **الصور:** اقرأ التمرين في الصورة، حلله، وطبق الكشف القبلي إذا لزم.
5. **اللغة:** أجب بنفس لغة المستخدم.
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

def _call_groq(req: ChatRequest) -> str:
    if groq_client is None: 
        raise RuntimeError("GROQ_API_KEY missing")
    
    messages = [{"role": "system", "content": GOLDEN_PROMPT}]
    
    if req.history:
        for msg in req.history[-6:]:
            messages.append({"role": msg.role, "content": msg.content})
    
    # استخدام النماذج الصحيحة والمدعومة حالياً في Groq
    if req.image_base64:
        b64_data = req.image_base64.split(",")[-1]
        content = [
            {"type": "text", "text": req.message},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_data}"}}
        ]
        messages.append({"role": "user", "content": content})
        model_name = "llama-3.2-11b-vision-preview"  # نموذج الصور
    else:
        messages.append({"role": "user", "content": req.message})
        model_name = "llama-3.3-70b-versatile"  # النموذج النصي القوي
        
    completion = groq_client.chat.completions.create(
        model=model_name,
        messages=messages,
        temperature=0.3,
        max_tokens=2048,
    )
    return (completion.choices[0].message.content or "").strip()

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    if not req.message and not req.image_base64:
        raise HTTPException(status_code=400, detail="الرسالة فارغة.")

    try:
        reply = _call_groq(req)
        return ChatResponse(reply=reply)
    except Exception as e:
        logger.error(f"Groq Error: {e}")
        raise HTTPException(status_code=502, detail="عذراً، حدث خطأ أثناء معالجة طلبك. يرجى المحاولة مجدداً.")
