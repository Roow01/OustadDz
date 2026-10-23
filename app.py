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

import requests
from bs4 import BeautifulSoup

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

# =========================================================
# قاعدة بيانات الروابط الشاملة (DzExams)
# =========================================================
EXAMDZ_SECONDARY_JSON = """
{
  "السنة الأولى ثانوي": {
    "جذع مشترك علوم وتكنولوجيا": {
      "الرياضيات": "https://www.dzexams.com/ar/1as-math",
      "الفيزياء والتكنولوجيا": "https://www.dzexams.com/ar/1as-pc",
      "علوم الطبيعة والحياة": "https://www.dzexams.com/ar/1as-snv",
      "اللغة العربية وآدابها": "https://www.dzexams.com/ar/1as-ar",
      "اللغة الفرنسية": "https://www.dzexams.com/ar/1as-fr",
      "اللغة الإنجليزية": "https://www.dzexams.com/ar/1as-en",
      "التاريخ والجغرافيا": "https://www.dzexams.com/ar/1as-hg",
      "العلوم الإسلامية": "https://www.dzexams.com/ar/1as-is",
      "الإعلام الآلي": "https://www.dzexams.com/ar/1as-inf"
    },
    "جذع مشترك آداب": {
      "اللغة العربية وآدابها": "https://www.dzexams.com/ar/1as-ar",
      "اللغة الفرنسية": "https://www.dzexams.com/ar/1as-fr",
      "اللغة الإنجليزية": "https://www.dzexams.com/ar/1as-en",
      "التاريخ والجغرافيا": "https://www.dzexams.com/ar/1as-hg",
      "العلوم الإسلامية": "https://www.dzexams.com/ar/1as-is",
      "الرياضيات": "https://www.dzexams.com/ar/1as-math",
      "علوم الطبيعة والحياة": "https://www.dzexams.com/ar/1as-snv",
      "الإعلام الآلي": "https://www.dzexams.com/ar/1as-inf"
    }
  },
  "السنة الثانية ثانوي": {
    "علوم تجريبية": {
      "علوم الطبيعة والحياة": "https://www.dzexams.com/ar/2as-snv",
      "الفيزياء": "https://www.dzexams.com/ar/2as-pc",
      "الرياضيات": "https://www.dzexams.com/ar/2as-math",
      "اللغة العربية وآدابها": "https://www.dzexams.com/ar/2as-ar",
      "اللغة الفرنسية": "https://www.dzexams.com/ar/2as-fr",
      "اللغة الإنجليزية": "https://www.dzexams.com/ar/2as-en",
      "التاريخ والجغرافيا": "https://www.dzexams.com/ar/2as-hg",
      "العلوم الإسلامية": "https://www.dzexams.com/ar/2as-is",
      "الفلسفة": "https://www.dzexams.com/ar/2as-ph"
    },
    "رياضيات": {
      "الرياضيات": "https://www.dzexams.com/ar/2as-math",
      "الفيزياء": "https://www.dzexams.com/ar/2as-pc",
      "علوم الطبيعة والحياة": "https://www.dzexams.com/ar/2as-snv",
      "اللغة العربية وآدابها": "https://www.dzexams.com/ar/2as-ar",
      "اللغة الفرنسية": "https://www.dzexams.com/ar/2as-fr",
      "اللغة الإنجليزية": "https://www.dzexams.com/ar/2as-en",
      "التاريخ والجغرافيا": "https://www.dzexams.com/ar/2as-hg",
      "العلوم الإسلامية": "https://www.dzexams.com/ar/2as-is",
      "الفلسفة": "https://www.dzexams.com/ar/2as-ph"
    },
    "تقني رياضي": {
      "الهندسة الكهربائية": "https://www.dzexams.com/ar/2as-ge",
      "الهندسة الميكانيكية": "https://www.dzexams.com/ar/2as-gm",
      "الهندسة المدنية": "https://www.dzexams.com/ar/2as-gc",
      "هندسة الطرائق": "https://www.dzexams.com/ar/2as-gp",
      "الرياضيات": "https://www.dzexams.com/ar/2as-math",
      "الفيزياء": "https://www.dzexams.com/ar/2as-pc",
      "اللغة العربية وآدابها": "https://www.dzexams.com/ar/2as-ar",
      "اللغة الفرنسية": "https://www.dzexams.com/ar/2as-fr",
      "اللغة الإنجليزية": "https://www.dzexams.com/ar/2as-en",
      "التاريخ والجغرافيا": "https://www.dzexams.com/ar/2as-hg",
      "العلوم الإسلامية": "https://www.dzexams.com/ar/2as-is"
    },
    "تسيير واقتصاد": {
      "التسيير المحاسبي والمالي": "https://www.dzexams.com/ar/2as-geb",
      "الاقتصاد والمناجمنت": "https://www.dzexams.com/ar/2as-eco",
      "القانون": "https://www.dzexams.com/ar/2as-law",
      "الرياضيات": "https://www.dzexams.com/ar/2as-math",
      "اللغة العربية وآدابها": "https://www.dzexams.com/ar/2as-ar",
      "اللغة الفرنسية": "https://www.dzexams.com/ar/2as-fr",
      "اللغة الإنجليزية": "https://www.dzexams.com/ar/2as-en",
      "التاريخ والجغرافيا": "https://www.dzexams.com/ar/2as-hg",
      "العلوم الإسلامية": "https://www.dzexams.com/ar/2as-is"
    },
    "آداب وفلسفة": {
      "الفلسفة": "https://www.dzexams.com/ar/2as-ph",
      "اللغة العربية وآدابها": "https://www.dzexams.com/ar/2as-ar",
      "اللغة الفرنسية": "https://www.dzexams.com/ar/2as-fr",
      "اللغة الإنجليزية": "https://www.dzexams.com/ar/2as-en",
      "التاريخ والجغرافيا": "https://www.dzexams.com/ar/2as-hg",
      "العلوم الإسلامية": "https://www.dzexams.com/ar/2as-is",
      "الرياضيات": "https://www.dzexams.com/ar/2as-math"
    },
    "لغات أجنبية": {
      "اللغة العربية وآدابها": "https://www.dzexams.com/ar/2as-ar",
      "اللغة الفرنسية": "https://www.dzexams.com/ar/2as-fr",
      "اللغة الإنجليزية": "https://www.dzexams.com/ar/2as-en",
      "اللغة الإسبانية": "https://www.dzexams.com/ar/2as-es",
      "اللغة الألمانية": "https://www.dzexams.com/ar/2as-de",
      "اللغة الإيطالية": "https://www.dzexams.com/ar/2as-it",
      "التاريخ والجغرافيا": "https://www.dzexams.com/ar/2as-hg",
      "الفلسفة": "https://www.dzexams.com/ar/2as-ph",
      "الرياضيات": "https://www.dzexams.com/ar/2as-math"
    }
  },
  "السنة الثالثة ثانوي (بكالوريا)": {
    "علوم تجريبية": {
      "علوم الطبيعة والحياة": "https://www.dzexams.com/ar/3as-snv",
      "الفيزياء": "https://www.dzexams.com/ar/3as-pc",
      "الرياضيات": "https://www.dzexams.com/ar/3as-math",
      "اللغة العربية وآدابها": "https://www.dzexams.com/ar/3as-ar",
      "اللغة الفرنسية": "https://www.dzexams.com/ar/3as-fr",
      "اللغة الإنجليزية": "https://www.dzexams.com/ar/3as-en",
      "الفلسفة": "https://www.dzexams.com/ar/3as-ph",
      "التاريخ والجغرافيا": "https://www.dzexams.com/ar/3as-hg",
      "العلوم الإسلامية": "https://www.dzexams.com/ar/3as-is"
    },
    "رياضيات": {
      "الرياضيات": "https://www.dzexams.com/ar/3as-math",
      "الفيزياء": "https://www.dzexams.com/ar/3as-pc",
      "علوم الطبيعة والحياة": "https://www.dzexams.com/ar/3as-snv",
      "اللغة العربية وآدابها": "https://www.dzexams.com/ar/3as-ar",
      "اللغة الفرنسية": "https://www.dzexams.com/ar/3as-fr",
      "اللغة الإنجليزية": "https://www.dzexams.com/ar/3as-en",
      "الفلسفة": "https://www.dzexams.com/ar/3as-ph",
      "التاريخ والجغرافيا": "https://www.dzexams.com/ar/3as-hg",
      "العلوم الإسلامية": "https://www.dzexams.com/ar/3as-is"
    },
    "تقني رياضي": {
      "الهندسة الكهربائية": "https://www.dzexams.com/ar/3as-ge",
      "الهندسة الميكانيكية": "https://www.dzexams.com/ar/3as-gm",
      "الهندسة المدنية": "https://www.dzexams.com/ar/3as-gc",
      "هندسة الطرائق": "https://www.dzexams.com/ar/3as-gp",
      "الرياضيات": "https://www.dzexams.com/ar/3as-math",
      "الفيزياء": "https://www.dzexams.com/ar/3as-pc",
      "اللغة العربية وآدابها": "https://www.dzexams.com/ar/3as-ar",
      "اللغة الفرنسية": "https://www.dzexams.com/ar/3as-fr",
      "اللغة الإنجليزية": "https://www.dzexams.com/ar/3as-en",
      "الفلسفة": "https://www.dzexams.com/ar/3as-ph",
      "التاريخ والجغرافيا": "https://www.dzexams.com/ar/3as-hg"
    },
    "تسيير واقتصاد": {
      "التسيير المحاسبي والمالي": "https://www.dzexams.com/ar/3as-geb",
      "الاقتصاد والمالية": "https://www.dzexams.com/ar/3as-eco",
      "القانون": "https://www.dzexams.com/ar/3as-law",
      "الرياضيات": "https://www.dzexams.com/ar/3as-math",
      "اللغة العربية وآدابها": "https://www.dzexams.com/ar/3as-ar",
      "اللغة الفرنسية": "https://www.dzexams.com/ar/3as-fr",
      "اللغة الإنجليزية": "https://www.dzexams.com/ar/3as-en",
      "الفلسفة": "https://www.dzexams.com/ar/3as-ph",
      "التاريخ والجغرافيا": "https://www.dzexams.com/ar/3as-hg"
    },
    "آداب وفلسفة": {
      "الفلسفة": "https://www.dzexams.com/ar/3as-ph",
      "اللغة العربية وآدابها": "https://www.dzexams.com/ar/3as-ar",
      "اللغة الفرنسية": "https://www.dzexams.com/ar/3as-fr",
      "اللغة الإنجليزية": "https://www.dzexams.com/ar/3as-en",
      "التاريخ والجغرافيا": "https://www.dzexams.com/ar/3as-hg",
      "العلوم الإسلامية": "https://www.dzexams.com/ar/3as-is",
      "الرياضيات": "https://www.dzexams.com/ar/3as-math"
    },
    "لغات أجنبية": {
      "اللغة العربية وآدابها": "https://www.dzexams.com/ar/3as-ar",
      "اللغة الفرنسية": "https://www.dzexams.com/ar/3as-fr",
      "اللغة الإنجليزية": "https://www.dzexams.com/ar/3as-en",
      "اللغة الإسبانية": "https://www.dzexams.com/ar/3as-es",
      "اللغة الألمانية": "https://www.dzexams.com/ar/3as-de",
      "اللغة الإيطالية": "https://www.dzexams.com/ar/3as-it",
      "التاريخ والجغرافيا": "https://www.dzexams.com/ar/3as-hg",
      "الفلسفة": "https://www.dzexams.com/ar/3as-ph"
    }
  }
}
"""
EXAMDZ_SECONDARY = json.loads(EXAMDZ_SECONDARY_JSON)
examdz_text = json.dumps(EXAMDZ_SECONDARY, ensure_ascii=False, indent=2)

