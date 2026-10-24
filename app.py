# =========================================================
# قاعدة البيانات الشاملة للطور الثانوي الجزائري (1AS, 2AS, 3AS)
# =========================================================

CURRICULUM_DATA = {
    "1AS": {
        "sciences": {
            "name": "جذع مشترك علوم وتكنولوجيا",
            "subjects": {
                "physics": {
                    "content": "بنية وهندسة أفراد بعض الأنواع الكيميائية، القوة والحركات، المول والتركيز، الظواهر الضوئية.",
                    "distribution": ["الوحدة 1: بنية وهندسة أفراد بعض الأنواع الكيميائية", "الوحدة 2: القوة والحركات المستقيمة", "الوحدة 3: القوة والحركات المنحنية", "الوحدة 4: الحركة والقوة والجاذبية", "الوحدة 5: من المجهري إلى العياني (المول والتركيز)", "الوحدة 6: انحفاظ الكتلة خلال تحول كيميائي", "الوحدة 7: الانكسار والضوء الأبيض"]
                },
                "math": {
                    "content": "الأعداد والحساب، الترتيب والمجالات، عموميات على الدوال، الدوال المرجعية، الهندسة المستوية، الحساب المثلثي.",
                    "distribution": ["المحور 1: الأعداد والحساب", "المحور 2: الترتيب والمجالات والحصر", "المحور 3: عموميات على الدوال", "المحور 4: الدوال المرجعية", "المحور 5: الهندسة المستوية والحساب الشعاعي", "المحور 6: معادلة مستقيم والجمل", "المحور 7: الإحصاء", "المحور 8: الحساب المثلثي والدائرة المثلثية"]
                },
                "sciences": {
                    "content": "استعمال المادة، تحويل الطاقة، إنتاج الكتلة الحيوية، التنسيق العصبي الهرموني.",
                    "distribution": ["المجال 1: استعمال المادة وتحديد مصدرها", "المجال 2: تحويل الطاقة الكيميائية الكامنة", "المجال 3: دخول الطاقة الضوئية (التركيب الضوئي)", "المجال 4: العوامل المؤثرة على إنتاج الكتلة الحيوية", "المجال 5: التنسيق الوظيفي العصبي الهرموني"]
                },
                "arabic": {"content": "اللغة العربية وآدابها (الجاهلي، صدر الإسلام، الأموي).", "distribution": ["الأدب الجاهلي", "صدر الإسلام", "العصر الأموي"]},
                "french": {"content": "Vulgarisation scientifique, L'interview.", "distribution": ["La vulgarisation scientifique", "L'interview"]},
                "english": {"content": "Getting Through, Once upon a time.", "distribution": ["Getting Through", "Once upon a time"]},
                "history": {"content": "التاريخ والجغرافيا: العالم الإسلامي، أدوات الجغرافيا.", "distribution": ["العالم الإسلامي", "أدوات الجغرافيا والبيئات"]},
                "islamic": {"content": "العلوم الإسلامية: عقيدة التوحيد، القرآن والحديث.", "distribution": ["عقيدة التوحيد", "القرآن والحديث"]}
            }
        },
        "lettres": {
            "name": "جذع مشترك آداب",
            "subjects": {
                "arabic": {"content": "عصر الجاهلية، عصر صدر الإسلام، العصر الأموي.", "distribution": ["العصر الجاهلي (الشعر، المعلقات، النثر)", "عصر صدر الإسلام (أثر العقيدة في الأدب)", "العصر الأموي (شعر السياسة والغزل)"]},
                "history": {"content": "الخلافة العثمانية، العلاقات الدولية للجزائر، البيئة والنظم البيئية.", "distribution": ["الخلافة العثمانية", "العلاقات الدولية للجزائر", "مفهوم البيئة والنظم البيئية"]},
                "french": {"content": "Le fait divers, L'interview, La nouvelle réaliste.", "distribution": ["Le fait divers", "L'interview", "La nouvelle réaliste"]},
                "english": {"content": "Interviews, Fables and tales, Report writing.", "distribution": ["Interviews", "Fables and tales", "Report writing"]},
                "math": {"content": "الرياضيات الأدبية.", "distribution": ["النسب المئوية والمؤشرات", "العبارات الجبرية والمعادلات", "الإحصاء"]},
                "sciences": {"content": "علوم الطبيعة والحياة.", "distribution": ["المنعكسات العضلية", "التنظيم العصبي للقلب والتنفس"]},
                "islamic": {"content": "العلوم الإسلامية.", "distribution": ["الأخلاق والعبادات الإسلامية"]}
            }
        }
    },
    "2AS": {
        "sciences": {
            "name": "شعبة علوم تجريبية",
            "subjects": {
                "sciences": {"content": "التنظيم العصبي والهرموني، الانقسام المنصف، بنية ADN، جيولوجيا.", "distribution": ["الوحدة 1: التنظيم العصبي", "الوحدة 2: التنظيم الهرموني", "الوحدة 3: التنسيق العصبي الهرموني", "الوحدة 4: الانقسام المنصف والإلقاح", "الوحدة 5: بنية الـ ADN", "الوحدة 6: الطفرات الوراثية", "الوحدة 7: حركية الصفائح"]},
                "physics": {"content": "طاقة جملة، العمل والطاقة، الناقلية، كيمياء عضوية، مغناطيسية، عدسات.", "distribution": ["الوحدة 1: طاقة جملة وانحفاظها", "الوحدة 2: العمل والطاقة الحركية", "الوحدة 3: الطاقة الكامنة", "الوحدة 4: الطاقة الداخلية", "الوحدة 5: قياس الناقلية", "الوحدة 6: المعايرة", "الوحدة 7: الكيمياء العضوية", "الوحدة 8: المغناطيسية", "الوحدة 9: العدسات"]},
                "math": {"content": "عموميات الدوال، كثيرات الحدود، الاشتقاقية، المتتاليات، المرجح، الجداء السلمي، الإحصاء.", "distribution": ["المحور 1: عموميات وتركيب الدوال", "المحور 2: كثيرات الحدود", "المحور 3: الاشتقاقية", "المحور 4: المتتاليات", "المحور 5: المرجح", "المحور 6: الزوايا الموجهة", "المحور 7: الجداء السلمي", "المحور 8: الإحصاء والاحتمالات"]},
                "arabic": {"content": "الأدب العربي (العصر العباسي).", "distribution": ["الأدب العباسي والتجديد", "شعر الزهد والتصوف"]},
                "french": {"content": "Le discours exhortatif.", "distribution": ["Le discours exhortatif", "Le plaidoyer"]},
                "english": {"content": "Make peace, Waste not.", "distribution": ["Make peace", "Waste not, want not"]},
                "history": {"content": "الاستعمار، الحركة الوطنية، الجزائر إقليميا.", "distribution": ["الاستعمار الحديث", "الحركة الوطنية", "الجزائر إقليميا"]},
                "islamic": {"content": "حقوق الإنسان، مصادر التشريع.", "distribution": ["حقوق الإنسان", "مصادر التشريع"]},
                "philosophy": {"content": "المشكلة العلمية والإشكالية.", "distribution": ["مدخل إلى الفلسفة", "المشكلة العلمية والإشكالية"]}
            }
        },
        "math": {
            "name": "شعبة الرياضيات",
            "subjects": {
                "math": {"content": "الاشتقاقية، دراسة الدوال، المتتاليات، الحساب المثلثي، الهندسة الفضائية.", "distribution": ["الاشتقاقية وتطبيقاتها", "دراسة الدوال", "المتتاليات العددية", "الحساب المثلثي", "الهندسة الفضائية والاحتمالات"]},
                "physics": {"content": "الطاقة، الناقلية، الأحماض والقواعد، المغناطيسية.", "distribution": ["الطاقة الحركية والكامنة", "الناقلية", "الأحماض والقواعد", "الظواهر المغناطيسية"]},
                "informatics": {"content": "الخوارزميات، البرمجة.", "distribution": ["الخوارزميات", "البرمجة بلغة بايثون", "معالجة البيانات"]}
            }
        },
        "tech": {
            "name": "تقني رياضي",
            "subjects": {
                "math": {"content": "الاشتقاقية، دراسة الدوال، المتتاليات، الحساب المثلثي.", "distribution": ["الاشتقاقية", "دراسة الدوال", "المتتاليات", "الحساب المثلثي"]},
                "physics": {"content": "الطاقة، الناقلية، الأحماض والقواعد.", "distribution": ["الطاقة", "الناقلية", "الأحماض والقواعد"]},
                "technology": {"content": "تكنولوجيا التخصص.", "distribution": ["أساسيات التخصص", "التطبيقات", "المشاريع"]}
            }
        },
        "gestion": {
            "name": "تسيير واقتصاد",
            "subjects": {
                "economics": {"content": "المحاسبة، الاقتصاد، التسيير.", "distribution": ["المحاسبة والتسيير المالي", "الاقتصاد والاجتماع", "اللوجستيك"]},
                "math": {"content": "الدوال، الإحصاء.", "distribution": ["الدوال", "الإحصاء", "المتتاليات"]},
                "law": {"content": "القانون المدني والتجاري.", "distribution": ["القانون المدني", "القانون التجاري"]}
            }
        },
        "lettres": {
            "name": "آداب وفلسفة",
            "subjects": {
                "philosophy": {"content": "نشأة الفلسفة، السؤال العلمي.", "distribution": ["نشأة الفلسفة", "السؤال العلمي والفلسفي", "الفكر واللغة"]},
                "arabic": {"content": "الأدب الحديث، المقالة.", "distribution": ["الأدب العربي الحديث", "المقالة", "البلاغة"]},
                "history": {"content": "الثورة الجزائرية، الحرب العالمية.", "distribution": ["الثورة الجزائرية", "الحرب العالمية الثانية", "النظام الدولي"]}
            }
        },
        "langues": {
            "name": "لغات أجنبية",
            "subjects": {
                "french": {"content": "Textes, grammaire.", "distribution": ["Textes", "Grammaire", "Dissertation"]},
                "english": {"content": "Texts, grammar, essay.", "distribution": ["Texts", "Grammar", "Essay writing"]},
                "spanish": {"content": "Textos, gramática.", "distribution": ["Textos", "Gramática", "Conversación"]},
                "german": {"content": "Texte, Grammatik.", "distribution": ["Texte", "Grammatik", "Konversation"]}
            }
        }
    },
    "3AS": {
        "sciences": {
            "name": "شعبة علوم تجريبية",
            "subjects": {
                "physics": {"content": "المتابعة الزمنية، التحولات النووية، الكهرباء، التوازن، الميكانيك، الموجات.", "distribution": ["الوحدة 1: المتابعة الزمنية لتحول كيميائي", "الوحدة 2: دراسة تحولات نووية", "الوحدة 3: دراسة ظواهر كهربائية (RC , RL)", "الوحدة 4: تطور جملة كيميائية نحو حالة التوازن", "الوحدة 5: تطور جملة ميكانيكية", "الوحدة 6: مراقبة تطور جملة كيميائية", "الوحدة 7: التطورات المهتزة", "الوحدة 8: مفهوم الموجة"]},
                "sciences": {"content": "التخصص الوظيفي للبروتينات، تحويل الطاقة، الجيولوجيا.", "distribution": ["الوحدة 1: آليات تركيب البروتين", "الوحدة 2: العلاقة بين بنية ووظيفة البروتين", "الوحدة 3: النشاط الإنزيمي", "الوحدة 4: الدفاع عن الذات (المناعة)", "الوحدة 5: الاتصال العصبي", "المجال 2: تحويل الطاقة", "المجال 3: التكتونية العامة"]},
                "math": {"content": "الاستمرارية، الدوال الأسية واللوغاريتمية، المتتاليات، التكامل، الاحتمالات، الأعداد المركبة.", "distribution": ["المحور 1: الاستمرارية والاشتقاقية والنهايات", "المحور 2: الدوال الأسية واللوغاريتمية", "المحور 3: التزايد المقارن", "المحور 4: المتتاليات العددية", "المحور 5: الحساب التكاملي", "المحور 6: الاحتمالات", "المحور 7: الأعداد المركبة", "المحور 8: الهندسة في الفضاء"]},
                "arabic": {"content": "الانحطاط، النهضة والالتزام.", "distribution": ["شعر المديح", "مدرسة الإحياء", "الشعر السياسي", "النثر الحديث"]},
                "philosophy": {"content": "المشكلة والإشكالية، فلسفة العلوم.", "distribution": ["المشكلة والإشكالية", "فلسفة العلوم", "العلاقات الإنسانية"]},
                "french": {"content": "Le texte historique, L'appel.", "distribution": ["Le texte historique", "L'appel", "Le débat d'idées"]},
                "english": {"content": "Ancient Civilizations, Ethics.", "distribution": ["Ancient Civilizations", "Ethics in Business", "Safety First"]},
                "history": {"content": "الحرب الباردة، الثورة الجزائرية.", "distribution": ["الحرب الباردة", "الثورة الجزائرية", "القوى الاقتصادية الكبرى"]},
                "islamic": {"content": "العقل والقرآن، أحكام المال.", "distribution": ["العقل والقرآن", "أحكام المال والميراث", "مصادر التشريع"]}
            }
        },
        "math": {
            "name": "شعبة الرياضيات",
            "subjects": {
                "math": {"content": "النهايات، الاستمرارية، الاشتقاقية، التكامل، الأعداد المركبة، الموافقات.", "distribution": ["النهايات والاستمرارية والاشتقاقية", "التكامل والأعداد المركبة", "الموافقات والاحتمالات"]},
                "physics": {"content": "المتابعة الزمنية، الكهرباء، الميكانيك.", "distribution": ["المتابعة الزمنية", "الكهرباء (RC, RL)", "الميكانيك"]},
                "informatics": {"content": "الخوارزميات، البرمجة.", "distribution": ["الخوارزميات", "البرمجة", "المشاريع"]}
            }
        },
        "tech": {
            "name": "تقني رياضي",
            "subjects": {
                "math": {"content": "النهايات، الاشتقاقية، التكامل، الأعداد المركبة.", "distribution": ["النهايات والاشتقاقية", "التكامل والأعداد المركبة", "الموافقات"]},
                "physics": {"content": "المتابعة الزمنية، الكهرباء، الميكانيك.", "distribution": ["المتابعة الزمنية", "الكهرباء", "الميكانيك"]},
                "technology": {"content": "تكنولوجيا التخصص.", "distribution": ["أساسيات", "تطبيقات", "مشاريع"]}
            }
        },
        "gestion": {
            "name": "تسيير واقتصاد",
            "subjects": {
                "economics": {"content": "المحاسبة، الاقتصاد الكلي، القانون.", "distribution": ["المحاسبة", "الاقتصاد الكلي", "القانون"]},
                "math": {"content": "الدوال، الإحصاء، المصفوفات.", "distribution": ["الدوال والمتتاليات", "الإحصاء والمصفوفات", "الاحتمالات"]},
                "law": {"content": "القانون التجاري والمدني.", "distribution": ["القانون التجاري", "القانون المدني"]}
            }
        },
        "lettres": {
            "name": "آداب وفلسفة",
            "subjects": {
                "philosophy": {"content": "إدراك العالم الخارجي، الأخلاق، فلسفة العلوم.", "distribution": ["إدراك العالم الخارجي", "الأخلاق", "فلسفة العلوم"]},
                "arabic": {"content": "عصر الضعف، عصر النهضة، المقالة النقدية.", "distribution": ["عصر الضعف", "عصر النهضة", "المقالة النقدية"]},
                "history": {"content": "الثورة الجزائرية، النظام الدولي.", "distribution": ["الثورة الجزائرية", "النظام الدولي", "القضايا المعاصرة"]}
            }
        },
        "langues": {
            "name": "لغات أجنبية",
            "subjects": {
                "french": {"content": "Textes, dissertation.", "distribution": ["Analyse", "Dissertation", "Commentaire"]},
                "english": {"content": "Literature, grammar, essay.", "distribution": ["Literature", "Grammar", "Essay"]},
                "spanish": {"content": "Textos, gramática.", "distribution": ["Textos", "Gramática", "Conversación"]},
                "german": {"content": "Texte, Grammatik.", "distribution": ["Texte", "Grammatik", "Konversation"]}
            }
        }
    }
}

