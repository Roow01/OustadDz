# curriculum_data.py
# القاعدة المعرفية الموسعة للبرنامج الرسمي (2026/2027)          
CURRICULUM_DATA = {
    "1AS": {
        "sciences": {
            "name": "جذع مشترك علوم وتكنولوجيا",
            "subjects": {
                "arabic": {
                    "content": "الأدب الجاهلي والإسلامي، البلاغة، القواعد والصرف، التعبير.",
                    "hours_per_week": 5,
                    "objectives": ["تعرف الأدب الجاهلي والإسلامي", "إتقان البلاغة والقواعد"],
                    "distribution": {"term1": "الأدب الجاهلي", "term2": "الأدب الإسلامي + البلاغة", "term3": "القواعد والتعبير"},
                    "books": ["كتاب اللغة العربية 1AS"],
                    "new_changes": "لا تغييرات كبيرة"
                },
                "french": {
                    "content": "Textes littéraires, grammaire, expression écrite et orale.",
                    "hours_per_week": 4,
                    "objectives": ["Maîtriser la lecture et la compréhension", "Développer l'expression écrite et orale"],
                    "distribution": {"term1": "Textes + grammaire", "term2": "Expression écrite", "term3": "Expression orale"},
                    "books": ["Livre de français 1AS"],
                    "new_changes": "Renforcement des heures"
                },
                "english": {
                    "content": "Texts, grammar, conversation, writing.",
                    "hours_per_week": 2,
                    "objectives": ["Enhance communication in English", "Master basic grammar"],
                    "distribution": {"term1": "Texts + grammar", "term2": "Conversation", "term3": "Writing"},
                    "books": ["English textbook 1AS"],
                    "new_changes": "Increased weekly hours"
                },
                "islamic": {
                    "content": "القرآن الكريم، الحديث الشريف، السيرة النبوية، الفقه.",
                    "hours_per_week": 2,
                    "objectives": ["فهم القيم الإسلامية", "تعزيز الأخلاق والسلوك"],
                    "distribution": {"term1": "القرآن الكريم", "term2": "الحديث والسيرة", "term3": "الفقه"},
                    "books": ["كتاب التربية الإسلامية 1AS"],
                    "new_changes": "لا تغييرات كبيرة"
                },
                "math": {
                    "content": "الأعداد والحساب، الدوال العددية، الدوال المرجعية، الهندسة المستوية والفضائية، الإحصاء والاحتمالات.",
                    "hours_per_week": 5,
                    "objectives": ["إتقان الحساب العددي والدوال المرجعية", "تطوير مهارات التحليل الإحصائي والاحتمالات"],
                    "distribution": {"term1": "الأعداد والحساب + الدوال المرجعية", "term2": "الهندسة المستوية والفضائية", "term3": "الإحصاء والاحتمالات"},
                    "books": ["كتاب الرياضيات 1AS"],
                    "new_changes": "لا تغييرات كبيرة"
                },
                "physics": {
                    "content": "مفهوم النوع الكيميائي، القوة والحركات، التحول الكيميائي والضوء.",
                    "hours_per_week": 5,
                    "objectives": ["فهم البنية الكيميائية", "تطبيق قوانين الحركة", "استيعاب التحولات الكيميائية والضوء"],
                    "distribution": {"term1": "مفهوم النوع الكيميائي", "term2": "القوة والحركات", "term3": "التحول الكيميائي والضوء"},
                    "books": ["كتاب الفيزياء 1AS"],
                    "new_changes": "لا تغييرات كبيرة"
                },
                "sciences": {
                    "content": "التركيب الضوئي، التحويل الطاقوي، التحكم العصبي والهرموني.",
                    "hours_per_week": 4,
                    "objectives": ["فهم آليات التركيب الضوئي", "التعرف على التحويلات الطاقوية", "استيعاب التحكم العصبي والهرموني"],
                    "distribution": {"term1": "التركيب الضوئي", "term2": "التحويل الطاقوي", "term3": "التحكم العصبي والهرموني"},
                    "books": ["كتاب العلوم الطبيعية 1AS"],
                    "new_changes": "لا تغييرات كبيرة"
                },
                "history": {
                    "content": "العالم الإسلامي، أدوات جغرافية، التكتلات الاقتصادية.",
                    "hours_per_week": 2,
                    "objectives": ["تعرف العالم الإسلامي", "فهم التكتلات الاقتصادية"],
                    "distribution": {"term1": "العالم الإسلامي", "term2": "الأدوات الجغرافية", "term3": "التكتلات الاقتصادية"},
                    "books": ["كتاب التاريخ والجغرافيا 1AS"],
                    "new_changes": "لا تغييرات كبيرة"
                },
                "physical_education": {
                    "content": "أنشطة رياضية متنوعة.",
                    "hours_per_week": 2,
                    "objectives": ["تعزيز اللياقة البدنية", "تنمية الروح الرياضية"],
                    "distribution": {"term1": "رياضات جماعية", "term2": "رياضات فردية", "term3": "اختبارات بدنية"},
                    "books": ["دليل التربية البدنية 1AS"],
                    "new_changes": "لا تغييرات كبيرة"
                },
                "arts": {
                    "content": "الرسم، الموسيقى، المسرح.",
                    "hours_per_week": 2,
                    "objectives": ["تنمية الحس الفني", "تعزيز الإبداع"],
                    "distribution": {"term1": "الرسم", "term2": "الموسيقى", "term3": "المسرح"},
                    "books": ["كتاب الفنون 1AS"],
                    "new_changes": "إضافة مادة الفنون"
                }
            }
        },
        "lettres": {
            "name": "جذع مشترك آداب",
            "subjects": {
                "arabic": {
                    "content": "الأدب الجاهلي والإسلامي، البلاغة، القواعد، التعبير.",
                    "hours_per_week": 6,
                    "objectives": ["تعزيز الأدب العربي", "إتقان التعبير"],
                    "distribution": {"term1": "الأدب الجاهلي", "term2": "الأدب الإسلامي", "term3": "التعبير والبلاغة"},
                    "books": ["كتاب اللغة العربية 1AS"],
                    "new_changes": "لا تغييرات كبيرة"
                },
                "french": {
                    "content": "Textes littéraires, grammaire, expression écrite et orale.",
                    "hours_per_week": 4,
                    "objectives": ["Maîtriser la lecture et la compréhension", "Développer l'expression écrite et orale"],
                    "distribution": {"term1": "Textes + grammaire", "term2": "Expression écrite", "term3": "Expression orale"},
                    "books": ["Livre de français 1AS"],
                    "new_changes": "Renforcement des heures"
                },
                "english": {
                    "content": "Texts, grammar, conversation, writing.",
                    "hours_per_week": 2,
                    "objectives": ["Enhance communication in English", "Master basic grammar"],
                    "distribution": {"term1": "Texts + grammar", "term2": "Conversation", "term3": "Writing"},
                    "books": ["English textbook 1AS"],
                    "new_changes": "Increased weekly hours"
                },
                "islamic": {
                    "content": "القرآن الكريم، الحديث الشريف، السيرة النبوية، الفقه.",
                    "hours_per_week": 2,
                    "objectives": ["فهم القيم الإسلامية", "تعزيز الأخلاق والسلوك"],
                    "distribution": {"term1": "القرآن الكريم", "term2": "الحديث والسيرة", "term3": "الفقه"},
                    "books": ["كتاب التربية الإسلامية 1AS"],
                    "new_changes": "لا تغييرات كبيرة"
                },
                "math": {
                    "content": "الحساب العددي، الدوال، الهندسة، الإحصاء.",
                    "hours_per_week": 3,
                    "objectives": ["إتقان الحساب العددي", "فهم الدوال والهندسة"],
                    "distribution": {"term1": "الحساب العددي", "term2": "الدوال", "term3": "الهندسة والإحصاء"},
                    "books": ["كتاب الرياضيات 1AS"],
                    "new_changes": "لا تغييرات كبيرة"
                },
                "physics": {
                    "content": "المحلول المائي، الظواهر الطبيعية البسيطة.",
                    "hours_per_week": 2,
                    "objectives": ["فهم الظواهر الطبيعية", "دراسة الماء والهواء"],
                    "distribution": {"term1": "المحلول المائي", "term2": "الهواء", "term3": "الماء"},
                    "books": ["كتاب الفيزياء 1AS
    "2AS": {
        "sciences": {
            "name": "علوم تجريبية",
            "subjects": {
                "arabic": {
                    "content": "الأدب العربي الحديث، البلاغة، القواعد، التعبير.",
                    "hours_per_week": 4,
                    "objectives": ["تعزيز مهارات التعبير", "فهم الأدب الحديث"],
                    "distribution": {"term1": "الأدب العربي الحديث", "term2": "البلاغة والقواعد", "term3": "التعبير"},
                    "books": ["كتاب اللغة العربية 2AS"],
                    "new_changes": "لا تغييرات كبيرة"
                },
                "french": {
                    "content": "Textes modernes, grammaire avancée, dissertation.",
                    "hours_per_week": 3,
                    "objectives": ["Approfondir la grammaire", "Rédiger une dissertation"],
                    "distribution": {"term1": "Textes modernes", "term2": "Grammaire avancée", "term3": "Dissertation"},
                    "books": ["Livre de français 2AS"],
                    "new_changes": "Renforcement de l'anglais"
                },
                "english": {
                    "content": "Advanced texts, grammar, essay writing.",
                    "hours_per_week": 3,
                    "objectives": ["Improve essay writing", "Enhance advanced grammar"],
                    "distribution": {"term1": "Texts", "term2": "Grammar", "term3": "Essay writing"},
                    "books": ["English textbook 2AS"],
                    "new_changes": "Increased weekly hours"
                },
                "islamic": {
                    "content": "القرآن الكريم، الحديث، الفقه، القيم الإسلامية.",
                    "hours_per_week": 2,
                    "objectives": ["تعزيز القيم الإسلامية", "فهم الفقه"],
                    "distribution": {"term1": "القرآن الكريم", "term2": "الحديث", "term3": "الفقه"},
                    "books": ["كتاب التربية الإسلامية 2AS"],
                    "new_changes": "لا تغييرات كبيرة"
                },
                "math": {
                    "content": "الاشتقاقية وتطبيقاتها، دراسة الدوال، المتتاليات العددية، الحساب المثلثي، الهندسة الفضائية والاحتمالات.",
                    "hours_per_week": 5,
                    "objectives": ["إتقان الاشتقاقية وتطبيقاتها", "فهم المتتاليات العددية", "تطبيق الاحتمالات في مسائل علمية"],
                    "distribution": {"term1": "الاشتقاقية والدوال", "term2": "المتتاليات والحساب المثلثي", "term3": "الهندسة الفضائية والاحتمالات"},
                    "books": ["كتاب الرياضيات 2AS"],
                    "new_changes": "تعزيز الإنجليزية"
                },
                "physics": {
                    "content": "الطاقة الحركية والكامنة، الناقلية، الأحماض والقواعد، الظواهر المغناطيسية.",
                    "hours_per_week": 5,
                    "objectives": ["فهم الطاقة الحركية والكامنة", "تطبيق قوانين الناقلية", "استيعاب الظواهر المغناطيسية"],
                    "distribution": {"term1": "الطاقة الحركية والكامنة", "term2": "الناقلية والأحماض والقواعد", "term3": "الظواهر المغناطيسية"},
                    "books": ["كتاب الفيزياء 2AS"],
                    "new_changes": "تعزيز الإنجليزية"
                },
                "sciences": {
                    "content": "التغذية عند الإنسان، المناعة، الوراثة.",
                    "hours_per_week": 4,
                    "objectives": ["فهم التغذية", "تعزيز مفهوم المناعة", "دراسة الوراثة"],
                    "distribution": {"term1": "التغذية", "term2": "المناعة", "term3": "الوراثة"},
                    "books": ["كتاب العلوم الطبيعية 2AS"],
                    "new_changes": "لا تغييرات كبيرة"
                },
                "history": {
                    "content": "الثورة الجزائرية، الحرب العالمية الثانية، النظام الدولي الجديد.",
                    "hours_per_week": 2,
                    "objectives": ["فهم الثورة الجزائرية", "تحليل الحرب العالمية الثانية"],
                    "distribution": {"term1": "الثورة الجزائرية", "term2": "الحرب العالمية الثانية", "term3": "النظام الدولي الجديد"},
                    "books": ["كتاب التاريخ والجغرافيا 2AS"],
                    "new_changes": "لا تغييرات كبيرة"
                },
                "physical_education": {
                    "content": "أنشطة رياضية متنوعة.",
                    "hours_per_week": 2,
                    "objectives": ["تعزيز اللياقة البدنية", "تنمية الروح الرياضية"],
                    "distribution": {"term1": "رياضات جماعية", "term2": "رياضات فردية", "term3": "اختبارات بدنية"},
                    "books": ["دليل التربية البدنية 2AS"],
                    "new_changes": "لا تغييرات كبيرة"
                },
                "arts": {
                    "content": "الرسم، الموسيقى، المسرح.",
                    "hours_per_week": 2,
                    "objectives": ["تنمية الحس الفني", "تعزيز الإبداع"],
                    "distribution": {"term1": "الرسم", "term2": "الموسيقى", "term3": "المسرح"},
                    "books": ["كتاب الفنون 2AS"],
                    "new_changes": "إضافة مادة الفنون"
                }
            }
        },
        "math": {
            "name": "شعبة الرياضيات",
            "subjects": {
                "arabic": {"content": "الأدب العربي الحديث، المقالة.", "hours_per_week": 3, "objectives": ["تعزيز الأدب العربي"], "distribution": {"term1": "الأدب", "term2": "المقالة", "term3": "مراجعة"}, "books": ["كتاب اللغة العربية 2AS"], "new_changes": "لا تغييرات كبيرة"},
                "french": {"content": "Textes scientifiques, grammaire.", "hours_per_week": 3, "objectives": ["Lire des textes scientifiques"], "distribution": {"term1": "Textes", "term2": "Grammaire", "term3": "Expression"}, "books": ["Livre de français 2AS"], "new_changes": "Renforcement de l'anglais"},
                "english": {"content": "Scientific texts, grammar, writing.", "hours_per_week": 3, "objectives": ["Enhance scientific English"], "distribution": {"term1": "Texts", "term2": "Grammar", "term3": "Writing"}, "books": ["English textbook 2AS"], "new_changes": "Increased weekly hours"},
                "math": {"content": "الجبر، التحليل، الهندسة، الاحتمالات.", "hours_per_week": 6, "objectives": ["إتقان الجبر والتحليل"], "distribution": {"term1": "الجبر", "term2": "التحليل", "term3": "الهندسة والاحتمالات"}, "books": ["كتاب الرياضيات 2AS"], "new_changes": "لا تغييرات كبيرة"},
                "physics": {"content": "الميكانيك، الكهرباء.", "hours_per_week": 5, "objectives": ["فهم الميكانيك", "تطبيق قوانين الكهرباء"], "distribution": {"term1": "الميكانيك", "term2": "الكهرباء", "term3": "مراجعة"}, "books": ["كتاب الفيزياء 2AS"], "new_changes": "لا تغييرات كبيرة"},
                "informatics": {"content": "الخوارزميات، البرمجة.", "hours_per_week": 2, "objectives": ["تعلم البرمجة"], "distribution": {"term1": "الخوارزميات", "term2": "البرمجة", "term3": "مشاريع تطبيقية"}, "books": ["كتاب الإعلام الآلي 2AS"], "new_changes": "إضافة مادة الإعلام الآلي"}
            }
        },
        "tech": {
            "name": "شعبة التقني رياضي",
            "subjects": {
                "arabic": {"content": "الأدب العربي الحديث.", "hours_per_week": 3, "objectives": ["تعزيز الأدب العربي"], "distribution": {"term1": "الأدب", "term2": "المقالة", "term3": "مراجعة"}, "books": ["كتاب اللغة العربية 2AS"], "new_changes": "لا تغييرات كبيرة"},
                "math": {"content": "الجبر، التحليل، الهندسة.", "hours_per_week": 6, "objectives": ["إتقان الجبر والتحليل"], "distribution": {"term1": "الجبر", "term2": "التحليل", "term3": "الهندسة"}, "books": ["كتاب الرياضيات 2AS"], "new_changes": "لا تغييرات كبيرة"},
                "physics": {"content": "الميكاني      
    "3AS": {
        "sciences": {
            "name": "علوم تجريبية",
            "subjects": {
                "arabic": {
                    "content": "الأدب الجزائري الحديث، المقالة النقدية.",
                    "hours_per_week": 4,
                    "objectives": ["تحليل الأدب الجزائري", "كتابة المقالة النقدية"],
                    "distribution": {"term1": "الأدب الجزائري", "term2": "المقالة النقدية", "term3": "مراجعة"},
                    "books": ["كتاب اللغة العربية 3AS"],
                    "new_changes": "لا تغييرات كبيرة"
                },
                "french": {
                    "content": "Analyse de textes, dissertation, commentaire composé.",
                    "hours_per_week": 3,
                    "objectives": ["Analyser des textes", "Rédiger un commentaire composé"],
                    "distribution": {"term1": "Analyse de textes", "term2": "Dissertation", "term3": "Commentaire composé"},
                    "books": ["Livre de français 3AS"],
                    "new_changes": "Renforcement de l'anglais"
                },
                "english": {
                    "content": "Literature analysis, advanced grammar, essay writing.",
                    "hours_per_week": 4,
                    "objectives": ["Analyze literature", "Write advanced essays"],
                    "distribution": {"term1": "Literature analysis", "term2": "Grammar", "term3": "Essay writing"},
                    "books": ["English textbook 3AS"],
                    "new_changes": "Increased weekly hours"
                },
                "islamic": {
                    "content": "القرآن الكريم، الحديث، الفقه، القيم الإسلامية.",
                    "hours_per_week": 2,
                    "objectives": ["تعزيز القيم الإسلامية", "فهم الفقه"],
                    "distribution": {"term1": "القرآن الكريم", "term2": "الحديث", "term3": "الفقه"},
                    "books": ["كتاب التربية الإسلامية 3AS"],
                    "new_changes": "لا تغييرات كبيرة"
                },
                "math": {
                    "content": "النهايات، الاستمرارية، الاشتقاقية، المعادلات التفاضلية، التكامل، الأعداد المركبة، الاحتمالات الشرطية.",
                    "hours_per_week": 6,
                    "objectives": ["إتقان النهايات والاستمرارية", "حل المعادلات التفاضلية", "تطبيق الاحتمالات الشرطية"],
                    "distribution": {"term1": "النهايات والاستمرارية", "term2": "المعادلات التفاضلية والتكامل", "term3": "الأعداد المركبة والاحتمالات"},
                    "books": ["كتاب الرياضيات 3AS"],
                    "new_changes": "إضافة مادة الإعلام الآلي"
                },
                "physics": {
                    "content": "الكهرباء، الميكانيك، الكيمياء العضوية، الموجات.",
                    "hours_per_week": 6,
                    "objectives": ["فهم الكهرباء والميكانيك", "استيعاب الكيمياء العضوية", "تحليل الموجات"],
                    "distribution": {"term1": "الكهرباء", "term2": "الميكانيك", "term3": "الكيمياء العضوية والموجات"},
                    "books": ["كتاب الفيزياء 3AS"],
                    "new_changes": "تعزيز الإنجليزية"
                },
                "sciences": {
                    "content": "الوراثة، المناعة، البيوتكنولوجيا.",
                    "hours_per_week": 6,
                    "objectives": ["فهم الوراثة", "تعزيز مفهوم المناعة", "التعرف على البيوتكنولوجيا"],
                    "distribution": {"term1": "الوراثة", "term2": "المناعة", "term3": "البيوتكنولوجيا"},
                    "books": ["كتاب العلوم الطبيعية 3AS"],
                    "new_changes": "إضافة موضوعات حديثة"
                },
                "informatics": {
                    "content": "Algorithms, Python programming, data processing.",
                    "hours_per_week": 2,
                    "objectives": ["Learn programming basics", "Apply algorithms", "Process data with Python"],
                    "distribution": {"term1": "Algorithms", "term2": "Python programming", "term3": "Data processing"},
                    "books": ["Informatics textbook 3AS"],
                    "new_changes": "New subject added"
                },
                "history": {
                    "content": "الثورة الجزائرية، النظام الدولي الجديد، القضايا المعاصرة.",
                    "hours_per_week": 2,
                    "objectives": ["فهم الثورة الجزائرية", "تحليل النظام الدولي الجديد"],
                    "distribution": {"term1": "الثورة الجزائرية", "term2": "النظام الدولي الجديد", "term3": "القضايا المعاصرة"},
                    "books": ["كتاب التاريخ والجغرافيا 3AS"],
                    "new_changes": "لا تغييرات كبيرة"
                },
                "physical_education": {
                    "content": "أنشطة رياضية متنوعة.",
                    "hours_per_week": 2,
                    "objectives": ["تعزيز اللياقة البدنية", "تنمية الروح الرياضية"],
                    "distribution": {"term1": "رياضات جماعية", "term2": "رياضات فردية", "term3": "اختبارات بدنية"},
                    "books": ["دليل التربية البدنية 3AS"],
                    "new_changes": "لا تغييرات كبيرة"
                },
                "arts": {
                    "content": "الرسم، الموسيقى، المسرح.",
                    "hours_per_week": 2,
                    "objectives": ["تنمية الحس الفني", "تعزيز الإبداع"],
                    "distribution": {"term1": "الرسم", "term2": "الموسيقى", "term3": "المسرح"},
                    "books": ["كتاب الفنون 3AS"],
                    "new_changes": "إضافة مادة الفنون"
                }
            }
        },
        "math": {
            "name": "شعبة الرياضيات",
            "subjects": {
                "arabic": {"content": "الأدب العربي الحديث.", "hours_per_week": 3, "objectives": ["تعزيز الأدب العربي"], "distribution": {"term1": "الأدب", "term2": "المقالة", "term3": "مراجعة"}, "books": ["كتاب اللغة العربية 3AS"], "new_changes": "لا تغييرات كبيرة"},
                "french": {"content": "Textes scientifiques, dissertation.", "hours_per_week": 3, "objectives": ["Lire et analyser des textes scientifiques"], "distribution": {"term1": "Textes", "term2": "Dissertation", "term3": "Commentaire"}, "books": ["Livre de français 3AS"], "new_changes": "Renforcement de l'anglais"},
                "english": {"content": "Scientific texts, grammar, essay writing.", "hours_per_week": 4, "objectives": ["Enhance scientific English"], "distribution": {"term1": "Texts", "term2": "Grammar", "term3": "Essay writing"}, "books": ["English textbook 3AS"], "new_changes": "Increased weekly hours"},
                "math": {"content": "الجبر، التحليل، الهندسة، الاحتمالات.", "hours_per_week": 8, "objectives": ["إتقان الجبر والتحليل"], "distribution": {"term1": "الجبر", "term2": "التحليل", "term3": "الهندسة والاحتمالات"}, "books": ["كتاب الرياضيات 3AS"], "new_changes": "إضافة مادة الإعلام الآلي"},
                "physics": {"content": "الميكانيك، الكهرباء.", "hours_per_week": 6, "objectives": ["فهم الميكانيك والكهرباء"], "distribution": {"term1": "الميكانيك", "term2": "الكهرباء", "term3": "مراجعة"}, "books": ["كتاب الفيزياء 3AS"], "new_changes": "لا تغييرات كبيرة"},
                "informatics": {"content": "Algorithms, Python programming.", "hours_per_week": 2, "objectives": ["Learn programming basics"], "distribution": {"term1": "Algorithms", "term2": "Python programming", "term3": "Projects"}, "books": ["Informatics textbook 3AS"], "new_changes": "New subject added"}
            }
        },
        "tech": {
            "name": "شعبة التقني رياضي",
            "subjects": {
                "arabic": {"content": "الأدب العربي الحديث.", "hours_per_week": 3, "objectives": ["تعزيز الأدب العربي"], "distribution": {"term1": "الأدب", "term2": "المقالة", "term3": "مراجعة"}, "books": ["كتاب اللغة العربية 3AS"], "new_changes": "لا تغييرات كبيرة"},
                "math": {"content": "الجبر، التحليل، الهندسة.", "hours_per_week": 8, "objectives": ["إتقان الجبر والتحليل"], "distribution": {"term1":
