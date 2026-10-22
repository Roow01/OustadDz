# curriculum_data.py
# القاعدة المعرفية الشاملة والنهائية للبرنامج الرسمي الجزائري (2026/2027) - النسخة المصححة

CURRICULUM_DATA = {
    "1AS": {
        "sciences": {
            "name": "جذع مشترك علوم وتكنولوجيا",
            "subjects": {
                "arabic": {"content": "الأدب الجاهلي والإسلامي، البلاغة، القواعد والصرف، التعبير.", "hours_per_week": 5, "objectives": ["تعرف الأدب", "إتقان البلاغة"], "distribution": {"term1": "الأدب الجاهلي", "term2": "الأدب الإسلامي", "term3": "القواعد"}, "books": ["كتاب اللغة العربية 1AS"], "new_changes": "لا تغييرات"},
                "french": {"content": "Textes littéraires, grammaire, expression.", "hours_per_week": 4, "objectives": ["Maîtriser la lecture"], "distribution": {"term1": "Textes", "term2": "Grammaire", "term3": "Expression"}, "books": ["Livre de français 1AS"], "new_changes": "Renforcement"},
                "english": {"content": "Texts, grammar, conversation.", "hours_per_week": 2, "objectives": ["Enhance communication"], "distribution": {"term1": "Texts", "term2": "Grammar", "term3": "Writing"}, "books": ["English 1AS"], "new_changes": "Increased hours"},
                "islamic": {"content": "القرآن، الحديث، السيرة، الفقه.", "hours_per_week": 2, "objectives": ["فهم القيم الإسلامية"], "distribution": {"term1": "القرآن", "term2": "الحديث", "term3": "الفقه"}, "books": ["التربية الإسلامية 1AS"], "new_changes": "لا تغييرات"},
                "civic": {"content": "الحياة الديمقراطية، المؤسسات، الهوية الوطنية.", "hours_per_week": 1, "objectives": ["تعزيز الحس المدني"], "distribution": {"term1": "الحياة الديمقراطية", "term2": "المؤسسات", "term3": "الهوية"}, "books": ["التربية المدنية 1AS"], "new_changes": "مادة أساسية"},
                "math": {"content": "الأعداد، الدوال، الهندسة، الإحصاء.", "hours_per_week": 5, "objectives": ["إتقان الحساب", "تطوير التحليل"], "distribution": {"term1": "الأعداد والدوال", "term2": "الهندسة", "term3": "الإحصاء"}, "books": ["الرياضيات 1AS"], "new_changes": "لا تغييرات"},
                "physics": {"content": "مفهوم النوع الكيميائي، القوة والحركات، التحول الكيميائي.", "hours_per_week": 5, "objectives": ["فهم البنية الكيميائية", "تطبيق قوانين الحركة"], "distribution": {"term1": "النوع الكيميائي", "term2": "الحركات", "term3": "التحول الكيميائي"}, "books": ["الفيزياء 1AS"], "new_changes": "لا تغييرات"},
                "sciences": {"content": "التركيب الضوئي، التحويل الطاقوي، التحكم العصبي.", "hours_per_week": 4, "objectives": ["فهم آليات التركيب الضوئي"], "distribution": {"term1": "التركيب الضوئي", "term2": "التحويل الطاقوي", "term3": "التحكم العصبي"}, "books": ["العلوم 1AS"], "new_changes": "لا تغييرات"},
                "history": {"content": "العالم الإسلامي، أدوات جغرافية.", "hours_per_week": 2, "objectives": ["تعرف العالم الإسلامي"], "distribution": {"term1": "العالم الإسلامي", "term2": "الأدوات الجغرافية", "term3": "التكتلات"}, "books": ["التاريخ والجغرافيا 1AS"], "new_changes": "لا تغييرات"},
                "informatics": {"content": "مدخل إلى الإعلام الآلي، الخوارزميات البسيطة.", "hours_per_week": 1, "objectives": ["استخدام الحاسوب"], "distribution": {"term1": "مدخل", "term2": "الخوارزميات", "term3": "تطبيقات"}, "books": ["الإعلام الآلي 1AS"], "new_changes": "مادة أساسية"},
                "physical_education": {"content": "أنشطة رياضية.", "hours_per_week": 2, "objectives": ["تعزيز اللياقة"], "distribution": {"term1": "رياضات جماعية", "term2": "رياضات فردية", "term3": "اختبارات"}, "books": ["دليل التربية البدنية"], "new_changes": "لا تغييرات"},
                "arts": {"content": "الرسم، الموسيقى، المسرح.", "hours_per_week": 1, "objectives": ["تنمية الحس الفني"], "distribution": {"term1": "الرسم", "term2": "الموسيقى", "term3": "المسرح"}, "books": ["كتاب الفنون 1AS"], "new_changes": "لا تغييرات"}
            }
        },
        "lettres": {
            "name": "جذع مشترك آداب",
            "subjects": {
                "arabic": {"content": "الأدب الجاهلي والإسلامي، البلاغة، القواعد.", "hours_per_week": 6, "objectives": ["تعزيز الأدب", "إتقان التعبير"], "distribution": {"term1": "الأدب الجاهلي", "term2": "الأدب الإسلامي", "term3": "التعبير"}, "books": ["اللغة العربية 1AS"], "new_changes": "لا تغييرات"},
                "french": {"content": "Textes littéraires, grammaire, expression.", "hours_per_week": 4, "objectives": ["Maîtriser la lecture"], "distribution": {"term1": "Textes", "term2": "Grammaire", "term3": "Expression"}, "books": ["Français 1AS"], "new_changes": "Renforcement"},
                "english": {"content": "Texts, grammar, conversation.", "hours_per_week": 2, "objectives": ["Enhance communication"], "distribution": {"term1": "Texts", "term2": "Grammar", "term3": "Writing"}, "books": ["English 1AS"], "new_changes": "Increased hours"},
                "islamic": {"content": "القرآن، الحديث، السيرة، الفقه.", "hours_per_week": 2, "objectives": ["فهم القيم الإسلامية"], "distribution": {"term1": "القرآن", "term2": "الحديث", "term3": "الفقه"}, "books": ["التربية الإسلامية 1AS"], "new_changes": "لا تغييرات"},
                "civic": {"content": "الحياة الديمقراطية، المؤسسات، الهوية الوطنية.", "hours_per_week": 1, "objectives": ["تعزيز الحس المدني"], "distribution": {"term1": "الحياة الديمقراطية", "term2": "المؤسسات", "term3": "الهوية"}, "books": ["التربية المدنية 1AS"], "new_changes": "مادة أساسية"},
                "math": {"content": "الحساب العددي، الدوال، الهندسة.", "hours_per_week": 3, "objectives": ["إتقان الحساب"], "distribution": {"term1": "الحساب", "term2": "الدوال", "term3": "الهندسة"}, "books": ["الرياضيات 1AS"], "new_changes": "لا تغييرات"},
                "physics": {"content": "المحلول المائي، الظواهر الطبيعية.", "hours_per_week": 2, "objectives": ["فهم الظواهر الطبيعية"], "distribution": {"term1": "المحلول المائي", "term2": "الهواء", "term3": "الماء"}, "books": ["الفيزياء 1AS"], "new_changes": "لا تغييرات"},
                "history": {"content": "العالم الإسلامي، أدوات جغرافية.", "hours_per_week": 2, "objectives": ["تعرف العالم الإسلامي"], "distribution": {"term1": "العالم الإسلامي", "term2": "الأدوات الجغرافية", "term3": "التكتلات"}, "books": ["التاريخ والجغرافيا 1AS"], "new_changes": "لا تغييرات"},
                "informatics": {"content": "مدخل إلى الإعلام الآلي.", "hours_per_week": 1, "objectives": ["استخدام الحاسوب"], "distribution": {"term1": "مدخل", "term2": "الخوارزميات", "term3": "تطبيقات"}, "books": ["الإعلام الآلي 1AS"], "new_changes": "مادة أساسية"},
                "arts": {"content": "الرسم، الموسيقى، المسرح.", "hours_per_week": 2, "objectives": ["تنمية الحس الفني"], "distribution": {"term1": "الرسم", "term2": "الموسيقى", "term3": "المسرح"}, "books": ["كتاب الفنون 1AS"], "new_changes": "لا تغييرات"}
            }
        }
    },
    "2AS": {
        "sciences": {
            "name": "علوم تجريبية",
            "subjects": {
                "arabic": {"content": "الأدب العربي الحديث، البلاغة، القواعد، التعبير.", "hours_per_week": 4, "objectives": ["تعزيز التعبير", "فهم الأدب الحديث"], "distribution": {"term1": "الأدب الحديث", "term2": "البلاغة", "term3": "التعبير"}, "books": ["اللغة العربية 2AS"], "new_changes": "لا تغييرات"},
                "french": {"content": "Textes modernes, grammaire, dissertation.", "hours_per_week": 3, "objectives": ["Approfondir la grammaire"], "distribution": {"term1": "Textes", "term2": "Grammaire", "term3": "Dissertation"}, "books": ["Français 2AS"], "new_changes": "Renforcement"},
                "english": {"content": "Advanced texts, grammar, essay writing.", "hours_per_week": 3, "objectives": ["Improve essay writing"], "distribution": {"term1": "Texts", "term2": "Grammar", "term3": "Essay"}, "books": ["English 2AS"], "new_changes": "Increased hours"},
                "islamic": {"content": "القرآن، الحديث، الفقه، القيم.", "hours_per_week": 2, "objectives": ["تعزيز القيم"], "distribution": {"term1": "القرآن", "term2": "الحديث", "term3": "الفقه"}, "books": ["التربية الإسلامية 2AS"], "new_changes": "لا تغييرات"},
                "math": {"content": "الاشتقاقية، الدوال، المتتاليات، الحساب المثلثي، الاحتمالات.", "hours_per_week": 5, "objectives": ["إتقان الاشتقاقية", "فهم المتتاليات"], "distribution": {"term1": "الاشتقاقية", "term2": "المتتاليات", "term3": "الاحتمالات"}, "books": ["الرياضيات 2AS"], "new_changes": "تعزيز الإنجليزية"},
                "physics": {"content": "الطاقة الحركية والكامنة، الناقلية، الأحماض والقواعد.", "hours_per_week": 5, "objectives": ["فهم الطاقة", "تطبيق الناقلية"], "distribution": {"term1": "الطاقة", "term2": "الناقلية", "term3": "الأحماض"}, "books": ["الفيزياء 2AS"], "new_changes": "تعزيز الإنجليزية"},
                "sciences": {"content": "التغذية، المناعة، الوراثة.", "hours_per_week": 4, "objectives": ["فهم التغذية", "دراسة الوراثة"], "distribution": {"term1": "التغذية", "term2": "المناعة", "term3": "الوراثة"}, "books": ["العلوم 2AS"], "new_changes": "لا تغييرات"},
                "history": {"content": "الثورة الجزائرية، الحرب العالمية الثانية.", "hours_per_week": 2, "objectives": ["فهم الثورة"], "distribution": {"term1": "الثورة", "term2": "الحرب العالمية", "term3": "النظام الدولي"}, "books": ["التاريخ 2AS"], "new_changes": "لا تغييرات"},
                "physical_education": {"content": "أنشطة رياضية.", "hours_per_week": 2, "objectives": ["تعزيز اللياقة"], "distribution": {"term1": "جماعية", "term2": "فردية", "term3": "اختبارات"}, "books": ["دليل التربية البدنية"], "new_changes": "لا تغييرات"},
                "arts": {"content": "الرسم، الموسيقى، المسرح.", "hours_per_week": 2, "objectives": ["تنمية الحس الفني"], "distribution": {"term1": "الرسم", "term2": "الموسيقى", "term3": "المسرح"}, "books": ["كتاب الفنون 2AS"], "new_changes": "مادة جديدة"}
            }
        },
        "math": {
            "name": "شعبة الرياضيات",
            "subjects": {
                "arabic": {"content": "الأدب العربي الحديث، المقالة.", "hours_per_week": 3, "objectives": ["تعزيز الأدب"], "distribution": {"term1": "الأدب", "term2": "المقالة", "term3": "مراجعة"}, "books": ["اللغة العربية 2AS"], "new_changes": "لا تغييرات"},
                "french": {"content": "Textes scientifiques, grammaire.", "hours_per_week": 3, "objectives": ["Lire des textes scientifiques"], "distribution": {"term1": "Textes", "term2": "Grammaire", "term3": "Expression"}, "books": ["Français 2AS"], "new_changes": "Renforcement"},
                "english": {"content": "Scientific texts, grammar, writing.", "hours_per_week": 3, "objectives": ["Enhance scientific English"], "distribution": {"term1": "Texts", "term2": "Grammar", "term3": "Writing"}, "books": ["English 2AS"], "new_changes": "Increased hours"},
                "math": {"content": "الجبر، التحليل، الهندسة، الاحتمالات.", "hours_per_week": 6, "objectives": ["إتقان الجبر والتحليل"], "distribution": {"term1": "الجبر", "term2": "التحليل", "term3": "الهندسة"}, "books": ["الرياضيات 2AS"], "new_changes": "لا تغييرات"},
                "physics": {"content": "الميكانيك، الكهرباء.", "hours_per_week": 5, "objectives": ["فهم الميكانيك"], "distribution": {"term1": "الميكانيك", "term2": "الكهرباء", "term3": "مراجعة"}, "books": ["الفيزياء 2AS"], "new_changes": "لا تغييرات"},
                "informatics": {"content": "الخوارزميات، البرمجة.", "hours_per_week": 2, "objectives": ["تعلم البرمجة"], "distribution": {"term1": "الخوارزميات", "term2": "البرمجة", "term3": "مشاريع"}, "books": ["الإعلام الآلي 2AS"], "new_changes": "مادة جديدة"}
            }
        },
        "tech": {
            "name": "شعبة التقني رياضي",
            "subjects": {
                "arabic": {"content": "الأدب العربي الحديث.", "hours_per_week": 3, "objectives": ["تعزيز الأدب"], "distribution": {"term1": "الأدب", "term2": "المقالة", "term3": "مراجعة"}, "books": ["اللغة العربية 2AS"], "new_changes": "لا تغييرات"},
                "math": {"content": "الجبر، التحليل، الهندسة.", "hours_per_week": 6, "objectives": ["إتقان الجبر"], "distribution": {"term1": "الجبر", "term2": "التحليل", "term3": "الهندسة"}, "books": ["الرياضيات 2AS"], "new_changes": "لا تغييرات"},
                "physics": {"content": "الميكانيك، الكهرباء.", "hours_per_week": 5, "objectives": ["فهم الميكانيك"], "distribution": {"term1": "الميكانيك", "term2": "الكهرباء", "term3": "مراجعة"}, "books": ["الفيزياء 2AS"], "new_changes": "لا تغييرات"}
            }
        },
        "lettres": {
            "name": "آداب وفلسفة",
            "subjects": {
                "arabic": {"content": "الأدب العربي الحديث، المقالة، البلاغة.", "hours_per_week": 5, "objectives": ["تعزيز الأدب العربي", "إتقان المقالة والبلاغة"], "distribution": {"term1": "الأدب الحديث", "term2": "المقالة", "term3": "البلاغة"}, "books": ["كتاب اللغة العربية 2AS"], "new_changes": "لا تغييرات كبيرة"},
                "french": {"content": "Textes littéraires, grammaire, dissertation.", "hours_per_week": 3, "objectives": ["Lire et analyser des textes littéraires", "Rédiger une dissertation"], "distribution": {"term1": "Textes", "term2": "Grammaire", "term3": "Dissertation"}, "books": ["Livre de français 2AS"], "new_changes": "Renforcement de l'anglais"},
                "english": {"content": "Texts, grammar, essay writing.", "hours_per_week": 3, "objectives": ["Enhance essay writing", "Improve grammar"], "distribution": {"term1": "Texts", "term2": "Grammar", "term3": "Essay writing"}, "books": ["English textbook 2AS"], "new_changes": "Increased weekly hours"},
                "philosophy": {"content": "نشأة الفلسفة، السؤال العلمي والفلسفي، الفكر واللغة.", "hours_per_week": 4, "objectives": ["تعرف نشأة الفلسفة", "التمييز بين السؤال العلمي والفلسفي"], "distribution": {"term1": "نشأة الفلسفة", "term2": "الفكر واللغة", "term3": "الملاحظة والتجربة"}, "books": ["كتاب الفلسفة 2AS"], "new_changes": "تعزيز الإنجليزية"},
                "history": {"content": "الثورة الجزائرية، الحرب العالمية الثانية.", "hours_per_week": 3, "objectives": ["فهم الثورة الجزائرية", "تحليل الحرب العالمية الثانية"], "distribution": {"term1": "الثورة الجزائرية", "term2": "الحرب العالمية الثانية", "term3": "النظام الدولي الجديد"}, "books": ["كتاب التاريخ والجغرافيا 2AS"], "new_changes": "لا تغييرات كبيرة"},
                "arts": {"content": "التربية الفنية (رسم، موسيقى).", "hours_per_week": 1, "objectives": ["تنمية الحس الفني"], "distribution": {"term1": "رسم", "term2": "موسيقى", "term3": "مسرح"}, "books": ["كتاب الفنون 2AS"], "new_changes": "مادة موجودة"}
            }
        },
        "gestion": {
            "name": "تسيير واقتصاد",
            "subjects": {
                "arabic": {"content": "الأدب العربي الحديث.", "hours_per_week": 3, "objectives": ["تعزيز الأدب العربي"], "distribution": {"term1": "الأدب", "term2": "المقالة", "term3": "مراجعة"}, "books": ["كتاب اللغة العربية 2AS"], "new_changes": "لا تغييرات كبيرة"},
                "french": {"content": "Textes économiques, grammaire.", "hours_per_week": 3, "objectives": ["Lire des textes économiques"], "distribution": {"term1": "Textes", "term2": "Grammaire", "term3": "Dissertation"}, "books": ["Livre de français 2AS"], "new_changes": "Renforcement de l'anglais"},
                "english": {"content": "Economic texts, grammar, writing.", "hours_per_week": 3, "objectives": ["Enhance economic English"], "distribution": {"term1": "Texts", "term2": "Grammar", "term3": "Writing"}, "books": ["English textbook 2AS"], "new_changes": "Increased weekly hours"},
                "economics": {"content": "مبادئ الاقتصاد، المحاسبة، التسيير.", "hours_per_week": 6, "objectives": ["فهم مبادئ الاقتصاد", "إتقان المحاسبة"], "distribution": {"term1": "مبادئ الاقتصاد", "term2": "المحاسبة", "term3": "التسيير"}, "books": ["كتاب الاقتصاد 2AS"], "new_changes": "تعزيز الإنجليزية"}
            }
        },
        "langues": {
            "name": "لغات أجنبية",
            "subjects": {
                "arabic": {"content": "الأدب العربي الحديث.", "hours_per_week": 3, "objectives": ["تعزيز الأدب العربي"], "distribution": {"term1": "الأدب", "term2": "المقالة", "term3": "مراجعة"}, "books": ["كتاب اللغة العربية 2AS"], "new_changes": "لا تغييرات كبيرة"},
                "french": {"content": "Textes littéraires, grammaire.", "hours_per_week": 4, "objectives": ["Lire et analyser des textes littéraires"], "distribution": {"term1": "Textes", "term2": "Grammaire", "term3": "Dissertation"}, "books": ["Livre de français 2AS"], "new_changes": "Renforcement de l'anglais"},
                "english": {"content": "Texts, grammar, essay writing.", "hours_per_week": 4, "objectives": ["Enhance essay writing"], "distribution": {"term1": "Texts", "term2": "Grammar", "term3": "Essay writing"}, "books": ["English textbook 2AS"], "new_changes": "Increased weekly hours"},
                "spanish": {"content": "Textos, gramática, conversación.", "hours_per_week": 5, "objectives": ["Mejorar la conversación", "Escribir ensayos"], "distribution": {"term1": "Textos", "term2": "Gramática", "term3": "Conversación"}, "books": ["Libro de español 2AS"], "new_changes": "Nueva langue renforcée"},
                "german": {"content": "Texte, Grammatik, Schreiben.", "hours_per_week": 5, "objectives": ["Verbessern Sie die Konversation", "Aufsätze schreiben"], "distribution": {"term1": "Texte", "term2": "Grammatik", "term3": "Konversation"}, "books": ["Deutschbuch 2AS"], "new_changes": "Neue Sprache renforcée"}
            }
        },
        "arts": {
            "name": "شعبة الفنون",
            "subjects": {
                "arabic": {"content": "الأدب العربي الحديث، النقد الأدبي.", "hours_per_week": 4, "objectives": ["تحليل النصوص الأدبية"], "distribution": {"term1": "الأدب", "term2": "النقد", "term3": "التعبير"}, "books": ["اللغة العربية 2AS"], "new_changes": "شعبة مستحدثة"},
                "french": {"content": "Textes littéraires, grammaire.", "hours_per_week": 3, "objectives": ["Lire des textes"], "distribution": {"term1": "Textes", "term2": "Grammaire", "term3": "Expression"}, "books": ["Français 2AS"], "new_changes": "شعبة مستحدثة"},
                "english": {"content": "Texts, grammar, conversation.", "hours_per_week": 3, "objectives": ["Enhance communication"], "distribution": {"term1": "Texts", "term2": "Grammar", "term3": "Writing"}, "books": ["English 2AS"], "new_changes": "شعبة مستحدثة"},
                "philosophy": {"content": "الفلسفة والفن.", "hours_per_week": 3, "objectives": ["فهم فلسفة الفن"], "distribution": {"term1": "مدخل", "term2": "الجمال", "term3": "الفن"}, "books": ["الفلسفة 2AS"], "new_changes": "شعبة مستحدثة"},
                "history": {"content": "تاريخ الفنون.", "hours_per_week": 2, "objectives": ["فهم تاريخ الفن"], "distribution": {"term1": "قديم", "term2": "حديث", "term3": "معاصر"}, "books": ["التاريخ 2AS"], "new_changes": "شعبة مستحدثة"},
                "arts_specialty": {"content": "تخصص فني (تشكيلية/موسيقى/مسرح/سينما).", "hours_per_week": 6, "objectives": ["إتقان التخصص الفني"], "distribution": {"term1": "أساسيات", "term2": "تطبيقات", "term3": "مشاريع"}, "books": ["كتب التخصص"], "new_changes": "شعبة مستحدثة"}
            }
        }
    },
    "3AS": {
        "sciences": {
            "name": "علوم تجريبية",
            "subjects": {
                "arabic": {"content": "الأدب الجزائري الحديث، المقالة النقدية.", "hours_per_week": 4, "objectives": ["تحليل الأدب الجزائري", "كتابة المقالة النقدية"], "distribution": {"term1": "الأدب الجزائري", "term2": "المقالة النقدية", "term3": "مراجعة"}, "books": ["كتاب اللغة العربية 3AS"], "new_changes": "لا تغييرات"},
                "french": {"content": "Analyse de textes, dissertation, commentaire composé.", "hours_per_week": 3, "objectives": ["Analyser des textes", "Rédiger un commentaire composé"], "distribution": {"term1": "Analyse de textes", "term2": "Dissertation", "term3": "Commentaire composé"}, "books": ["Livre de français 3AS"], "new_changes": "Renforcement"},
                "english": {"content": "Literature analysis, advanced grammar, essay writing.", "hours_per_week": 4, "objectives": ["Analyze literature", "Write advanced essays"], "distribution": {"term1": "Literature analysis", "term2": "Grammar", "term3": "Essay writing"}, "books": ["English textbook 3AS"], "new_changes": "Increased weekly hours"},
                "islamic": {"content": "القرآن الكريم، الحديث، الفقه، القيم الإسلامية.", "hours_per_week": 2, "objectives": ["تعزيز القيم الإسلامية", "فهم الفقه"], "distribution": {"term1": "القرآن الكريم", "term2": "الحديث", "term3": "الفقه"}, "books": ["كتاب التربية الإسلامية 3AS"], "new_changes": "لا تغييرات"},
                "math": {"content": "النهايات، الاستمرارية، الاشتقاقية، المعادلات التفاضلية، التكامل، الأعداد المركبة، الاحتمالات الشرطية.", "hours_per_week": 6, "objectives": ["إتقان النهايات والاستمرارية", "حل المعادلات التفاضلية", "تطبيق الاحتمالات الشرطية"], "distribution": {"term1": "النهايات والاستمرارية", "term2": "المعادلات التفاضلية والتكامل", "term3": "الأعداد المركبة والاحتمالات"}, "books": ["كتاب الرياضيات 3AS"], "new_changes": "إضافة مادة الإعلام الآلي"},
                "physics": {"content": "الكهرباء، الميكانيك، الكيمياء العضوية، الموجات.", "hours_per_week": 6, "objectives": ["فهم الكهرباء والميكانيك", "استيعاب الكيمياء العضوية", "تحليل الموجات"], "distribution": {"term1": "الكهرباء", "term2": "الميكانيك", "term3": "الكيمياء العضوية والموجات"}, "books": ["كتاب الفيزياء 3AS"], "new_changes": "تعزيز الإنجليزية"},
                "sciences": {"content": "الوراثة، المناعة، البيوتكنولوجيا.", "hours_per_week": 6, "objectives": ["فهم الوراثة", "تعزيز مفهوم المناعة", "التعرف على البيوتكنولوجيا"], "distribution": {"term1": "الوراثة", "term2": "المناعة", "term3": "البيوتكنولوجيا"}, "books": ["كتاب العلوم الطبيعية 3AS"], "new_changes": "إضافة موضوعات حديثة"},
                "informatics": {"content": "Algorithms, Python programming, data processing.", "hours_per_week": 2, "objectives": ["Learn programming basics", "Apply algorithms", "Process data with Python"], "distribution": {"term1": "Algorithms", "term2": "Python programming", "term3": "Data processing"}, "books": ["Informatics textbook 3AS"], "new_changes": "New subject added"},
                "history": {"content": "الثورة الجزائرية، النظام الدولي الجديد، القضايا المعاصرة.", "hours_per_week": 2, "objectives": ["فهم الثورة الجزائرية", "تحليل النظام الدولي الجديد"], "distribution": {"term1": "الثورة الجزائرية", "term2": "النظام الدولي الجديد", "term3": "القضايا المعاصرة"}, "books": ["كتاب التاريخ والجغرافيا 3AS"], "new_changes": "لا تغييرات"},
                "physical_education": {"content": "أنشطة رياضية متنوعة.", "hours_per_week": 2, "objectives": ["تعزيز اللياقة البدنية", "تنمية الروح الرياضية"], "distribution": {"term1": "رياضات جماعية", "term2": "رياضات فردية", "term3": "اختبارات بدنية"}, "books": ["دليل التربية البدنية 3AS"], "new_changes": "لا تغييرات"},
                "arts": {"content": "الرسم، الموسيقى، المسرح.", "hours_per_week": 2, "objectives": ["تنمية الحس الفني", "تعزيز الإبداع"], "distribution": {"term1": "الرسم", "term2": "الموسيقى", "term3": "المسرح"}, "books": ["كتاب الفنون 3AS"], "new_changes": "إضافة مادة الفنون"}
            }
        },
        "math": {
            "name": "شعبة الرياضيات",
            "subjects": {
                "arabic": {"content": "الأدب العربي الحديث.", "hours_per_week": 3, "objectives": ["تعزيز الأدب العربي"], "distribution": {"term1": "الأدب", "term2": "المقالة", "term3": "مراجعة"}, "books": ["كتاب اللغة العربية 3AS"], "new_changes": "لا تغييرات"},
                "french": {"content": "Textes scientifiques, dissertation.", "hours_per_week": 3, "objectives": ["Lire et analyser des textes scientifiques"], "distribution": {"term1": "Textes", "term2": "Dissertation", "term3": "Commentaire"}, "books": ["Livre de français 3AS"], "new_changes": "Renforcement"},
                "english": {"content": "Scientific texts, grammar, essay writing.", "hours_per_week": 4, "objectives": ["Enhance scientific English"], "distribution": {"term1": "Texts", "term2": "Grammar", "term3": "Essay writing"}, "books": ["English textbook 3AS"], "new_changes": "Increased weekly hours"},
                "math": {"content": "الجبر، التحليل، الهندسة، الاحتمالات.", "hours_per_week": 8, "objectives": ["إتقان الجبر والتحليل"], "distribution": {"term1": "الجبر", "term2": "التحليل", "term3": "الهندسة والاحتمالات"}, "books": ["كتاب الرياضيات 3AS"], "new_changes": "إضافة مادة الإعلام الآلي"},
                "physics": {"content": "الميكانيك، الكهرباء.", "hours_per_week": 6, "objectives": ["فهم الميكانيك والكهرباء"], "distribution": {"term1": "الميكانيك", "term2": "الكهرباء", "term3": "مراجعة"}, "books": ["كتاب الفيزياء 3AS"], "new_changes": "لا تغييرات"},
                "informatics": {"content": "Algorithms, Python programming.", "hours_per_week": 3, "objectives": ["Learn programming basics"], "distribution": {"term1": "Algorithms", "term2": "Python programming", "term3": "Projects"}, "books": ["Informatics textbook 3AS"], "new_changes": "New subject added"}
            }
        },
        "tech": {
            "name": "شعبة التقني رياضي (هندسة)",
            "subjects": {
                "arabic": {"content": "الأدب العربي الحديث.", "hours_per_week": 3, "objectives": ["تعزيز الأدب العربي"], "distribution": {"term1": "الأدب", "term2": "المقالة", "term3": "مراجعة"}, "books": ["كتاب اللغة العربية 3AS"], "new_changes": "لا تغييرات"},
                "math": {"content": "الجبر، التحليل، الهندسة.", "hours_per_week": 5, "objectives": ["إتقان الجبر والتحليل"], "distribution": {"term1": "الجبر", "term2": "التحليل", "term3": "الهندسة"}, "books": ["كتاب الرياضيات 3AS"], "new_changes": "تغيير المعامل"},
                "physics": {"content": "الميكانيك، الكهرباء.", "hours_per_week": 4, "objectives": ["فهم الميكانيك والكهرباء"], "distribution": {"term1": "الميكانيك", "term2": "الكهرباء", "term3": "مراجعة"}, "books": ["كتاب الفيزياء 3AS"], "new_changes": "تغيير المعامل"},
                "informatics": {"content": "الخوارزميات، البرمجة.", "hours_per_week": 3, "objectives": ["تعلم البرمجة"], "distribution": {"term1": "الخوارزميات", "term2": "البرمجة", "term3": "مشاريع"}, "books": ["الإعلام الآلي 3AS"], "new_changes": "مادة جديدة"}
            }
        },
        "lettres": {
            "name": "آداب وفلسفة",
            "subjects": {
                "arabic": {"content": "الأدب الجزائري الحديث، المقالة النقدية.", "hours_per_week": 8, "objectives": ["تحليل الأدب الجزائري", "كتابة المقالة النقدية"], "distribution": {"term1": "الأدب الجزائري", "term2": "المقالة النقدية", "term3": "مراجعة"}, "books": ["كتاب اللغة العربية 3AS"], "new_changes": "لا تغييرات كبيرة"},
                "french": {"content": "Analyse de textes, dissertation, commentaire composé.", "hours_per_week": 3, "objectives": ["Analyser des textes", "Rédiger un commentaire composé"], "distribution": {"term1": "Analyse de textes", "term2": "Dissertation", "term3": "Commentaire composé"}, "books": ["Livre de français 3AS"], "new_changes": "Renforcement de l'anglais"},
                "english": {"content": "Literature analysis, advanced grammar, essay writing.", "hours_per_week": 4, "objectives": ["Analyze literature", "Write advanced essays"], "distribution": {"term1": "Literature analysis", "term2": "Grammar", "term3": "Essay writing"}, "books": ["English textbook 3AS"], "new_changes": "Increased weekly hours"},
                "philosophy": {"content": "إدراك العالم الخارجي، الأخلاق بين المطلق والنسبي، فلسفة العلوم.", "hours_per_week": 6, "objectives": ["فهم إدراك العالم الخارجي", "تحليل الأخلاق بين المطلق والنسبي"], "distribution": {"term1": "إدراك العالم الخارجي", "term2": "الأخلاق", "term3": "فلسفة العلوم"}, "books": ["كتاب الفلسفة 3AS"], "new_changes": "تعزيز الإنجليزية"},
                "history": {"content": "الثورة الجزائرية، النظام الدولي الجديد.", "hours_per_week": 4, "objectives": ["فهم الثورة الجزائرية", "تحليل النظام الدولي الجديد"], "distribution": {"term1": "الثورة الجزائرية", "term2": "النظام الدولي الجديد", "term3": "مراجعة عامة"}, "books": ["كتاب التاريخ والجغرافيا 3AS"], "new_changes": "لا تغييرات كبيرة"}
            }
        },
        "gestion": {
            "name": "تسيير واقتصاد",
            "subjects": {
                "arabic": {"content": "الأدب الجزائري الحديث، المقالة النقدية.", "hours_per_week": 3, "objectives": ["تحليل الأدب الجزائري", "كتابة المقالة النقدية"], "distribution": {"term1": "الأدب الجزائري", "term2": "المقالة النقدية", "term3": "مراجعة"}, "books": ["كتاب اللغة العربية 3AS"], "new_changes": "لا تغييرات كبيرة"},
                "french": {"content": "Textes économiques, grammaire, dissertation.", "hours_per_week": 3, "objectives": ["Lire et analyser des textes économiques", "Rédiger une dissertation"], "distribution": {"term1": "Textes économiques", "term2": "Grammaire", "term3": "Dissertation"}, "books": ["Livre de français 3AS"], "new_changes": "Renforcement de l'anglais"},
                "english": {"content": "Economic texts, grammar, essay writing.", "hours_per_week": 3, "objectives": ["Enhance economic English", "Write essays"], "distribution": {"term1": "Texts", "term2": "Grammar", "term3": "Essay writing"}, "books": ["English textbook 3AS"], "new_changes": "Increased weekly hours"},
                "economics": {"content": "المحاسبة، التسيير المالي، الاقتصاد الكلي.", "hours_per_week": 6, "objectives": ["إتقان المحاسبة", "فهم الاقتصاد الكلي", "تطبيق مبادئ التسيير المالي"], "distribution": {"term1": "المحاسبة", "term2": "التسيير المالي", "term3": "الاقتصاد الكلي"}, "books": ["كتاب الاقتصاد 3AS"], "new_changes": "تعزيز الإنجليزية"},
                "law": {"content": "القانون التجاري، القانون المدني.", "hours_per_week": 3, "objectives": ["فهم القانون التجاري", "دراسة القانون المدني"], "distribution": {"term1": "القانون التجاري", "term2": "القانون المدني", "term3": "مراجعة"}, "books": ["كتاب القانون 3AS"], "new_changes": "إضافة موضوعات حديثة"},
                "math": {"content": "الدوال العددية، المتتاليات، الإحصاء، المصفوفات.", "hours_per_week": 5, "objectives": ["تطبيق الرياضيات في الاقتصاد"], "distribution": {"term1": "الدوال", "term2": "الإحصاء", "term3": "المصفوفات"}, "books": ["كتاب الرياضيات 3AS"], "new_changes": "تطبيقات اقتصادية"},
                "history": {"content": "الثورة الجزائرية، النظام الدولي الجديد.", "hours_per_week": 2, "objectives": ["فهم الثورة"], "distribution": {"term1": "الثورة", "term2": "النظام الدولي", "term3": "مراجعة"}, "books": ["التاريخ 3AS"], "new_changes": "لا تغييرات"},
                "philosophy": {"content": "إدراك العالم الخارجي، الأخلاق، فلسفة العلوم.", "hours_per_week": 2, "objectives": ["فهم الفلسفة"], "distribution": {"term1": "إدراك العالم", "term2": "الأخلاق", "term3": "فلسفة العلوم"}, "books": ["الفلسفة 3AS"], "new_changes": "لا تغييرات"}
            }
        },
        "langues": {
            "name": "لغات أجنبية",
            "subjects": {
                "arabic": {"content": "الأدب العربي الحديث.", "hours_per_week": 2, "objectives": ["تعزيز الأدب العربي"], "distribution": {"term1": "الأدب", "term2": "المقالة", "term3": "مراجعة"}, "books": ["كتاب اللغة العربية 3AS"], "new_changes": "لا تغييرات كبيرة"},
                "french": {"content": "Analyse de textes littéraires, dissertation.", "hours_per_week": 4, "objectives": ["Analyser des textes littéraires", "Rédiger une dissertation"], "distribution": {"term1": "Analyse de textes", "term2": "Dissertation", "term3": "Commentaire composé"}, "books": ["Livre de français 3AS"], "new_changes": "Renforcement de l'anglais"},
                "english": {"content": "Literature analysis, advanced grammar, essay writing.", "hours_per_week": 4, "objectives": ["Analyze literature", "Write advanced essays"], "distribution": {"term1": "Literature analysis", "term2": "Grammar", "term3": "Essay writing"}, "books": ["English textbook 3AS"], "new_changes": "Increased weekly hours"},
                "spanish": {"content": "Textos literarios, gramática avanzada, conversación.", "hours_per_week": 5, "objectives": ["Mejorar la conversación", "Escribir ensayos"], "distribution": {"term1": "Textos literarios", "term2": "Gramática avanzada", "term3": "Conversación"}, "books": ["Libro de español 3AS"], "new_changes": "Nueva langue renforcée"},
                "german": {"content": "Texte, Grammatik, Aufsatzschreiben.", "hours_per_week": 5, "objectives": ["Verbessern Sie die Konversation", "Aufsätze schreiben"], "distribution": {"term1": "Texte", "term2": "Grammatik", "term3": "Konversation"}, "books": ["Deutschbuch 3AS"], "new_changes": "Neue Sprache renforcée"},
                "italian": {"content": "Testi, grammatica, conversazione.", "hours_per_week": 5, "objectives": ["Migliorare la conversazione", "Scrivere saggi"], "distribution": {"term1": "Testi", "term2": "Grammatica", "term3": "Conversazione"}, "books": ["Libro di italiano 3AS"], "new_changes": "Nuova lingua renforcée"},
                "philosophy": {"content": "إدراك العالم الخارجي، الأخلاق، فلسفة العلوم.", "hours_per_week": 2, "objectives": ["فهم الفلسفة"], "distribution": {"term1": "إدراك العالم", "term2": "الأخلاق", "term3": "فلسفة العلوم"}, "books": ["الفلسفة 3AS"], "new_changes": "لا تغييرات"},
                "math": {"content": "القسمة الإقليدية، المتتاليات، الدوال.", "hours_per_week": 2, "objectives": ["فهم الرياضيات الأساسية"], "distribution": {"term1": "القسمة", "term2": "المتتاليات", "term3": "الدوال"}, "books": ["الرياضيات 3AS"], "new_changes": "لا تغييرات"}
            }
        },
        "arts": {
            "name": "شعبة الفنون",
            "subjects": {
                "arabic": {"content": "الأدب والنقد والبلاغة والعروض.", "hours_per_week": 3, "objectives": ["تحليل النصوص"], "distribution": {"term1": "الأدب", "term2": "النقد", "term3": "البلاغة"}, "books": ["اللغة العربية 3AS"], "new_changes": "شعبة مستحدثة"},
                "philosophy": {"content": "فلسفة الفن وعلم الجمال.", "hours_per_week": 3, "objectives": ["فهم فلسفة الفن"], "distribution": {"term1": "مدخل", "term2": "الجمال", "term3": "الفن"}, "books": ["الفلسفة 3AS"], "new_changes": "شعبة مستحدثة"},
                "history": {"content": "تاريخ الفنون.", "hours_per_week": 2, "objectives": ["فهم تاريخ الفن"], "distribution": {"term1": "قديم", "term2": "حديث", "term3": "معاصر"}, "books": ["التاريخ 3AS"], "new_changes": "شعبة مستحدثة"},
                "arts_specialty": {"content": "تخصص فني (تشكيلية/موسيقى/مسرح/سينما).", "hours_per_week": 8, "objectives": ["إتقان التخصص الفني"], "distribution": {"term1": "أساسيات", "term2": "تطبيقات", "term3": "مشاريع"}, "books": ["كتب التخصص"], "new_changes": "شعبة مستحدثة"}
            }
        }
    }
}
