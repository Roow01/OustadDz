import os
import gradio as gr
from google import genai
from google.genai import types
import requests

# 🔑 المفاتيح من إعدادات البيئة (Environment Variables) في Render
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# 🖼️ مسار أيقونة الأستاذ الافتراضي
BOT_AVATAR_PATH = "Gemini_Generated_Image_9ccjp9ccjp9ccjp9.jpeg"

# 🧠 الـ Prompt المحترف والمدمج وفق التدرجات الرسمية الجزائريـة
PROMPT_SYSTEM = """
أنت أستاذ الرياضيات الافتراضي (OustadDz)، مساعد ذكي ومدرب تربوي محترف لتلاميذ السنة الثالثة ثانوي في الجزائر (الموسم الدراسي 2026/2027) المترشحين لشهادة البكالوريا.

---
### 📌 [الهوية والضوابط السلوكية]:
1. **قفل الهوية والتحية:**
   - أنت أستاذ رياضيات فقط. يُمنع منعاً باتاً التطرق لأي مادة أخرى (فيزياء، فلسفة، إلخ). عند السؤال عنها، اعتذر بلطف.
   - **تنبيه هام:** كلمة "لغات" تعني **شعبة اللغات الأجنبية** وليس مادة اللغات. قدم للشخص ما يناسب شعبته.
   - في أول رسالة فقط، رحب بالتلميذ واطلب اسمه وشعبته. يُمنع إعادة سؤال التلميذ عن اسمه أو شعبته لاحقاً.
2. **الذكاء السلوكي:** خاطب التلميذ(ة) بصيغة المؤنث إن كان الاسم مؤنثاً (مثل: نسرين، مريم...).
3. **المرونة اللغوية:** رد بنفس اللغة التي يعتمدها التلميذ (عربية، دارجة، فرنسية، إنجليزية).
4. **الدعم النفسي:** قدم الدعم والأمان النفسي للتلميذ عند التوتر لتخفيف ضغط البكالوريا.

---
### 📚 [المنهاج الرسمي والتدرجات السنوية 2026/2027]:

#### 1️⃣ مجموعة الشعب العلمية والتكنولوجية:
* **شعبة رياضيات (معامل 7):**
  - الدوال العددية (النهايات، الاستمرارية، الاشتقاقية، التزايد المقارن).
  - الدالتان الأسية واللوغاريتمية (معادلات تفاضلية والتزايد المقارن التام).
  - المتتاليات العددية (الاستدلال بالتراجع، النهايات).
  - الحساب والتكامل (الدوال الأصلية والتكامل الموسع).
  - الأعداد المركبة والتحويلات النقطية في المستوي.
  - الهندسة في الفضاء (الجداء السلمي، المستويات والمستقيمات، المقاطع).
  - الحساب: القسمة والموافقات في $\mathbb{Z}$، مبرهنة غوص وفيرما.
  - الاحتمالات الشرطية والمتغيرات العشوائية والتوزيعات.
* **شعبة تقني رياضي (معامل 6):** نفس برنامج العلوم مع التركيز التطبيقي والأعداد المركبة والتحويلات والقسمة والموافقات.
* **شعبة علوم تجريبية (معامل 5):**
  - نفس المحاور العلمية **مع استثناء**: القسمة والموافقات غير مقررة، والأعداد المركبة تكون **بدون** تحويلات نقطية عمقية.

#### 2️⃣ شعبة تسيير واقتصاد (معامل 5):
* الدوال العددية والتطبيقات الاقتصادية (الكلفة، الإيراد، الهامش) + الأسية واللوغاريتمية.
* المتتاليات العددية (الحسابية والهندسية وتطبيقات الفوائد والنمو).
* الإحصاء والاحتمالات (السلاسل الإحصائية بمتغيرين، التعديل الخطي بالمربعات الدنيا، والاحتمالات الشرطية).
* **المصفوفات والأنظمة:** الحساب المصروفي وحل جمل معادلات خطية.

#### 3️⃣ الشعب الأدبية (آداب وفلسفة + لغات أجنبية - معامل 2):
* **المحور 1:** القسمة الإقليدية والموافقات في $\mathbb{Z}$ (بواقي القوى، تحديد الأيام، والأنماط التكرارية).
* **المحور 2:** المتتاليات العددية (الحسابية والهندسية: التعريف، الحدود، المجموع).
* **المحور 3:** الدوال العددية (دوال كثيرات الحدود من الدرجة 2 و 3، قراءة المنحنيات واستخراج التغيرات).

---
### ⚠️ [القيود العلمية والبيداغوجية]:
1. **يُمنع منعاً باتاً** استخدام قاعدة **لوبيتال (L'Hôpital)** في حساب النهايات.
2. استخدام تنسيق **LaTeX** الحتمي لكتابة كافة المبرهنات والمعادلات والرموز الرياضية.
3. اعتماد أسلوب التدرج التدريبي (Coaching): شرح مبسط ⬅️ مثال محلول خطوة بخطوة ⬅️ سؤال تقويمي قصير.
4. **تحليل الصور:** عند استقبال صورة تمرين، قم بقراءتها بعناية واشرح خطوات الحل بالتفصيل والدقة.
"""

# 🛠️ تهيئة عميل Google GenAI
try:
    client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None
