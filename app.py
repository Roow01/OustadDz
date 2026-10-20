import os
import gradio as gr
from google import genai
from google.genai import types
import requests
from pathlib import Path

# المفاتيح من إعدادات Render
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# رابط الصورة (Avatar)
BOT_AVATAR_PATH = "https://raw.githubusercontent.com/Roow01/OustadDz/main/Gemini_Generated_Image_9ccjp9ccjp9ccjp9.jpeg"

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
- **الشعب العلمية (رياضيات، تقني رياضي، علوم تجريبية):**
  * الدوال العددية: دراسة النهايات، الاستمرارية، الاشتقاقية، والتزايد المقارن.
  * الدالتان الأسية واللوغاريتمية: التوسع التام، المعادلات التفاضلية (لرياضيات)، الخواص والتطبيقات (لعلوم وتقني).
  * المتتاليات العددية: المتتاليات، التراجع، الاستدلال بالتراجع، والنهايات.
  * الحساب والتكامل: الدوال الأصلية والحساب التكاملي (موسع للرياضيات، بسيط للعلوم).
  * الأعداد المركبة: مع التحويلات النقطية (لرياضيات وتقني)، دون التحويلات (لعلوم تجريبية).
  * الهندسة في الفضاء: الجداء السلمي، معادلات المستويات والمستقيمات، المقاطع.
  * الحساب (الموافقات): مقررة بالكامل لرياضيات وتقني (مبرهنة غوص وغوس)، غير مقررة لعلوم تجريبية.
  * الاحتمالات والإحصاء: الاحتمالات الشرطية، المتغيرات العشوائية، والتوزيعات.
- **شعبة تسيير واقتصاد:**
  * الدوال العددية: دراسة السلوك المقارب والدوال وتطبيقاتها الاقتصادية (كلفة، هامش، إيراد).
  * الدالة الأسية واللوغاريتمية.
  * المتتاليات الحسابية والهندسية وتطبيقاتها في الفوائد والنمو الاقتصادي.
  * الإحصاء والاحتمالات: السلاسل الإحصائية لمتغيرين (تعديل خطي، المربعات الدنيا)، الاحتمالات الشرطية وشجرة الاحتمالات.
  * المصفوفات والأنظمة: الحساب المصروفي وحل جمل معادلات خطية.
- **الشعب الأدبية (آداب وفلسفة، لغات أجنبية):**
  * القسمة الإقليدية والموافقات في Z: خصائص القسمة والموافقات بمدول n، تطبيق الموافقات في إيجاد بواقي القوى وتحديد أيام الأسبوع.
  * المتتاليات الحسابية والهندسية: تعريف، حدود، ومجموع.
  * الدوال العددية: دراسة دوال كثيرة الحدود من الدرجة الثانية والثالثة، قراءة المنحنيات وجداول التغيرات.

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

try:
    client = genai.Client(api_key=GEMINI_API_KEY)
except Exception as e:
    client = None

def call_gemini(contents, system_instruction):
    if not client: return None
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=contents,
            config=types.GenerateContentConfig(system_instruction=system_instruction, temperature=0.2)
        )
        return response.text if response.text else None
    except Exception as e:
        return None

def call_groq(contents, system_instruction):
    if not GROQ_API_KEY: return None
    try:
        headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
        data = {
            "model": "openai/gpt-oss-20b",
            "messages": [{"role": "system", "content": system_instruction}, {"role": "user", "content": contents}],
            "temperature": 0.2
        }
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data, timeout=15)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return None
    except Exception as e:
        return None

def chat_response(message, history):
    try:
        if isinstance(message, dict):
            text_content = message.get("text", "")
            files = message.get("files", [])
            
            if files:
                image_path = files[0]
                response = client.models.generate_content(
                    model="gemini-2.5-flash-lite",
                    contents=[
                        types.Part.from_text(text_content if text_content else "حلل هذه الصورة الرياضية واشرحها لي."),
                        types.Part.from_image(image_path)
                    ],
                    config=types.GenerateContentConfig(system_instruction=prompt, temperature=0.2)
                )
                return response.text if response.text else "عذراً، لم أتمكن من تحليل الصورة."
            else:
                message = text_content

        if len(history) == 0:
            welcome_msg = "أهلاً بك! أنا أستاذك المساعد الافتراضي في الرياضيات للثالثة ثانوي. تفضل، قول لي وش هو اسمك وش هي شعبتك باش ننطلقوا؟"
            return welcome_msg

        conversation_context = ""
        for item in history:
            if isinstance(item, dict):
                role = item.get("role", "user")
                content = item.get("content", "")
                if role == "user":
                    conversation_context += f"Student: {content}\n"
                elif role == "assistant":
                    conversation_context += f"OustadDz: {content}\n"
            elif isinstance(item, (list, tuple)) and len(item) == 2:
                user_msg, bot_msg = item
                conversation_context += f"Student: {user_msg}\nOustadDz: {bot_msg}\n"
        
        conversation_context += f"Student: {message}\nOustadDz:"

        res = call_gemini(conversation_context, prompt)
        if res: return res
        
        res = call_groq(conversation_context, prompt)
        if res: return res

        return "عذراً، الخوادم مشغولة حالياً. يرجى المحاولة بعد قليل."
    
    except Exception as e:
        return "حدث خطأ غير متوقع. يرجى المحاولة."

custom_css = """
footer {visibility: hidden !important;}
body, .gradio-container { background-color: #ffffff !important; }
.message-wrap .message { 
    font-size: 17px !important; 
    line-height: 1.8 !important; 
    border-radius: 16px !important;
    padding: 16px 20px !important;
    margin-bottom: 15px !important;
}
.message-wrap .message.user { 
    background-color: #e3f2fd !important; 
    color: #000 !important;
}
.message-wrap .message.bot { 
    background-color: #f7f7f7 !important; 
    color: #000 !important;
    border: 1px solid #e0e0e0 !important;
}
textarea {
    border-radius: 12px !important;
    border: 2px solid #d0d0d0 !important;
    padding: 15px !important;
    font-size: 16px !important;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05) !important;
}
.katex-display { font-size: 1.2em !important; margin: 15px 0 !important; }
"""

with gr.Blocks(css=custom_css, theme=gr.themes.Soft()) as demo:
    chat = gr.ChatInterface(
        fn=chat_response,
        title="OustadDz - أستاذ الرياضيات",
        description="أهلاً بك! أنا أستاذك المساعد الافتراضي. تفضل، قول لي وش هو اسمك وش هي شعبتك باش ننطلقوا؟",
        multimodal=True,
        type="messages",
        textbox=gr.MultimodalTextbox(placeholder="اكتب سؤالك أو أرفق صورة لتمرين...", file_types=["image"]),
        chatbot=gr.Chatbot(
            avatar_images=(None, BOT_AVATAR_PATH),
            latex_delimiters=[
                {"left": "$$", "right": "$$", "display": True},
                {"left": "$", "right": "$", "display": False}
            ]
        ),
        save_history=True
    )
    
    chat.saved_conversations.secret = "oustad_dz_secret_2026"
    chat.saved_conversations.storage_key = "_oustad_dz_saved_conversations"
    
    gr.HTML("<div translate='no' style='text-align: center; margin-top: 20px; font-weight: bold; color: #666; font-size: 15px;'>Powered by Qimah Production | v5.0</div>")

demo.queue().launch(
    server_name="0.0.0.0", 
    server_port=int(os.environ.get("PORT", 7860)), 
    pwa=True,
    favicon_path=BOT_AVATAR_PATH
)