curriculum_text = json.dumps(CURRICULUM_DATA, ensure_ascii=False, indent=2)

def _fetch_web_content(url: str) -> str:
    if not url: return ""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        for script in soup(["script", "style"]): script.decompose()
        text = soup.get_text(separator=' ', strip=True)
        return text[:4000]
    except Exception as e:
        logger.warning(f"Scraping failed for {url}: {e}")
        return ""

# =========================================================
# البرومبت الذهبي (مع العناصر النائبة)
# =========================================================
GOLDEN_PROMPT_TEMPLATE = """أنت "OustadDz"، نظام ذكاء اصطناعي فائق الذكاء والشمولية (مثل ChatGPT). تتقن جميع اللغات والدارجة الجزائرية. 

# 🎭 شخصياتك:
1. **الذكاء العام:** تصرف كأي مساعد ذكي متمكن في الدردشة العامة.
2. **الخبير التربوي والمدرب:** أستاذ خبير، مرافق بيداغوجي، ومدرب في المنظومة التربوية الجزائرية.

# 🔄 آلية التحول الذكي:
- **الدردشة العامة:** رحب بالمستخدم بذكاء وأجب عن أسئلته العامة.
- **دعوة لمرة واحدة:** في نهاية أول رد عام، أضف: "إذا كنت تلميذاً أو أستاذاً وترغب في الخوض في المنهاج أو الدروس، فأنا هنا لخدمتك."
- **التفعيل والتدقيق:** إذا سأل سؤالاً دراسياً، تحول فوراً إلى "الخبير التربوي". **يُمنع تقديم إجابة تعليمية** إذا لم يذكر (أستاذ أم تلميذ؟ السنة 1،2،3؟ الشعبة؟). يجب أن تطلب هذه المعلومات أولاً.

# 🧠 ميزات "الأستاذ المدرب المتطور":
- **الكشف القبلي:** إذا لم يفهم الطالب، اسأله سؤالاً بسيطاً للتأكد من الأساسيات قبل الشرح.
- **التدريب (Coach):** دعم نفسي للتلاميذ، واقتراح مواضيع بكالوريا. مساعدة الأساتذة في بناء الفروض وفق الدروس التي أداها.
- **التمريس التطبيقي:** اطلب من الطالب التطبيق وليس الحفظ.

# 📚 المنهاج النظري (CURRICULUM_DATA):
__CURRICULUM__

# 🔗 دليل الروابط الرسمي (DzExams):
__EXAMDZ__

# 🧠 محتوى مسحوب من الإنترنت لدعم إجابتك (Context):
__CONTEXT__

# 🎯 قواعد تقديم الروابط:
1. **الافتراضي:** قدم الشرح من (CURRICULUM_DATA). **لا تضع أي رابط** إلا في الحالتين التاليتين.
2. **طلب صريح:** إذا طلب رابطاً (مثال: "أعطني رابط الفروض")، ابحث في (DzExams) وأعطه الرابط فوراً.
3. **ضرورة بيداغوجية:** يمكنك اقتراح الرابط بلباقة بعد شرح درس طويل، ولا تضعه إلا إذا وافق المستخدم.
4. **ممنوع** إعطاء رابط لمادة أو سنة أو شعبة غير التي حددها المستخدم.

# 🎯 قواعد عامة:
- أجب في صلب الموضوع، بدون ثرثرة.
- استخدم لغة المستخدم.
"""

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    image_base64: Optional[str] = None
    history: Optional[List[ChatMessage]] = None
    context_hint: Optional[dict] = None 

