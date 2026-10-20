import os
import gradio as gr
from google import genai
from google.genai import types
import requests

# المفاتيح من إعدادات البيئة (Render / Environment Variables)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# اسم ملف الصورة المرفق مع المشروع
BOT_AVATAR_PATH = "Gemini_Generated_Image_9ccjp9ccjp9ccjp9.jpeg"

# التوجيه النظامي المشدد للأستاذ الافتراضي
prompt = """
أنت أستاذ الرياضيات الافتراضي (OustadDz). أنت مساعد ذكي، مدرب، ومرافق تربوي محترف لتلاميذ السنة الثالثة ثانوي في الجزائر (الموسم الدراسي 2026/2027).

[القواعد الصارمة - التزم بها حرفياً]:

1. قفل الهوية والتحية (مرة واحدة فقط):
- أنت أستاذ رياضيات فقط. يُمنع منعاً باتاً ذكر أي مادة أخرى (فيزياء، فلسفة). إذا سألك التلميذ عن مادة أخرى، اعتذر بلطف وقل أنا متخصص في الرياضيات فقط.
- ملاحظة هامة جداً: إذا ذكر التلميذ كلمة "لغات" (مثل "أنا رضوان، لغات")، فهو يقصد شعبة اللغات الأجنبية (وهي شعبة دراسية)، وليس مادة اللغة. تعامل معه على أنه تلميذ في شعبة لغات أجنبية وقدم له الرياضيات الخاصة بشعبته.
- في أول رسالة فقط، رحب بالتلميذ واطلب اسمه وشعبته.
- يُمنع منعاً باتاً سؤال التلميذ عن اسمه أو جنسه أو شعبته مرة أخرى.

2. الذكاء السلوكي (التذكير والتأنيث):
- إذا كان الاسم مؤنثاً (نسرين، مريم، سارة، مروة...) أو صرحت بذلك، خاطبها بصيغة المؤنث (أهلاً بكِ، مساعدتِك، فهمتِ، أحسنتِ، تريدين).

3. المرونة اللغوية:
- اكتشف لغة التلميذ (عربية، دارجة، فرنسية، إنجليزية) ورد بنفسها.

4. البيداغوجيا والبروتوكول التدريبي (Coaching):
- اشرح المفهوم بتبسيط، أعطِ مثالاً محلولاً خطوة بخطوة، ثم اطرح سؤالاً قصيراً للتأكد من الفهم.
- إذا أخطأ التلميذ، وجهه بلطف ليكتشف الخطأ بنفسه.

5. التصميم البصري للشرح (مهم جداً):
- استخدم العناوين البارزة (مثل ###) لتقسيم الدروس.
- استخدم الرموز التعبيرية (📌، 📊، ⚠️، ✅) لتوضيح النقاط.
- ضع القواعد الهامة داخل صناديق مميزة باستخدام علامة (>) (Blockquote).

6. التدرج السنوي الرسمي المفصل (2026/2027):
- الشعب العلمية (رياضيات، تقني رياضي، علوم تجريبية): المتتاليات، الاستمرارية والاشتقاقية، النهايات، الدوال الأسية واللوغاريتمية، الدوال الأصلية والتكامل، الأعداد المركبة (مع التحويلات لرياضيات وتقني)، الهندسة، الحساب (القسمة والموافقات)، الإحصاء والاحتمالات.
- تسيير واقتصاد: الدوال، المتتاليات، الإحصاء، الاحتمالات، المصفوفات.
- آداب وفلسفة ولغات أجنبية: الموافقات، المتتاليات، الدوال (درجة 2 و 3)، الإحصاء.

7. الانتقال المباشر للشرح:
- إذا طلب التلميذ درساً، اذكر عنوانه ومحتواه فوراً.
- إذا طلب "الدرس الأول": (علمي: المتتاليات العددية) | (تسيير: المتتاليات) | (آداب/لغات: القسمة والموافقات).

8. القيود العلمية الصارمة:
- يُمنع منعاً باتاً استخدام قاعدة لوبيتال (L'Hôpital).
- استخدم تنسيق LaTeX لكتابة المعادلات الرياضية.

9. مراجعة البكالوريا:
- اطرح تمارين من مواضيع البكالوريا السابقة، وانتظر الحل، ثم صحح خطوة بخطوة.

10. الدعم النفسي التربوي:
- إذا لاحظت توتراً، توقف فوراً، طمئنه بأسلوب أبوي حنون، وقدم له نصائح للتهدئة.

11. تحليل الصور:
- إذا أرسل التلميذ صورة لتمرين، قم بتحليلها بعناية واشرح الخطوات بالتفصيل.
"""

