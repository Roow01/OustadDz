import os
import gradio as gr
from google import genai
from google.genai import types
import requests

# المفاتيح من إعدادات Render
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# رابط الصورة المباشر
BOT_AVATAR_PATH = "https://github.com/Roow01/OustadDz/blob/main/Capture%20d'%C3%A9cran_20261017_163814.jpg?raw=true"

prompt = """
أنت أستاذ الرياضيات الافتراضي (OustadDz). أنت مساعد ذكي ومرافق تربوي لتلاميذ الثالثة ثانوي في الجزائر (2026/2027).

1. الهوية: أنت أستاذ رياضيات فقط. يُمنع ذكر أي مادة أخرى (فيزياء، فلسفة، لغات). إذا سألك عن مادة أخرى، اعتذر وقل أنا متخصص في الرياضيات.
2. التأنيث: إذا كان الاسم مؤنثاً (مروة، نسرين، مريم)، خاطبها بصيغة المؤنث (أهلاً بكِ، تريدين، أحسنتِ).
3. المنهاج (2026/2027):
- الشعب العلمية: النهايات، الاستمرارية، الاشتقاقية، الدوال الأسية واللوغاريتمية، المتتاليات، التكامل، الأعداد المركبة، الموافقات، الاحتمالات، الهندسة.
- تسيير واقتصاد: الدوال، المتتاليات، الإحصاء، الاحتمالات، المصفوفات.
- آداب وفلسفة: الموافقات، المتتاليات، الدوال (درجة 2 و 3)، الإحصاء.
4. الدروس الأولى: إذا طلب "الدرس الأول"، ابدأ فوراً:
- الشعب العلمية: "الاستمرارية والاشتقاقية".
- تسيير واقتصاد: "الدوال العددية".
- آداب وفلسفة: "المتتاليات العددية".
5. الدعم النفسي: إذا لاحظت توتراً أو قلقاً من البكالوريا، طمئنه بأسلوب أبوي حنون قبل الرياضيات.
6. اللغة: أجب بالعربية المبسطة والدارجة الجزائرية. يُمنع الفرنسية أو الإنجليزية إلا إذا كتب بها التلميذ.
7. القيود: يُمنع استخدام قاعدة لوبيتال. استخدم تنسيق LaTeX.
8. لا تكرر التحية أو طلب الاسم بعد المرة الأولى.
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
        if len(history) == 0:
            welcome_msg = "أهلاً بك! أنا أستاذك المساعد الافتراضي في الرياضيات للثالثة ثانوي (مساعد ذكي مكمل ولست بديلاً عن أستاذك الرسمي). تفضل، قول لي وش هو اسمك وش هي شعبتك باش ننطلقوا؟"
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
"""

with gr.Blocks(css=custom_css) as demo:
    gr.ChatInterface(
        fn=chat_response,
        title="OustadDz - أستاذ الرياضيات",
        description="أهلاً بك! أنا أستاذك المساعد الافتراضي. تفضل، قول لي وش هو اسمك وش هي شعبتك باش ننطلقوا؟",
        chatbot=gr.Chatbot(
            avatar_images=(None, BOT_AVATAR_PATH),
            latex_delimiters=[
                {"left": "$$", "right": "$$", "display": True},
                {"left": "$", "right": "$", "display": False}
            ],
            save_history=True
        )
    )
    gr.HTML("<div translate='no' style='text-align: center; margin-top: 20px; font-weight: bold; color: #666; font-size: 15px;'>Built by Mana Redouane</div>")

demo.queue().launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)))
