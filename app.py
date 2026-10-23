import os
import io
import base64
import json
import logging
import urllib.parse
import xml.etree.ElementTree as ET
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
# قاعدة بيانات الروابط (DzExams) - كاملة
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

# =========================================================
# دالة جلب الأخبار من Google News RSS
# =========================================================
def _get_latest_news(query: str = None, limit: int = 5) -> str:
    try:
        if query:
            url = f"https://news.google.com/rss/search?q={urllib.parse.quote(query)}&hl=ar&gl=DZ&ceid=DZ:ar"
        else:
            url = "https://news.google.com/rss?hl=ar&gl=DZ&ceid=DZ:ar"
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        root = ET.fromstring(response.content)
        items = root.findall('.//item')[:limit]
        
        news_list = []
        for item in items:
            title = item.find('title').text
            link = item.find('link').text
            pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ""
            news_list.append(f"- {title} ({pub_date})\n  {link}")
        
        return "\n".join(news_list) if news_list else "لا توجد أخبار حالياً."
    except Exception as e:
        logger.warning(f"News fetch failed: {e}")
        return "عذراً، لم أتمكن من جلب الأخبار حالياً."

# =========================================================
# البرومبت الذهبي (مع فصل المصادر + الأخبار)
# =========================================================
GOLDEN_PROMPT_TEMPLATE = """أنت "OustadDz"، نظام ذكاء اصطناعي فائق الذكاء (مثل ChatGPT). تتقن جميع اللغات والدارجة الجزائرية.

# 🎭 شخصياتك:
1. **الذكاء العام:** أجب عن أي سؤال عام بذكاء. إذا سألك المستخدم عن الأخبار، استخدم بيانات الأخبار المرفقة.
2. **الخبير التربوي:** أستاذ خبير في المنظومة التربوية الجزائرية (2026/2027).

# 🔄 آلية التحول:
- إذا سأل سؤالاً عاماً أو عن أخبار، أجب بذكاء (لا تطلب السنة أو الشعبة).
- إذا سأل سؤالاً دراسياً، اطلب توضيح (أستاذ أم تلميذ؟ السنة؟ الشعبة؟) قبل الإجابة.

# 📚 مصادر المعرفة (مهم جداً - لا تخلط بينها):
1. **المنهاج النظري (CURRICULUM_DATA):** استخدمه لشرح الدروس، المحاور، الأهداف، والتوزيع الفصلي. (هذا هو المصدر النظري).
2. **دليل الروابط (DzExams):** استخدمه فقط عندما يطلب المستخدم رابطاً (فروض، تمارين، كتب، بكالوريا). لا تعطه رابطاً لم يطلبه.
3. **الأخبار (News Context):** إذا سأل المستخدم عن الأخبار، استخدم البيانات المرفقة.

# 🧠 ميزات الأستاذ المدرب:
- **الكشف القبلي:** إذا لم يفهم الطالب، اسأله سؤالاً بسيطاً للتأكد من الأساسيات قبل الشرح.
- **التدريب (Coach):** دعم نفسي للتلاميذ، واقتراح مواضيع بكالوريا. مساعدة الأساتذة في بناء الفروض.

# 🎯 قواعد صارمة:
- **لا تخلط** بين المصادر. اذكر المصدر الذي استخدمته (مثلاً: "حسب المنهاج الرسمي...").
- إذا لم تكن متأكداً، قل: "هذه المعلومة تحتاج تحققاً".
- أجب في صلب الموضوع، بدون ثرثرة.
- استخدم لغة المستخدم.

# 📚 المنهاج النظري (CURRICULUM_DATA):
__CURRICULUM__

# 🔗 دليل الروابط (DzExams):
__EXAMDZ__

# 🧠 محتوى مسحوب من الإنترنت (Context):
__CONTEXT__

# 📰 الأخبار (News Context):
__NEWS__
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

    # 1. جلب الأخبار إذا طلب المستخدم ذلك
    news_context = ""
    news_keywords = ["أخبار", "خبر", "اليوم", "آخر", "news", "actualité", "dernières", "عاجل"]
    if any(kw in req.message.lower() for kw in news_keywords):
        news_context = _get_latest_news()

    # 2. جلب المحتوى من الروابط (إذا تم تمرير context_hint)
    context_from_web = ""
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

    # 3. استبدال العناصر النائبة
    final_prompt = GOLDEN_PROMPT_TEMPLATE.replace("__CURRICULUM__", curriculum_text)
    final_prompt = final_prompt.replace("__EXAMDZ__", examdz_text)
    final_prompt = final_prompt.replace("__CONTEXT__", context_from_web)
    final_prompt = final_prompt.replace("__NEWS__", news_context)
    
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
