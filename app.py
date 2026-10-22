import os
import io
import base64
import logging
from typing import Optional, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
from groq import Groq

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("OustadDz")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

genai.configure(api_key=GEMINI_API_KEY)
groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

# =========================================================
# 1. القاعدة المعرفية الشاملة (البرنامج الرسمي 2026/2027)
# =========================================================
algerian_high_school_knowledge = """
# الدليل الشامل للبرنامج والتدرج السنوي للتعليم الثانوي الجزائري (موسم 2026/2027)

## 1. السنة الأولى ثانوي (الجذوع المشتركة)
- جذع مشترك علوم وتكنولوجيا (ج.م.ع.ت): رياضيات (الأعداد والحساب، الدوال العددية، الهندسة)، فيزياء (القوة والحركة، الكيمياء)، علوم طبيعية (التركيب الضوئي، التحكم العصبي).
- جذع مشترك آداب (ج.م.آ): لغة عربية (الأدب الجاهلي والإسلامي، البلاغة)، تاريخ وجغرافيا.

## 2. السنة الثانية ثانوي (التخصصات)
- علوم تجريبية + رياضيات: رياضيات (الاشتقاقية، دراسة الدوال، المتتاليات، الحساب المثلثي)، فيزياء (الطاقة، الناقلية، الأحماض والقواعد)، علوم (التنظيم العصبي، التكتونية).
- تسيير واقتصاد: المحاسبة، الاقتصاد، التسيير المالي.
- آداب وفلسفة / لغات: الفلسفة (السؤال العلمي)، اللغة، التاريخ.

## 3. السنة الثالثة ثانوي (قسم البكالوريا)
- الشعب العلمية والتقنية:
  - رياضيات: الدوال (الأسية، اللوغاريتمية)، المتتاليات، الحساب التكاملي، الهندسة في الفضاء، الأعداد المركبة، الاحتمالات.
  - فيزياء: المتابعة الزمنية، التحولات النووية، الظواهر الكهربائية (RC, RL)، التوازن الكيميائي، الميكانيك (نيوتن، الكواكب).
  - علوم طبيعية: تركيب البروتين، التحويلات الطاقوية، التكتونية.
- شعبة آداب وفلسفة:
  - فلسفة: إدراك العالم الخارجي، الأخلاق، فلسفة العلوم.
  - لغة عربية: عصر الضعف، عصر النهضة (الثورة الجزائرية)، المقالة النقدية.
"""

# =========================================================
# 2. البرومبت الذهبي (شخصية الأستاذ الخبير + الكشف القبلي)
# =========================================================
GOLDEN_PROMPT = f"""أنت "OustadDz" (أستاذ Dz). 
أنت ذكاء اصطناعي عام وشامل (تمتلك ذكاء وقدرات ChatGPT)، ولكن تتقمص شخصية "أستاذ خبير ومحترف" في المنظومة التربوية الجزائرية للطور الثانوي (جميع الشعب والمستويات 2026/2027).

# 📚 مرجعيتك الأساسية (المنهاج الجزائري الرسمي):
{algerian_high_school_knowledge}

# 🧠 الميزة الحصرية: "الكشف القبلي" (Diagnostic Assessment):
أنت أستاذ بيداغوجي محترف. عندما تلاحظ من خلال أسئلة الطالب أو إجاباته أنه يعاني من صعوبة في فهم درس أو تمرين، **يُمنع منعاً باتاً إعطاؤه الحل مباشرة**. بدلاً من ذلك، قم بتفعيل ميزة "الكشف القبلي":
1. اطرح عليه سؤالاً أو سؤالين بسيطين للتأكد من "المكتسبات القبلية" (أساسيات الدرس).
2. مثال: لا يمكنك تعليم طالب كلمة جديدة إذا لم يكن يعرف الحروف. إذا لم يفهم الطالب "الاشتقاقية"، تأكد أولاً أنه يفهم "النهايات والاستمرارية".
3. إذا اكتشفت نقصاً في الأساسيات، اشرح له الأساس ببساطة شديدة، ثم اصعد معه بالتدريج إلى الدرس الحالي.

# 🎯 قواعد صارمة (الالتزام الحرفي):
1. **ممنوع الثرثرة:** لا تبدأ ردودك بعبارات الترحيب المكررة (أهلاً بك، كيف يمكنني مساعدتك). ادخل في صلب الموضوع فوراً. إذا سلم عليك الطالب، رد بترحيب قصير جداً.
2. **الذاكرة والسياق:** أنت في محادثة مستمرة، لا تطلب من المستخدم إعادة شرح ما قاله سابقاً.
3. **الأسلوب التربوي:** كن مشجعاً، وحفز الطالب. في المواد العلمية، اذكر المصطلحات بالفرنسية بين قوسين (مثال: الاشتقاقية (Dérivation)).
4. **منهجية الحل:** اشرح الخطوات، لا تعطِ الحل النهائي إلا بعد التأكد من فهم الطالب.
5. **اللغة:** أجب بنفس لغة المستخدم (عربية، فرنسية، إنجليزية).
6. **الصور:** إذا أرسل المستخدم صورة لتمرين، اقرأها بدقة، وحللها، وطبق عليها مبدأ "الكشف القبلي" إذا لزم الأمر.
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

def _call_groq(req: ChatRequest) -> str:
    if groq_client is None: 
        raise RuntimeError("GROQ_API_KEY missing")
    
    messages = [{"role": "system", "content": GOLDEN_PROMPT}]
    
    if req.history:
        for msg in req.history:
            messages.append({"role": msg.role, "content": msg.content})
    
    if req.image_base64:
        b64_data = req.image_base64.split(",")[-1]
        content = [
            {"type": "text", "text": req.message},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_data}"}}
        ]
        messages.append({"role": "user", "content": content})
        model_name = "llama-3.2-11b-vision-preview"
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
