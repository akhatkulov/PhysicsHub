from flasky import db, app
from app.models import HandbookItem

handbook_data = [
    {
        "category": "O'zgarmaslar",
        "title": "Erkin tushish tezlanishi",
        "content": "g ≈ 9.81 m/s²",
        "about": "Yer sirtida jismlarning erkin tushish tezlanishi."
    },
    {
        "category": "O'zgarmaslar",
        "title": "Yorug'lik tezligi",
        "content": "c ≈ 3 * 10^8 m/s",
        "about": "Vakuumda yorug'likning tarqalish tezligi."
    },
    {
        "category": "Mexanika",
        "title": "Nyutonning ikkinchi qonuni",
        "content": "F = m * a",
        "about": "Jismga ta'sir etuvchi kuch uning massasi va tezlanishi ko'paytmasiga teng."
    },
    {
        "category": "Mexanika",
        "title": "Kinetik energiya",
        "content": "Ek = (m * v²) / 2",
        "about": "Harakatdagi jismning energiyasi."
    },
    {
        "category": "Termodinamika",
        "title": "Ideal gaz holat tenglamasi",
        "content": "P * V = n * R * T",
        "about": "Mendeleyev-Klapeyron tenglamasi."
    },
    {
        "category": "Elektr",
        "title": "Om qonuni",
        "content": "I = U / R",
        "about": "Zanjir qismidagi tok kuchi kuchlanishga to'g'ri proportsional."
    }
]

with app.app_context():
    for item in handbook_data:
        new_item = HandbookItem(
            category=item["category"],
            title=item["title"],
            content=item["content"],
            about=item["about"]
        )
        db.session.add(new_item)
    db.session.commit()
    print("Handbook ma'lumotlari muvaffaqiyatli qo'shildi!")
