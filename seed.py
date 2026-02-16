from app import create_app, db
from app.models import Theme, Matter, Quiz, HandbookItem

app = create_app("default")
with app.app_context():
    # Add Themes if empty
    if not Theme.query.first():
        themes = [
            Theme(name="Mexanika", about="Harakat, kuch, energiya va impuls qonuniyatlari."),
            Theme(name="Optika", about="Yorug'likning tarqalishi, qaytishi va sinishi."),
            Theme(name="Termodinamika", about="Issiqlik, harorat va ichki energiya jarayonlari."),
            Theme(name="Elektr", about="Zaryadlar, maydonlar va elektr qarshiligi.")
        ]
        db.session.add_all(themes)
        print("Coefficients: Themes added.")
    
    # Add Handbook items if empty
    if not HandbookItem.query.first():
        items = [
            HandbookItem(category="Konstantalar", title="Erkin tushish tezlanishi", content="g = 9.81 m/s²", about="Yer sirtidagi o'rtacha qiymat."),
            HandbookItem(category="Mexanika", title="Nyutonning II-qonuni", content="F = m * a", about="Kuch, massa va tezlanish bog'liqligi."),
            HandbookItem(category="Optika", title="Yorug'lik tezligi", content="c = 3 * 10⁸ m/s", about="Vakuumdagi yorug'lik tezligi.")
        ]
        db.session.add_all(items)
        print("Coefficients: Handbook items added.")

    db.session.commit()
    print("Database seeding complete.")
