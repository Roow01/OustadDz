import os
import gradio as gr
from google import genai
from google.genai import types
import requests
import base64

# المفاتيح من إعدادات Render
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# ✅ مسار الصورة
BOT_AVATAR_PATH = "Gemini_Generated_Image_9ccjp9ccjp9ccjp9.jpeg"

prompt = """
أنت "أستاذ دي زد" (OustadDz). أنت ذكاء اصطناعي عام ومتعدد المواهب، لكنك تتقمص دور "الأستاذ المساعد الافتراضي" المتخصص حصرياً في مادة الرياضيات للسنة الثالثة ثانوي في الجزائر (المنهاج الرسمي 2026/2027).

[القواعد الصارمة - التزم بها حرفياً]:

1. الهوية والشخصية (الذكاء العام والتخصص):
- أنت مثقف، لبق، وتجيد الحوار في كل المواضيع العامة (ثقافة، علوم، تاريخ، نفسي)، لكنك تعرف حدودك.
- إذا سألك التلميذ عن موضوع غير رياضي، أجب عليه بذكاء وإيجاز (سطر أو سطرين)، ثم اسأله: "ولكن دعنا نعد إلى الرياضيات، هل لديك سؤال أو تمرين تريد أن نراجعه؟".
- تذكر دائماً أنك "مساعد مكمل ومرافق"، ولست بديلاً عن الأستاذ الرسمي في القسم.
- إذا ذكر التلميذ "لغات" (مثل: أنا رضوان، لغات)، فهو يقصد شعبة اللغات الأجنبية. تعامل معه على هذا الأساس.
- **مهم جداً**: **لا تسأل عن الاسم أو الشعبة مطلقاً**. اكتفِ بالترحيب وابدأ بالشرح مباشرة. إذا احتجت إليهما، اسأل بلطف في نهاية الرد.

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
- إذا لم تتمكن من رؤية الصورة بوضوح: لا تعتذر بأسلوب تقني مزعج. بل قل ببساطة: "الصورة غير واضحة يا صديقي، هل يمكنك إعادة تصويرها بإضاءة أفضل؟ أو اكتب لي النص وسأحله لك فوراً".

12. التقييم القبلي (Pre-assessment - مهم جداً):
- قبل شرح أي درس جديد أو حل أي تمرين معقد، قم بتقييم سريع لمستوى التلميذ.
- اطرح سؤالاً بسيطاً واحداً يتعلق بالمفهوم الأساسي (مثلاً: إذا سأل عن "الاشتقاق"، اسأله أولاً: "هل تعرف كيف نجد نهاية دالة؟" أو "هل تفهم معنى الميل؟").
- إذا أجاب التلميذ بشكل صحيح، انتقل مباشرة للشرح.
- إذا لم يجب أو أخطأ، قل له بلطف: "يبدو أننا نحتاج إلى مراجعة الأساسيات أولاً. دعنا نبدأ بـ [المفهوم الأساسي] ثم نعود إلى [الموضوع المطلوب]". هذا يضمن بناء تعليمي سليم.
"""

try:
    client = genai.Client(api_key=GEMINI_API_KEY)
except Exception as e:
    client = None

def call_gemini(contents, system_instruction):
    if not client: return None
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash", # ✅ flash لدعم الصور
            contents=contents,
            config=types.GenerateContentConfig(system_instruction=system_instruction, temperature=0.3)
        )
        return response.text if response.text else None
    except Exception as e:
        print(f"⚠️ Gemini Error: {e}")
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
            content_blocks = message.get("content", [])
            
            image_path = None
            for block in content_blocks:
                if isinstance(block, dict) and block.get("type") == "file":
                    image_path = block.get("file", {}).get("path")
                    break
            
            if image_path and client:
                with open(image_path, "rb") as f:
                    image_bytes = f.read()
                
                # ✅ تحديد mime_type الصحيح
                mime_type = "image/jpeg"
                if image_path.lower().endswith(".png"):
                    mime_type = "image/png"
                elif image_path.lower().endswith(".webp"):
                    mime_type = "image/webp"
                
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[
                        types.Part.from_text(text_content if text_content else "حلل هذه الصورة الرياضية واشرحها لي."),
                        types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
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
                if isinstance(content, list):
                    text_part = ""
                    for block in content:
                        if isinstance(block, dict) and block.get("type") == "text":
                            text_part += block.get("text", "")
                    content = text_part
                
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

custom_css = """
footer {visibility: hidden !important;}
"""

with gr.Blocks(css=custom_css) as demo:
    gr.Markdown("<h1 style='text-align: center; margin-bottom: 0;'>OustadDz - أستاذ الرياضيات</h1>")
    gr.Markdown("<p style='text-align: center; font-size: 16px; color: #444; margin-top: 5px;'>مساعدك الذكي في الرياضيات.</p>")

    chat = gr.ChatInterface(
        fn=chat_response,
        multimodal=True,
        textbox=gr.MultimodalTextbox(placeholder="اكتب سؤالك أو أرفق صورة لتمرين...", file_types=["image"]),
        chatbot=gr.Chatbot(
            avatar_images=(None, BOT_AVATAR_PATH),
            height=500,
            latex_delimiters=[
                {"left": "$$", "right": "$$", "display": True},
                {"left": "$", "right": "$", "display": False}
            ]
        ),
        save_history=True
    )
    
    chat.saved_conversations.secret = "oustad_dz_secret_2026"
    chat.saved_conversations.storage_key = "_oustad_dz_saved_conversations"
    
    gr.HTML("""
    <div translate="no" style='text-align: center; margin-top: 15px;'>
        <p style='font-size: 12px; color: #888; margin-bottom: 5px;'>This is an AI assistant. It may make mistakes.</p>
        <p style='font-weight: bold; color: #666; font-size: 14px;'>Powered by Qimah Production | v1.0</p>
    </div>
    """)

demo.queue().launch(
    server_name="0.0.0.0", 
    server_port=int(os.environ.get("PORT", 7860)), 
    pwa=True,
    favicon_path=BOT_AVATAR_PATH,
    theme=gr.themes.Soft()
)
