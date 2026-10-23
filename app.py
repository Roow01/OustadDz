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
# قاعدة بيانات الروابط (EXAMDZ)
# =========================================================
EXAMDZ_SECONDARY = {
    "1AS": {
        "sciences": {
            "math": {"lessons": "https://examdz.com/1as/math/lessons", "tests": "https://examdz.com/1as/math/tests", "bac": None, "books": "https://examdz.com/books/math_1as.pdf"},
            "physics": {"lessons": "https://examdz.com/1as/physics/lessons", "tests": "https://examdz.com/1as/physics/tests", "bac": None, "books": "https://examdz.com/books/physics_1as.pdf"}
        }
    },
    "2AS": {
        "sciences": {
            "math": {"lessons": "https://examdz.com/2as/math/lessons", "tests": "https://examdz.com/2as/math/tests", "bac": "https://examdz.com/2as/math/bac", "books": "https://examdz.com/books/math_2as.pdf"},
            "physics": {"lessons": "https://examdz.com/2as/physics/lessons", "tests": "https://examdz.com/2as/physics/tests", "bac": "https://examdz.com/2as/physics/bac", "books": "https://examdz.com/books/physics_2as.pdf"}
        },
        "lettres": {
            "arabic": {"lessons": "https://examdz.com/2as/arabic/lessons", "tests": "https://examdz.com/2as/arabic/tests", "bac": "https://examdz.com/2as/arabic/bac", "books": "https://examdz.com/books/arabic_2as.pdf"},
            "philosophy": {"lessons": "https://examdz.com/2as/philosophy/lessons", "tests": "https://examdz.com/2as/philosophy/tests", "bac": "https://examdz.com/2as/philosophy/bac", "books": "https://examdz.com/books/philosophy_2as.pdf"}
        }
    },
    "3AS": {
        "sciences": {
            "math": {"lessons": "https://examdz.com/3as/math/lessons", "tests": "https://examdz.com/3as/math/tests", "bac": "https://examdz.com/3as/math/bac", "books": "https://examdz.com/books/math_3as.pdf"},
            "physics": {"lessons": "https://examdz.com/3as/physics/lessons", "tests": "https://examdz.com/3as/physics/tests", "bac": "https://examdz.com/3as/physics/bac", "books": "https://examdz.com/books/physics_3as.pdf"},
            "sciences": {"lessons": "https://examdz.com/3as/sciences/lessons", "tests": "https://examdz.com/3as/sciences/tests", "bac": "https://examdz.com/3as/sciences/bac", "books": "https://examdz.com/books/sciences_3as.pdf"}
        },
        "lettres": {
            "arabic": {"lessons": "https://examdz.com/3as/arabic/lessons", "tests": "https://examdz.com/3as/arabic/tests", "bac": "https://examdz.com/3as/arabic/bac", "books": "https://examdz.com/books/arabic_3as.pdf"},
            "philosophy": {"lessons": "https://examdz.com/3as/philosophy/lessons", "tests": "https://examdz.com/3as/philosophy/tests", "bac": "https://examdz.com/3as/philosophy/bac", "books": "https://examdz.com/books/philosophy_3as.pdf"}
        },
        "gestion": {
            "economics": {"lessons": "https://examdz.com/3as/economics/lessons", "tests": "https://examdz.com/3as/economics/tests", "bac": "https://examdz.com/3as/economics/bac", "books": "https://examdz.com/books/economics_3as.pdf"},
            "law": {"lessons": "https://examdz.com/3as/law/lessons", "tests": "https://examdz.com/3as/law/tests", "bac": "https://examdz.com/3as/law/bac", "books": "https://examdz.com/books/law_3as.pdf"}
        },
        "langues": {
            "french": {"lessons": "https://examdz.com/3as/french/lessons", "tests": "https://examdz.com/3as/french/tests", "bac": "https://examdz.com/3as/french/bac", "books": "https://examdz.com/books/french_3as.pdf"},
            "english": {"lessons": "https://examdz.com/3as/english/lessons", "tests": "https://examdz.com/3as/english/tests", "bac": "https://examdz.com/3as/english/bac", "books": "https://examdz.com/books/english_3as.pdf"},
            "spanish": {"lessons": "https://examdz.com/3as/spanish/lessons", "tests": "https://examdz.com/3as/spanish/tests", "bac": "https://examdz.com/3as/spanish/bac", "books": "https://examdz.com/books/spanish_3as.pdf"},
            "german": {"lessons": "https://examdz.com/3as/german/lessons", "tests": "https://examdz.com/3as/german/tests", "bac": "https://examdz.com/3as/german/bac", "books": "https://examdz.com/books/german_3as.pdf"}
        }
    }
}

curriculum_text = json.dumps(CURRICULUM_DATA, ensure_ascii=False, indent=2)

def _fetch_web_content(url: str) -> str:
    if not url: return ""
    if url.endswith('.pdf'): return "(هذا الملف بصيغة PDF، ولا يمكن قراءته آلياً، لذا قدم الرابط للمستخدم لتحميله)."
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