# =========================================================
# استكمال المواد المشتركة لجميع الشعب (عربية، فرنسية، إنجليزية، تاريخ، إسلامية، فلسفة)
# =========================================================

common_2as = {
    "arabic": {"content": "الأدب العربي الحديث، المقالة.", "distribution": ["الأدب الحديث", "المقالة", "البلاغة"]},
    "french": {"content": "Textes, grammaire.", "distribution": ["Textes", "Grammaire", "Expression"]},
    "english": {"content": "Texts, grammar, writing.", "distribution": ["Texts", "Grammar", "Writing"]},
    "history": {"content": "الثورة الجزائرية، الحرب العالمية.", "distribution": ["الثورة الجزائرية", "الحرب العالمية", "النظام الدولي"]},
    "islamic": {"content": "القرآن، الحديث، الفقه.", "distribution": ["القرآن", "الحديث", "الفقه"]},
    "philosophy": {"content": "نشأة الفلسفة، السؤال العلمي.", "distribution": ["نشأة الفلسفة", "السؤال العلمي", "الفكر واللغة"]},
    "math": {"content": "الدوال، الإحصاء.", "distribution": ["الدوال", "الإحصاء", "المتتاليات"]},
    "physics": {"content": "الطاقة، الناقلية.", "distribution": ["الطاقة", "الناقلية", "الأحماض"]}
}

