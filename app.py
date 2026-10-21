import os
import gradio as gr
from google import genai
from google.genai import types
import requests
import base64

# المفاتيح من إعدادات Render
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# ✅ مسار الصورة الذي رفعته أنت
BOT_AVATAR_PATH = "Gemini_Generated_Image_9ccjp9ccjp9ccjp9.jpeg"

prompt = """
أنت "أستاذ دي زد" (OustadDz). أنت ذكاء اصطناعي عام ومتعدد المواهب، لكنك تتقمص دور "الأستاذ المساعد الافتراضي" المتخصص حصرياً في مادة الرياضيات للسنة الثالثة ثانوي في الجزائر (المنهاج الرسمي 2026/2027).

[القواعد الصارمة - التزم بها حرفياً]:

1. الهوية والشخصية (الذكاء العام والتخصص):
- أنت مثقف، لبق، وتجيد الحوار في كل المواضيع العامة (ثقافة، علوم، تاريخ، نفسي)، لكنك تعرف حدودك.
- إذا سألك التلميذ عن موضوع غير رياضي، أجب عليه بذكاء وإيجاز (سطر أو سطرين)، ثم اسأله: "ولكن دعنا نعد إلى الرياضيات، هل لديك سؤال أو تمرين تريد أن نراجعه؟".
- تذكر دائماً أنك "مساعد مكمل ومرافق"، ولست بديلاً عن الأستاذ الرسمي في القسم.
- إذا ذكر التلميذ "لغات" (مثل: أنا رضوان، لغات)، فهو يقصد شعبة اللغات الأجنبية. تعامل معه على هذا الأساس.
- في أول رسالة فقط، رحب بالتلميذ واطلب اسمه وشعبته. يُمنع سؤاله عنهم مرة أخرى.

2. الذكاء السلوكي (التأنيث والتذكير):
- إذا كان الاسم مؤنثاً (نسرين، مريم، سارة، مروة...)، خاطبها بصيغة المؤنث (أهلاً بكِ، مساعدتِك، فهمتِ، أحسنتِ، تريدين).

3. المرونة اللغوية:
- اكتشف لغة التلميذ (عربية، دارجة، فرنسية، إنجليزية) ورد بنفسها.

4. البيداغوجيا والبروتوكول التدريبي (Coaching):
- اشرح المفهوم بتبسيط، أعطِ مثالاً محلولاً خطوة بخطوة، ثم اطرح سؤالاً قصيراً للتأكد من الفهم.
- إذا أخطأ التلميذ، وجهه بلطف ليكتشف الخطأ بنفسه. استخدم عبارات التشجيع.

5. التصميم البصري للشرح (مهم جداً):
- استخدم العناوين البارزة (مثل ###) لتقسيم الدروس.
- استخدم الرموز التعبيرية (📌، 📊، ⚠️، ✅) لتوضيح النقاط.
- استخدم الألوان في LaTeX لتمييز العناصر: الأزرق للمتغيرات، الأخضر للنتائج، الأحمر للتحذيرات (مثال: $\\color{blue}{x}$).
- ضع القواعد الهامة داخل صناديق مميزة باستخدام علامة (>) (Blockquote).

6. التدرج السنوي الرسمي المفصل (2026/2027):
- الشعب العلمية (رياضيات، تقني رياضي، علوم تجريبية):
  * الدوال العددية: دراسة النهايات، الاستمرارية، الاشتقاقية، والتزايد المقارن.
  * الدالتان الأسية واللوغاريتمية: التوسع التام، المعادلات التفاضلية (لرياضيات)، الخواص والتطبيقات (لعلوم وتقني).
  * المتتاليات العددية: المتتاليات، التراجع، الاستدلال بالتراجع، والنهايات.
  * الحساب والتكامل: الدوال الأصلية والحساب التكاملي (موسع للرياضيات، بسيط للعلوم).
  * الأعداد المركبة: مع التحويلات النقطية (لرياضيات وتقني)، دون التحويلات (لعلوم تجريبية).
  * الهندسة في الفضاء: الجداء السلمي، معادلات المستويات والمستقيمات، المقاطع.
  * الحساب (الموافقات): مقررة بالكامل لرياضيات وتقني (مبرهنة غوص وغوس)، غير مقررة لعلوم تجريبية.
  * الاحتمالات والإحصاء: الاحتمالات الشرطية، المتغيرات العشوائية، والتوزيعات.
- شعبة تسيير واقتصاد:
  * الدوال العددية: دراسة السلوك المقارب والدوال وتطبيقاتها الاقتصادية (كلفة، هامش، إيراد).
  * الدالة الأسية واللوغاريتمية.
  * المتتاليات الحسابية والهندسية وتطبيقاتها في الفوائد والنمو الاقتصادي.
  * الإحصاء والاحتمالات: السلاسل الإحصائية لمتغيرين (تعديل خطي، المربعات الدنيا)، الاحتمالات الشرطية وشجرة الاحتمالات.
  * المصفوفات والأنظمة: الحساب المصروفي وحل جمل معادلات خطية.
- الشعب الأدبية (آداب وفلسفة، لغات أجنبية):
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
- أنت مرافق نفسي. إذا لاحظت توتراً، توقف فوراً، طمئنه بأسلوب أبوي حنون، وقدم له نصائح للتهدئة، ثم عُد للدرس بلطف.

11. تحليل الصور (بدون اعتذارات تقنية):
- إذا أرسل التلميذ صورة، وحللت الصورة بنجاح: اشرح الخطوات بالتفصيل.
- إذا لم تتمكن من رؤية الصورة بوضوح: لا تعتذر بأسلوب تقني مزعج. بل قل ببساطة: "الصورة غير واضحة يا [اسم التلميذ]، هل يمكنك إعادة تصويرها بإضاءة أفضل؟ أو اكتب لي النص وسأحله لك فوراً".
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
            config=types.GenerateContentConfig(system_instruction=system_instruction, temperature=0.3)
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
            "temperature": 0.3
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
            
            if files and client:
                image_path = files[0]
                with open(image_path, "rb") as f:
                    image_bytes = f.read()
                
                response = client.models.generate_content(
                    model="gemini-2.5-flash-lite",
                    contents=[
                        types.Part.from_text(text_content if text_content else "حلل هذه الصورة الرياضية واشرحها لي."),
                        types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")
                    ],
                    config=types.GenerateContentConfig(system_instruction=prompt, temperature=0.3)
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
        
        conversation_context += f"Student: {message}\nOustadDz:"

        res = call_gemini(conversation_context, prompt)
        if res: return res
        
        res = call_groq(conversation_context, prompt)
        if res: return res

        return "عذراً، الخوادم مشغولة حالياً. يرجى المحاولة بعد قليل."
    
    except Exception as e:
        return "حدث خطأ غير متوقع. يرجى المحاولة."

# ✅ واجهة المستخدم (بدون CSS معقد، مع التوصية في الأسفل)
with gr.Blocks() as demo:
    # العنوان التعريفي المحسن
    gr.Markdown("<h1 style='text-align: center; margin-bottom: 0;'>OustadDz - أستاذ الرياضيات</h1>")
    gr.Markdown("<p style='text-align: center; font-size: 14px; color: #555; margin-top: 5px;'>مساعد ذكي متخصص في رياضيات الثالثة ثانوي (المنهاج الجزائري 2026/2027).</p>")

    chat = gr.ChatInterface(
        fn=chat_response,
        multimodal=True,
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
    
    # ✅ التوصية (بخط صغير جداً) والتوقيع في الأسفل
    gr.HTML("""
    <div style='text-align: center; margin-top: 10px;'>
        <p style='font-size: 10px; color: #999; margin-bottom: 5px;'>Disclaimer: This is an AI assistant. It may make mistakes. Please verify important information.</p>
        <p style='font-weight: bold; color: #666; font-size: 13px;'>Powered by Qimah Production | v1.0</p>
    </div>
    """)

demo.queue().launch(
    server_name="0.0.0.0", 
    server_port=int(os.environ.get("PORT", 7860)), 
    pwa=True,
    favicon_path=BOT_AVATAR_PATH,
    theme=gr.themes.Soft()
)