# تهيئة العميل الخاص بـ Google GenAI
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
        return response.text if response.text else None
    except Exception:
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
    except Exception:
        return None

def chat_response(message, history):
    try:
        text_content = ""
        image_path = None

        # التعامل المرن مع نوع الرسالة (نص أم مرفق صورة)
        if isinstance(message, dict):
            text_content = message.get("text", "")
            files = message.get("files", [])
            if files:
                image_path = files[0]
        else:
            text_content = str(message)

        # تحليل الصور إذا أرفق التلميذ صورة لتمرين
        if image_path and client:
            try:
                with open(image_path, "rb") as f:
                    image_bytes = f.read()
                
                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=[
                        types.Part.from_text(text_content if text_content else "حلل هذه الصورة الرياضية واشرح خطوات الحل بالتفصيل."),
                        types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")
                    ],
                    config=types.GenerateContentConfig(system_instruction=prompt, temperature=0.2)
                )
                if response and response.text:
                    return response.text
            except Exception:
                pass

        if not history:
            return "أهلاً بك! أنا أستاذك المساعد الافتراضي في الرياضيات للثالثة ثانوي. تفضل، قول لي وش هو اسمك وش هي شعبتك باش ننطلقوا؟"

        # إعداد سياق المحادثة
        conversation_context = ""
        for item in history:
            if isinstance(item, (list, tuple)) and len(item) == 2:
                u, b = item
                if u: conversation_context += f"Student: {u}\n"
                if b: conversation_context += f"OustadDz: {b}\n"

        conversation_context += f"Student: {text_content}\nOustadDz:"

        # محاولة طلب الاستجابة من Gemini أولاً ثم Groq
        res = call_gemini(conversation_context, prompt)
        if res: return res
        
        res = call_groq(conversation_context, prompt)
        if res: return res

        return "عذراً، الخوادم مشغولة حالياً. يرجى المحاولة بعد قليل."
        
    except Exception:
        return "حدث خطأ غير متوقع. يرجى المحاولة لاحقاً."

# تنسيق CSS احترافي ومحسن لقراءة الشروح والمعادلات الرياضية على الهواتف
custom_css = """
footer {visibility: hidden !important;}
body, .gradio-container { background-color: #fcfcfc !important; font-family: 'Tajawal', sans-serif !important; }

/* توسيع المساحة واستغلال شاشة الهاتف */
.main { max-width: 1000px !important; margin: 0 auto !important; }
.message-wrap .message { 
    font-size: 16px !important; 
    line-height: 1.9 !important; 
    border-radius: 14px !important; 
    padding: 14px 18px !important; 
    margin-bottom: 12px !important; 
}
.message-wrap .message.user { 
    background-color: #e8f0fe !important; 
    color: #1a73e8 !important; 
    border: 1px solid #d2e3fc !important;
}
.message-wrap .message.bot { 
    background-color: #ffffff !important; 
    color: #202124 !important; 
    border: 1px solid #e0e0e0 !important; 
    box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
}

/* تنسيق معادلات LaTeX الرياضية لتظهر بشكل بارز ومقروء */
.katex-display { 
    font-size: 1.25em !important; 
    margin: 12px 0 !important; 
    overflow-x: auto !important;
    overflow-y: hidden !important;
    padding: 8px !important;
    background: #f8f9fa !important;
    border-radius: 8px !important;
    border-right: 3px solid #1a73e8 !important;
}

textarea { 
    border-radius: 12px !important; 
    border: 1.5px solid #cccccc !important; 
    font-size: 16px !important; 
}
"""

# التحقق من وجود صورة الأيقونة
avatar_img = BOT_AVATAR_PATH if os.path.exists(BOT_AVATAR_PATH) else None

with gr.Blocks(css=custom_css, title="OustadDz") as demo:
    chat = gr.ChatInterface(
        fn=chat_response,
        title="OustadDz - أستاذ الرياضيات",
        description="أهلاً بك! أنا أستاذك المساعد الافتراضي لمادة الرياضيات للسنة الثالثة ثانوي.",
        multimodal=True,
        textbox=gr.MultimodalTextbox(
            placeholder="اكتب سؤالك هنا أو أرفق صورة لتمرين...", 
            file_types=["image"]
        ),
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
    
    gr.HTML("<div translate='no' style='text-align: center; margin-top: 15px; font-weight: bold; color: #777; font-size: 14px;'>Powered by Qimah Production | v8.0</div>")

if __name__ == "__main__":
    demo.queue().launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 7860)),
        pwa=True,
        favicon_path=avatar_img,
        theme=gr.themes.Soft()
    )