common_3as = {
    "arabic": {"content": "الأدب الجزائري، المقالة النقدية.", "distribution": ["الأدب الجزائري", "المقالة النقدية", "المراجعة"]},
    "french": {"content": "Analyse, dissertation.", "distribution": ["Analyse", "Dissertation", "Commentaire"]},
    "english": {"content": "Literature, grammar, essay.", "distribution": ["Literature", "Grammar", "Essay"]},
    "history": {"content": "الثورة الجزائرية، النظام الدولي.", "distribution": ["الثورة الجزائرية", "النظام الدولي", "القضايا المعاصرة"]},
    "islamic": {"content": "القرآن، الحديث، الفقه.", "distribution": ["القرآن", "الحديث", "الفقه"]},
    "philosophy": {"content": "المشكلة والإشكالية، فلسفة العلوم.", "distribution": ["المشكلة والإشكالية", "فلسفة العلوم", "العلاقات الإنسانية"]},
    "math": {"content": "الدوال، الإحصاء.", "distribution": ["الدوال", "الإحصاء", "المصفوفات"]},
    "physics": {"content": "المتابعة الزمنية، الكهرباء.", "distribution": ["المتابعة الزمنية", "الكهرباء", "الميكانيك"]}
}

# دمج المواد المشتركة في كل شعبة (2AS)
for stream in ["math", "tech", "gestion", "lettres", "langues"]:
    if stream in CURRICULUM_DATA["2AS"] and "subjects" in CURRICULUM_DATA["2AS"][stream]:
        for subj_key, subj_val in common_2as.items():
            if subj_key not in CURRICULUM_DATA["2AS"][stream]["subjects"]:
                CURRICULUM_DATA["2AS"][stream]["subjects"][subj_key] = subj_val

