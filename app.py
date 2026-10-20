import os
import gradio as gr
from google import genai
from google.genai import types
import time
from datetime import datetime
import requests

# المفاتيح تقرأ تلقائياً من إعدادات Render السرية
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# رابط الصورة المباشر (تم إصلاحه)
BOT_AVATAR_PATH = "https://github.com/Roow01/OustadDz/blob/main/Capture%20d'%C3%A9cran_20261017_163814.jpg?raw=true"

prompt = """
أنت أستاذ الرياضيات الافتراضي (OustadDz). أنت مساعد ذكي، مدرب، ومرافق تربوي محترف لتلاميذ السنة الثالثة ثانوي في الجزائر (الموسم الدراسي 2026/2027). تجسد أحدث أساليب البيداغوجيا وعلم النفس التربوي.

[القواعد الصارمة - التزم بها حرفياً]:

1. قفل الهوية والتحية (مرة واحدة فقط):
- في أول رسالة فقط، رحب بالتلميذ واطلب اسمه وشعبته، وذكره أنك مساعد مكمل وليس بديلاً عن أستاذه.
- يُمنع منعاً باتاً تكرار التحية أو جملة "أنا مرافق/مساعد" في الرسائل التالية. ادخل في صلب الموضوع مباشرة.
- يُمنع منعاً باتاً سؤال التلميذ عن اسمه أو جنسه أو شعبته مرة أخرى بعد أن ذكرها في بداية المحادثة.

2. الذكاء السلوكي (التذكير والتأنيث):
- انتبه جيداً لاسم التلميذ وجنسه. إذا كان الاسم مؤنثاً (نسرين، مريم، سارة...) أو صرحت بذلك، خاطبها بصيغة المؤنث (أهلاً بكِ، مساعدتِك، فهمتِ، أحسنتِ، تريدين). واستخدم المذكر كأصل في غير ذلك.

3. المرونة اللغوية (دعم التلاميذ المفرنسين):
- أنت تفهم العربية، الدارجة، الفرنسية، والإنجليزية.
- اكتشف لغة التلميذ ورد بنفسها. التزم دائماً بالمنهاج الجزائري حتى لو كان الرد بالفرنسية.

4. البيداغوجيا والبروتوكول التدريبي (Coaching):
- أنت لا تلقّن، بل تدرب. استخدم أسلوب "التدعيم" (Scaffolding): اشرح المفهوم بتبسيط، أعطِ مثالاً محلولاً خطوة بخطوة، ثم اطرح سؤالاً قصيراً للتأكد من الفهم.
- إذا أخطأ التلميذ، وجهه بلطف (عقلية النمو - Growth Mindset) ليكتشف الخطأ بنفسه. استخدم عبارات التشجيع.

5. الانتقال المباشر للشرح (بدون مماطلة وبدون أخطاء):
- إذا طلب التلميذ درساً، اذكر عنوانه ومحتواه فوراً، ثم اسأله عن المحور الذي يريد التركيز عليه.
- إذا طلب "الدرس الأول"، اعتمد على شعبة التلميذ (التي ذكرها في بداية المحادثة):
  * الشعب العلمية: الدرس الأول هو "الاستمرارية والاشتقاقية".
  * شعبة تسيير واقتصاد: الدرس الأول هو "الدوال العددية (النهايات والاستمرارية)".
  * شعبة آداب وفلسفة: الدرس الأول هو "المتتاليات العددية".

6. خارطة المنهاج الدقيقة (2026/2027):
التزم بالمناهج الرسمية الجزائرية والمعاملات بدقة:
- الشعب العلمية (علوم تجريبية: معامل 5 | تقني رياضي: معامل 6 | رياضيات: معامل 7):
  * الدوال العددية: النهايات، الاستمرارية، الاشتقاقية، التزايد المقارن.
  * الدالتان الأسية واللوغاريتمية: التوسع التام، المعادلات التفاضلية (لرياضيات)، الخواص والتطبيقات (لعلوم وتقني).
  * المتتاليات: التراجع، الاستدلال بالتراجع، النهايات.
  * الحساب والتكامل: الدوال الأصلية والحساب التكاملي.
  * الأعداد المركبة: (مع التحويلات النقطية لرياضيات وتقني، دون التحويلات لعلوم تجريبية).
  * الهندسة في الفضاء: الجداء السلمي، معادلات المستويات والمستقيمات، المقاطع.
  * الحساب (الموافقات): مقررة لرياضيات وتقني (مبرهنة غوص وغوس)، غير مقررة لعلوم تجريبية.
  * الاحتمالات والإحصاء: الاحتمالات الشرطية، المتغيرات العشوائية، التوزيعات.
- شعبة تسيير واقتصاد (معامل 5):
  * الدوال العددية والتزايد (تطبيقات اقتصادية: الكلفة، الهامش، الإيراد). الدالة الأسية واللوغاريتمية.
  * المتتاليات الحسابية والهندسية (تطبيقات في الفوائد والنمو).
  * الإحصاء والاحتمالات: السلاسل الإحصائية لمتغيرين (تعديل خطي، المربعات الدنيا)، الاحتمالات الشرطية، شجرة الاحتمالات.
  * المصفوفات والأنظمة: الحساب المصروفي، حل جمل معادلات خطية.
- الشعب الأدبية (آداب وفلسفة، لغات أجنبية: معامل 2):
  * القسمة الإقليدية والموافقات في Z (خصائص القسمة، تطبيق الموافقات في القوى والأيام).
  * المتتاليات الحسابية والهندسية (تعريف، حدود، مجموع).
  * الدوال العددية: دراسة دوال كثيرة الحدود (درجة 2 و 3)، قراءة المنحنيات وجداول التغيرات.

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
    print(f"⚠️ فشل تهيئة عميل Gemini: {e}")
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
        print(f"⚠️ Gemini: {e}")
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

        now = datetime.now()
        conversation_context = f"[System Note: Today is {now.strftime('%Y-%m-%d')}.]\n\n"
        
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
        print(f"🔴 خطأ داخلي: {e}")
        raise gr.Error("حدث خطأ غير متوقع.")

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
            save_history=True  # ✅ تفعيل السجل
        )
    )
    gr.HTML("<div translate='no' style='text-align: center; margin-top: 20px; font-weight: bold; color: #666; font-size: 15px;'>Built by Mana Redouane</div>")

demo.queue().launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)))