class ChatResponse(BaseModel):
    reply: str

app = FastAPI(title="OustadDz API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=False, allow_methods=["*"], allow_headers=["*"])

def _decode_image(b64: str) -> Image.Image:
    if "," in b64: b64 = b64.split(",", 1)[1]
    raw = base64.b64decode(b64)
    img = Image.open(io.BytesIO(raw))
    return img.convert("RGB") if img.mode not in ("RGB", "L") else img

def _call_openrouter(messages) -> str:
    response = openrouter_client.chat.completions.create(model="openai/gpt-4o-mini", messages=messages, temperature=0.3, max_tokens=2048)
    return (response.choices[0].message.content or "").strip()

def _call_groq(messages, model_name="openai/gpt-oss-120b") -> str:
    completion = groq_client.chat.completions.create(model=model_name, messages=messages, temperature=0.3, max_tokens=2048)
    return (completion.choices[0].message.content or "").strip()

def _call_gemini(contents, final_prompt) -> str:
    model = genai.GenerativeModel(model_name="gemini-3.6-flash", system_instruction=final_prompt)
    response = model.generate_content(contents)
    return (response.text or "").strip()

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    if not req.message and not req.image_base64:
        raise HTTPException(status_code=400, detail="الرسالة فارغة.")

    context_from_web = ""
    # استخدام context_hint إذا تم تمريره (اختياري)
    if req.context_hint:
        level = req.context_hint.get("level")
        stream = req.context_hint.get("stream")
        subject = req.context_hint.get("subject")
        if level and stream and subject:
            try:
                url = EXAMDZ_SECONDARY.get(level, {}).get(stream, {}).get(subject)
                if url:
                    context_from_web = f"\n[محتوى مسحوب من DzExams:]\n" + _fetch_web_content(url)
            except Exception as e:
                logger.warning(f"Context fetch error: {e}")

    # استبدال العناصر النائبة بالقيم الفعلية
    final_prompt = GOLDEN_PROMPT_TEMPLATE.replace("__CURRICULUM__", curriculum_text)
    final_prompt = final_prompt.replace("__EXAMDZ__", examdz_text)
    final_prompt = final_prompt.replace("__CONTEXT__", context_from_web)
    
    messages = [{"role": "system", "content": final_prompt}]
    
    if req.history:
        for msg in req.history[-4:]: 
            messages.append({"role": msg.role, "content": msg.content})
    
    if req.image_base64:
        messages.append({"role": "user", "content": [
            {"type": "text", "text": req.message},
            {"type": "image_url", "image_url": {"url": req.image_base64}}
        ]})
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
                role = "user" if m["role"] == "user" else "model"
                if isinstance(m["content"], str):
                    contents.append({"role": role, "parts": [m["content"]]})
                else: 
                    parts = [{"text": p["text"]} if p["type"]=="text" else _decode_image(p["image_url"]["url"]) for p in m["content"]]
                    contents.append({"role": role, "parts": parts})
            return ChatResponse(reply=_call_gemini(contents, final_prompt))
        except Exception as e: logger.error(f"Gemini failed: {e}")

    raise HTTPException(status_code=502, detail="الخوادم مشغولة حالياً.")

@app.get("/")
def root(): return {"app": "OustadDz", "status": "running"}

@app.get("/health")
def health(): return {"status": "ok"}

@app.head("/health")
async def health_head(): return {}