# دمج المواد المشتركة في كل شعبة (3AS)
for stream in ["math", "tech", "gestion", "lettres", "langues"]:
    if stream in CURRICULUM_DATA["3AS"] and "subjects" in CURRICULUM_DATA["3AS"][stream]:
        for subj_key, subj_val in common_3as.items():
            if subj_key not in CURRICULUM_DATA["3AS"][stream]["subjects"]:
                CURRICULUM_DATA["3AS"][stream]["subjects"][subj_key] = subj_val

# استكمال مواد شعبة الآداب (التي تنقصها الرياضيات والعلوم)
if "lettres" in CURRICULUM_DATA["2AS"]:
    CURRICULUM_DATA["2AS"]["lettres"]["subjects"]["math"] = common_2as["math"]
    CURRICULUM_DATA["2AS"]["lettres"]["subjects"]["islamic"] = common_2as["islamic"]
if "lettres" in CURRICULUM_DATA["3AS"]:
    CURRICULUM_DATA["3AS"]["lettres"]["subjects"]["math"] = common_3as["math"]
    CURRICULUM_DATA["3AS"]["lettres"]["subjects"]["islamic"] = common_3as["islamic"]

# استكمال مواد شعبة اللغات
if "langues" in CURRICULUM_DATA["2AS"]:
    CURRICULUM_DATA["2AS"]["langues"]["subjects"]["arabic"] = common_2as["arabic"]
    CURRICULUM_DATA["2AS"]["langues"]["subjects"]["history"] = common_2as["history"]
    CURRICULUM_DATA["2AS"]["langues"]["subjects"]["islamic"] = common_2as["islamic"]
    CURRICULUM_DATA["2AS"]["langues"]["subjects"]["philosophy"] = common_2as["philosophy"]
if "langues" in CURRICULUM_DATA["3AS"]:
    CURRICULUM_DATA["3AS"]["langues"]["subjects"]["arabic"] = common_3as["arabic"]
    CURRICULUM_DATA["3AS"]["langues"]["subjects"]["history"] = common_3as["history"]
    CURRICULUM_DATA["3AS"]["langues"]["subjects"]["islamic"] = common_3as["islamic"]
    CURRICULUM_DATA["3AS"]["langues"]["subjects"]["philosophy"] = common_3as["philosophy"]