except Exception:
    client = None

def call_gemini(contents, system_instruction):
    if not client: return None
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=contents,
            config=types.GenerateContentConfig(system_instruction=system_instruction, temperature=0.2)
        )
        return response.text if response and response.text else None
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return None

def call_groq(contents, system_instruction):
    if not GROQ_API_KEY: return None
    try:
        headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
        data = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "system", "content": system_instruction}, {"role": "user", "content": contents}],
            "temperature": 0.2
        }
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data, timeout=15)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        return None
    except Exception as e:
        print(f"Groq API Error: {e}")
        return None

def chat_response(message, history):
    try:
        text_content = ""
        image_path = None

        # 📥 استخراج النص والصور بشكل آمن من Gradio Multimodal
        if isinstance(message, dict):
            text_content = message.get("text", "")
            files = message.get("files", [])
            if files:
                image_path = files[0]
        else:
            text_content = str(message)

        # 🖼️ معالجة الصور إن وجدت
        if image_path and client:
            try:
                if isinstance(image_path, str) and os.path.exists(image_path):
                    with open(image_path, "rb") as f:
                        image_bytes = f.read()
                else:
                    image_bytes = image_path.read() if hasattr(image_path, "read") else None

                if image_bytes:
                    response = client.models.generate_content(
                        model="gemini-1.5-flash",
                        contents=[
                            types.Part.from_text(text_content if text_content else "حلل هذه الصورة الرياضية واشرح خطوات الحل بالتفصيل."),
                            types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")
                        ],
                        config=types.GenerateContentConfig(system_instruction=PROMPT_SYSTEM, temperature=0.2)
                    )
                    if response and response.text:
                        return response.text
            except Exception as img_err:
                print(f"Image Error: {img_err}")

        # 💬 الترحيب في بداية المحادثة
        if not history:
            return "أهلاً بك! أنا أستاذك المساعد الافتراضي في الرياضيات للثالثة ثانوي. تفضل، قول لي وش هو اسمك وش هي شعبتك باش ننطلقوا؟"

        # 📝 بناء سياق الدردشة
        conversation_context = ""
        for item in history:
            if isinstance(item, (list, tuple)) and len(item) == 2:
                u, b = item
                if u: conversation_context += f"Student: {u}\n"
                if b: conversation_context += f"OustadDz: {b}\n"

        conversation_context += f"Student: {text_content}\nOustadDz:"

        # 🚀 طلب الإجابة من Gemini أولاً ثم Groq
        res = call_gemini(conversation_context, PROMPT_SYSTEM)
        if res: return res
        
        res = call_groq(conversation_context, PROMPT_SYSTEM)
        if res: return res

        return "عذراً، يرجى التأكد من إضافة مفاتيح GEMINI_API_KEY و GROQ_API_KEY في إعدادات البيئة (Environment Variables) لمنصة Render."
        
    except Exception as err:
        print(f"General Error: {err}")
        return "حدث خطأ غير متوقع أثناء معالجة الطلب."

# 🎨 تصميم CSS متجاوب مخصص لـ LaTeX وشاشات الهواتف
custom_css = """
footer {visibility: hidden !important;}
body, .gradio-container { background-color: #f8f9fa !important; font-family: 'Tajawal', sans-serif !important; }
.message-wrap .message { font-size: 16px !important; line-height: 1.8 !important; border-radius: 12px !important; padding: 14px 18px !important; margin-bottom: 10px !important; }
.message-wrap .message.user { background-color: #e3f2fd !important; color: #0d47a1 !important; }
.message-wrap .message.bot { background-color: #ffffff !important; color: #212121 !important; border: 1px solid #e0e0e0 !important; }
.katex-display { font-size: 1.25em !important; margin: 10px 0 !important; overflow-x: auto !important; background: #f1f3f4 !important; padding: 8px !important; border-radius: 6px !important; }
"""

avatar_img = BOT_AVATAR_PATH if os.path.exists(BOT_AVATAR_PATH) else None

with gr.Blocks(css=custom_css, title="OustadDz") as demo:
    chat = gr.ChatInterface(
        fn=chat_response,
        title="OustadDz - أستاذ الرياضيات",
        description="أهلاً بك! أنا أستاذك المساعد الافتراضي لمادة الرياضيات للسنة الثالثة ثانوي.",
        multimodal=True,
        textbox=gr.MultimodalTextbox(placeholder="اكتب سؤالك هنا أو أرفق صورة لتمرين...", file_types=["image"]),
        chatbot=gr.Chatbot(
            avatar_images=(None, avatar_img),
            latex_delimiters=[
                {"left": "$$", "right": "$$", "display": True},
                {"left": "$", "right": "$", "display": False}
            ]
        ),
        save_history=True
    )
    
    chat.saved_conversations.secret = "oustad_dz_secret_2026"
    chat.saved_conversations.storage_key = "_oustad_dz_saved_conversations"
    
    gr.HTML("<div translate='no' style='text-align: center; margin-top: 15px; font-weight: bold; color: #666; font-size: 14px;'>Powered by Qimah Production | v8.0</div>")

if __name__ == "__main__":
    demo.queue().launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 7860)),
        pwa=True,
        favicon_path=avatar_img,
        theme=gr.themes.Soft()
    )
