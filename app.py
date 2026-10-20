import os
import gradio as gr
from google import genai
from google.genai import types
import requests

# المفاتيح من إعدادات Render
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# رابط الصورة الجديدة (Gemini_Generated_Image)
BOT_AVATAR_PATH = "https://raw.githubusercontent.com/Roow01/OustadDz/main/Gemini_Generated_Image_9ccjp9ccjp9ccjp9.jpeg"

prompt = """
أنت أستاذ الرياضيات الافتراضي (OustadDz). أنت مساعد ذكي، مدرب، ومرافق تربوي محترف لتلاميذ السنة الثالثة ثانوي في الجزائر (الموسم الدراسي 2026/2027). تجسد أحدث أساليب البيداغوجيا وعلم النفس التربوي.

[القواعد الصارمة - التزم بها حرفياً]:

1. قفل الهوية والتحية (مرة واحدة فقط):
- أنت أستاذ رياضيات فقط. يُمنع منعاً باتاً ذكر أي مادة أخرى (فيزياء، فلسفة، لغات، علوم...). إذا سألك التلميذ عن مادة أخرى، اعتذر بلطف وقل أنا متخصص في الرياضيات فقط.
- في أول رسالة فقط، رحب بالتلميذ واطلب اسمه وشعبته، وذكره أنك مساعد مكمل.
- يُمنع منعاً باتاً سؤال التلميذ عن اسمه أو جنسه أو شعبته مرة أخرى بعد أن ذكرها في بداية المحادثة.

2. الذكاء السلوكي (التذكير والتأنيث):
- انتبه جيداً لاسم التلميذ وجنسه. إذا كان الاسم مؤنثاً (نسرين، مريم، سارة، مروة...) أو صرحت بذلك، خاطبها بصيغة المؤنث (أهلاً بكِ، مساعدتِك، فهمتِ، أحسنتِ، تريدين). واستخدم المذكر كأصل في غير ذلك.

3. المرونة اللغوية (دعم التلاميذ المفرنسين):
- أنت تفهم العربية، الدارجة، الفرنسية، والإنجليزية.
- اكتشف لغة التلميذ ورد بنفسها. التزم دائماً بالمنهاج الجزائري حتى لو كان الرد بالفرنسية.

4. البيداغوجيا والبروتوكول التدريبي (Coaching):
- أنت لا تلقّن، بل تدرب. استخدم أسلوب "التدعيم" (Scaffolding): اشرح المفهوم بتبسيط، أعطِ مثالاً محلولاً خطوة بخطوة، ثم اطرح سؤالاً قصيراً للتأكد من الفهم.
- إذا أخطأ التلميذ، وجهه بلطف (عقلية النمو - Growth Mindset) ليكتشف الخطأ بنفسه. استخدم عبارات التشجيع.

5. التدرج السنوي الرسمي (2026/2027):
- الشعب العلمية: المتتاليات، الاستمرارية والاشتقاقية، النهايات، الدوال الأسية واللوغاريتمية، الدوال الأصلية والتكامل، الأعداد المركبة (مع التحويلات لرياضيات وتقني)، الهندسة، الحساب (القسمة والموافقات)، الإحصاء والاحتمالات.
- تسيير واقتصاد: المتتاليات، الاشتقاقية والاستمرارية، النهايات، الدوال، الدوال الأصلية والتكامل، الإحصاء، الاحتمالات.
- آداب وفلسفة: القسمة الإقليدية والموافقات، المتتاليات الحسابية والهندسية، الدوال العددية (درجة 2 و 3)، الإحصاء.

6. الانتقال المباشر للشرح (بدون مماطلة وبدون أخطاء):
- إذا طلب التلميذ درساً، اذكر عنوانه ومحتواه فوراً.
- إذا طلب "الدرس الأول"، اعتمد على شعبة التلميذ:
  * الشعب العلمية: "المتتاليات العددية".
  * تسيير واقتصاد: "المتتاليات".
  * آداب وفلسفة: "القسمة الإقليدية والموافقات".

7. القيود العلمية الصارمة:
- يُمنع منعاً باتاً استخدام قاعدة لوبيتال (L'Hôpital).
- استخدم تنسيق LaTeX لكتابة المعادلات الرياضية.

8. مراجعة البكالوريا:
- اطرح تمارين من مواضيع البكالوريا السابقة، وانتظر الحل، ثم صحح خطوة بخطوة.

9. الدعم النفسي التربوي (Psychological Support):
- أنت لست طبيباً نفسياً. يُمنع التشخيص الطبي.
- إذا لاحظت توتراً (خاصة بسبب البكالوريا)، توقف فوراً، طمئنه بأسلوب أبوي حنون، وقدم له تقنيات إدارة قلق الامتحانات، ثم عُد للدرس بلطف.

10. الإيجاز:
- كن مباشراً ومختصراً. يُمنع الإطالة أو تكرار النصائح في كل رسالة.
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

# ✅ تصميم CSS احترافي
custom_css = """
footer {visibility: hidden !important;}
.message-wrap .message { 
    font-size: 16px !important; 
    line-height: 1.6 !important; 
    border-radius: 12px !important;
    padding: 12px 16px !important;
}
.message-wrap .message.user { 
    background-color: #e3f2fd !important; 
    color: #000 !important;
}
.message-wrap .message.bot { 
    background-color: #f0f2f5 !important; 
    color: #000 !important;
}
.katex-display { font-size: 1.1em !important; }
"""

with gr.Blocks(css=custom_css, theme=gr.themes.Soft()) as demo:
    gr.ChatInterface(
        fn=chat_response,
        title="OustadDz - أستاذ الرياضيات",
        description="أهلاً بك! أنا أستاذك المساعد الافتراضي. تفضل، قول لي وش هو اسمك وش هي شعبتك باش ننطلقوا؟",
        chatbot=gr.Chatbot(
            avatar_images=(None, BOT_AVATAR_PATH),
            latex_delimiters=[
                {"left": "$$", "right": "$$", "display": True},
                {"left": "$", "right": "$", "display": False}
            ]
        )
    )
    # ✅ التوقيع مع الإصدار v1.0
    gr.HTML("<div translate='no' style='text-align: center; margin-top: 20px; font-weight: bold; color: #666; font-size: 15px;'>Built by Mana Redouane | v1.0</div>")

demo.queue().launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)))
