## Innovatsion Yondashuv: AI Mentor + Virtual Laboratoriya

Physics Hub platformasini oddiy elektron kutubxonadan ajratib turuvchi ikkita asosiy innovatsion modul mavjud: **AI Savol-Javob mentori** va **Virtual Laboratoriya**. Aynan shu ikki imkoniyat fizikaonline.uz loyihasini zamonaviy, interaktiv va talabaga yo'naltirilgan ta'lim muhitiga aylantiradi.

### 1. AI Savol-Javob — Shaxsiy Fizika Mentori

**Nima ish qiladi?** Foydalanuvchi istalgan fizika savolini o'zbek tilida yozadi (masalan: "Nyutonning ikkinchi qonunini misol bilan tushuntiring" yoki "Lorenz kuchi formulasi nima?"), AI esa bir necha soniya ichida o'zbek tilida tushunarli, formulalar va misollar bilan boyitilgan javob qaytaradi.

**Qanday ishlaydi?** Frontendda foydalanuvchi savol yuboradi, server `POST /api/chat` endpointi orqali (login talab qilinadi) so'rovni qabul qiladi. Backend bu so'rovni `https://api.u2s.uz/physics-ai` xizmatiga uzatadi va `javob` maydonini oladi. Har bir muloqot `ChatMessage` jadvalida (`user_id`, `message`, `response`, `timestamp`) saqlanadi — shunday qilib talaba o'zining oldingi savollariga qaytib kelishi mumkin. Javob frontendda **marked.js** kutubxonasi yordamida Markdown sifatida render qilinadi: bu AI'ga formulalar, kod bloklari, ro'yxatlar va sarlavhalar qaytarish imkonini beradi.

**Ta'lim uchun ahamiyati:** Talaba kechasi soat 02:00 da uy vazifasini yechayotganda ham javob ololadi — bu **24/7, bepul va bir zumda** ishlaydigan shaxsiy repetitor. O'qituvchining vaqti chegaralangan, lekin AI har bir o'quvchining individual savoliga sabr bilan javob beradi. O'zbek tilidagi javoblar mahalliy ta'lim standartlariga mos keladi va til to'sig'ini yo'q qiladi. Bundan tashqari, muloqot tarixining saqlanishi talabaga o'z o'rganish jarayonini kuzatish, takrorlash va o'qituvchi bilan bo'lishish imkonini beradi.

### 2. Virtual Laboratoriya — Xavfsiz Tajriba Maydoni

**Nima ish qiladi?** Platformada hozirda **4 ta interaktiv simulyatsiya** mavjud:
- **Induktiv qarshilik** — o'zgaruvchan tok zanjirida g'altakning xatti-harakatini o'rganish;
- **Sindirish ko'rsatkichi** — yorug'likning turli muhitlarda sinishini vizual kuzatish;
- **Transformator** — chulg'amlar nisbati va kuchlanish o'zgarishini tahlil qilish;
- **Yoritilganlik** — yorug'lik manbai va masofa ta'sirini o'lchash.

**Qanday ishlaydi?** Har bir laboratoriya alohida HTML/JS modul sifatida `/static/labs/<slug>/` katalogida joylashgan. Foydalanuvchi `/lab/workspace?src=...&title=...` sahifasi orqali laboratoriyani **iframe** ko'rinishida ochadi va to'liq ekranda ishlaydi. Eng muhimi — admin panelda yangi laboratoriya **ZIP fayl** ko'rinishida yuklanadi: `views.py` ichidagi `add_lab_v2` funksiyasi arxivni avtomatik ochadi, fayllarni joylashtiradi va bazaga yozadi. Ya'ni dasturchi aralashuvisiz yangi tajribalarni qo'shish mumkin.

**Ta'lim uchun ahamiyati:** Ko'pgina maktab va kollejlarda laboratoriya jihozlari yetishmaydi yoki eskirgan. Virtual laboratoriya bu muammoni hal qiladi — talaba **laborantsiz, qimmat qurilmalarsiz va xavfsiz tarzda** rezistor qiymatini, sindirish burchagini yoki transformator chastotasini o'zgartirib, natijani real vaqtda ko'rishi mumkin. Bu "o'qib o'rganish"dan "qilib o'rganish"ga o'tishni ta'minlaydi va fizik intuitsiyani rivojlantiradi. Tajribani istalgan vaqtda qayta o'tkazish, parametrlarni ekstremal qiymatlarga o'zgartirish va xato qilishdan qo'rqmasdan o'rganish — bu klassik laboratoriyada deyarli imkonsiz bo'lgan erkinlikdir.

### Xulosa

AI Mentor talabaning **savollariga**, Virtual Laboratoriya esa uning **qiziqishi va tajribalariga** javob beradi. Birgalikda ular fizikaonline.uz'ni passiv kontent saytidan **faol o'qitish ekotizimiga** aylantiradi.
