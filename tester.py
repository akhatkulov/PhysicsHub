from flasky import db,app 
from app.models import Matter,Quiz,Theme

problems = [
    {
        "title": "Tezlikni hisoblash",
        "main": "Jism 100 metr masofani 5 sekundda bosib o‘tdi. Uning o‘rtacha tezligi qancha?",
        "helper": "O‘rtacha tezlik v = s / t formulasi bilan hisoblanadi.",
        "correct": "20 m/s",
        "theme": "Mexanika",
        "ball": 1
    },
    {
        "title": "Tezlanishni hisoblash",
        "main": "Jism 4 sekund ichida 10 m/s tezlikdan 30 m/s tezlikka erishdi. Uning tezlanishini toping.",
        "helper": "Tezlanish a = (v - v0) / t formulasi bilan hisoblanadi.",
        "correct": "5 m/s²",
        "theme": "Mexanika",
        "ball": 1
    },
    {
        "title": "Erkin tushish masofasi",
        "main": "Jism erkin tushib, 3 sekund harakat qildi. U qanchalik pastga tushadi? (g = 9.8 m/s²)",
        "helper": "S = (1/2) * g * t² formulasi bilan hisoblanadi.",
        "correct": "44.1 m",
        "theme": "Mexanika",
        "ball": 1
    },
    {
        "title": "Newton birinchi qonuni",
        "main": "Jismga hech qanday tashqi kuch ta’sir qilmasa, u qanday harakat qiladi?",
        "helper": "Newtonning birinchi qonuniga ko‘ra, tashqi kuch bo‘lmasa, jism o‘z harakatini o‘zgartirmaydi.",
        "correct": "Tinch yoki tekis harakat qiladi",
        "theme": "Mexanika",
        "ball": 1
    },
    {
        "title": "Newton ikkinchi qonuni",
        "main": "Massasi 8 kg bo‘lgan jismga 40 N kuch ta’sir qilmoqda. Uning tezlanishini toping.",
        "helper": "Newtonning ikkinchi qonuniga ko‘ra, a = F / m.",
        "correct": "5 m/s²",
        "theme": "Mexanika",
        "ball": 1
    },
    {
        "title": "Newton uchinchi qonuni",
        "main": "Stolga qo‘yilgan kitob qanday kuch ta’sir qiladi?",
        "helper": "Newtonning uchinchi qonuniga ko‘ra, har bir harakatga teskari yo‘nalishda teng kuch ta’sir qiladi.",
        "correct": "Stol kitobga teskari yo‘nalishda teng kuch bilan ta’sir qiladi.",
        "theme": "Mexanika",
        "ball": 1
    },
    {
        "title": "Ishni hisoblash",
        "main": "Massasi 10 kg bo‘lgan jism 5 m balandlikka ko‘tarildi. Ishni hisoblang. (g = 9.8 m/s²)",
        "helper": "Ish W = m * g * h formulasi bilan hisoblanadi.",
        "correct": "490 J",
        "theme": "Mexanika",
        "ball": 1
    },
    {
        "title": "Kinetik energiya",
        "main": "10 kg massali jism 4 m/s tezlik bilan harakatlanmoqda. Uning kinetik energiyasi qancha?",
        "helper": "Kinetik energiya Ek = (1/2) * m * v² formulasi bilan hisoblanadi.",
        "correct": "80 J",
        "theme": "Mexanika",
        "ball": 1
    },
    {
        "title": "Potensial energiya",
        "main": "5 kg massali jism 2 m balandlikda turibdi. Uning potensial energiyasi qancha? (g = 9.8 m/s²)",
        "helper": "Potensial energiya Ep = m * g * h formulasi bilan hisoblanadi.",
        "correct": "98 J",
        "theme": "Mexanika",
        "ball": 1
    },
    {
        "title": "Impulsni hisoblash",
        "main": "Jismning massasi 3 kg, tezligi 6 m/s. Uning impulsi qancha?",
        "helper": "Impuls P = m * v formulasi bilan hisoblanadi.",
        "correct": "18 kg·m/s",
        "theme": "Mexanika",
        "ball": 1
    }
]

with app.app_context():
    for problem in problems:
        new_problem = Matter(
            title=problem["title"],
            main=problem["main"],
            helper=problem["helper"],
            correct=problem["correct"],
            theme=problem["theme"].lower(),
            ball=problem["ball"]
        )
        db.session.add(new_problem)

    db.session.commit()


# quiz_data = """[
#         {
#             "id": 1,
#             "question": "Python dasturlash tilida eng asosiy o'zgaruvchi turi qaysi?",
#             "options": ["String", "Integer", "List", "Boolean"],
#             "answer": "Integer",
#             "ball": 1
#         },
#         {
#             "id": 2,
#             "question": "HTML nima uchun ishlatiladi?",
#             "options": [
#                 "Web sahifalarni yaratish",
#                 "Dasturlarni yozish",
#                 "Ma'lumotlarni saqlash",
#                 "Chizma yaratish"
#             ],
#             "answer": "Web sahifalarni yaratish",
#             "ball": 1
#         }
#     ]"""

# with app.app_context():
#     new_quiz = Quiz(title="poxuy_masmi",theme="dinamika",status=True,data=quiz_data)
#     db.session.add(new_quiz)
#     db.session.commit()
# print("Barcha masalalar bazaga yuklandi!")

# # Fizika bo‘yicha mavzular
# themes = [
#     {"name": "kinematika", "about": "Jismning harakati va tezlanish qonunlari."},
#     {"name": "dinamika", "about": "Nyuton qonunlari va kuchlar."},
#     {"name": "ish_va_energiya", "about": "Ish, energiya va quvvat haqida."},
#     {"name": "termodinamika", "about": "Issiqlik va energiya almashinuvi."},
#     {"name": "elektr_magnit", "about": "Elektr va magnit hodisalari."},
# ]

# with app.app_context():

#     # Ma'lumotlar bazasiga qo'shish
#     for theme in themes:
#         db.session.add(Theme(name=theme["name"], about=theme["about"]))

#     for quiz in quizzes:
#         db.session.add(Quiz(
#             title=quiz["title"], 
#             theme=quiz["theme"], 
#             data=quiz["data"]
#         ))

#     db.session.commit()
print("Barcha ma'lumotlar qo'shildi!")