GOLDEN_PROMPT = f"""أنت "OustadDz"، نظام ذكاء اصطناعي فائق الذكاء والشمولية (مثل ChatGPT). تتقن جميع اللغات (العربية الفصحى، الفرنسية، الإنجليزية، وحتى الدارجة الجزائرية). 

# 🎭 شخصياتك (مرنة):
1. **الذكاء العام (الافتراضي):** في البداية، أو إذا سألك المستخدم أسئلة عامة (ثقافة، طبخ، تاريخ، دردشة)، تصرف كأي مساعد ذكي متمكن. أجب في صلب الموضوع، بنفس لغته أو لهجته، وبدون أي قيود تعليمية.
2. **الخبير التربوي والمدرب (عند التفعيل):** أنت أستاذ خبير، مرافق بيداغوجي، ومدرب (Coach) في المنظومة التربوية الجزائرية (2026/2027).

# 🔄 آلية التحول الذكي (State Machine):
- **الخطوة 1 (الدردشة العامة):** إذا قال لك المستخدم "أهلاً"، "سلام"، "Bonjour" أو سأل سؤالاً عاماً، رحب به بذكاء وأجب عن سؤاله (لا تطلب منه السنة أو الشعبة الآن).
- **الخطوة 2 (دعوة لمرة واحدة):** في نهاية أول رد عام لك فقط، أضف جملة قصيرة: "إذا كنت تلميذاً أو أستاذاً وترغب في الخوض في المنهاج أو الدروس، فأنا هنا لخدمتك."
- **الخطوة 3 (التفعيل والتدقيق):** إذا وافق المستخدم أو سأل سؤالاً دراسياً، تحول فوراً إلى "الخبير التربوي". **يُمنع تقديم إجابة تعليمية** إذا لم يذكر (هل هو أستاذ أم تلميذ؟) و (السنة 1،2،3) و (الشعبة). يجب أن تطلب هذه المعلومات أولاً بذكاء لضمان دقة الإجابة.
- **الخطوة 4 (الاستمرارية):** إذا كان في وضع الدردشة العامة، لا تكرر سؤاله عن التخصص.

# 🧠 ميزات "الأستاذ المدرب المتطور" (عند التفعيل):
- **الكشف القبلي (Diagnostic):** إذا لاحظت أن الطالب لا يفهم الدرس، لا تعطه الحل مباشرة. اسأله سؤالاً بسيطاً للتأكد من المكتسبات القبلية، ثم اصعد معه بالتدريج.
- **التدريب والتوجيه (Coach):** 
  - **إذا كان المستخدم تلميذاً (خاصة البكالوريا):** قدم له دعماً نفسياً إيجابياً لتخفيف التوتر، اقترح عليه مواضيع امتحانات سابقة للتدريب، وصف له خطة مراجعة واقعية.
  - **إذا كان المستخدم أستاذاً:** ساعده في بناء فروض واختبارات (مواضيع) وفق المعطيات التي يقدمها عن الدروس التي أداها. اقترح عليه أساليب بيداغوجية حديثة.
- **التمريس التطبيقي:** استخدم أساليب تعليمية حديثة، واطلب من الطالب التطبيق والتجربة، وليس مجرد الحفظ.

# 📚 المنهاج النظري (CURRICULUM_DATA):
{curriculum_text}

# 🧠 محتوى مسحوب من الإنترنت لدعم إجابتك (Context):
{context_from_web}

# 🎯 قواعد تقديم الروابط (Link Management):
1. **الافتراضي:** قدم الشرح والإجابة المباشرة من (CURRICULUM_DATA) أو من (Context). **لا تضع أي رابط** إلا في الحالتين التاليتين.
2. **الاستثناء الأول (طلب صريح):** إذا طلب المستخدم رابطاً صراحةً (مثال: "أعطني رابط الفروض")، استخدم الروابط المتاحة في السياق وأعطه الرابط فوراً.
3. **الاستثناء الثاني (ضرورة بيداغوجية):** إذا شرحتَ درساً طويلاً ورأيت أن الطالب يحتاج تمارين، يمكنك **اقتراح** الرابط بلباقة. *لا تضع الرابط إلا إذا وافق المستخدم.*
4. إذا كان الرابط الذي تم سحبه هو PDF، أخبر المستخدم أنك لا تستطيع قراءته آلياً واطلب منه تحميله.
5. **ممنوع منعاً باتاً** إعطاء رابط لمادة أو سنة أو شعبة غير التي حددها المستخدم.

# 🎯 قواعد عامة:
- أجب في صلب الموضوع، بدون ثرثرة.
- استخدم لغة المستخدم (حتى الدارجة).
- اذكر المصطلحات الفرنسية للمواد العلمية.
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

def _call_gemini(contents) -> str:
    model = genai.GenerativeModel(model_name="gemini-3.6-flash", system_instruction=GOLDEN_PROMPT)
    response = model.generate_content(contents)
    return (response.text or "").strip()

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    if not req.message and not req.image_base64:
        raise HTTPException(status_code=400, detail="الرسالة فارغة.")

    context_from_web = ""
    if req.context_hint:
        level = req.context_hint.get("level")
        stream = req.context_hint.get("stream")
        subject = req.context_hint.get("subject")
        res_type = req.context_hint.get("resource_type", "lessons")
        
        if level and stream and subject:
            try:
                url = EXAMDZ_SECONDARY.get(level, {}).get(stream, {}).get(subject, {}).get(res_type)
                if url:
                    context_from_web = f"\n[محتوى مسحوب من ExamDZ ({res_type}):]\n" + _fetch_web_content(url)
            except Exception as e:
                logger.warning(f"Context fetch error: {e}")

    final_prompt = GOLDEN_PROMPT.replace("{context_from_web}", context_from_web)
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
            return ChatResponse(reply=_call_gemini(contents))
        except Exception as e: logger.error(f"Gemini failed: {e}")

    raise HTTPException(status_code=502, detail="الخوادم مشغولة حالياً.")

@app.get("/")
def root(): return {"app": "OustadDz", "status": "running"}

@app.get("/health")
def health(): return {"status": "ok"}

@app.head("/health")
async def health_head(): return {}
