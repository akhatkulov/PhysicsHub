## Loyiha Qaysi Texnologiyalar Asosida Qurilgan?

Physics Hub (fizikaonline.uz) zamonaviy, ishonchli va kengaytiriladigan texnologiyalar steki asosida qurilgan. Quyida loyihaning har bir qatlamida ishlatilgan asosiy vositalar keltirilgan.

### Backend (Server qismi)
- **Python 3.9** — asosiy dasturlash tili.
- **Flask 2.0.3** — yengil va moslashuvchan mikroframework.
- **Flask-SQLAlchemy 2.5.1** va **SQLAlchemy 1.4.52** — ma'lumotlar bazasi bilan ishlash uchun ORM.
- **Flask-Login 0.6.3** — foydalanuvchi autentifikatsiyasi va sessiyalar.
- **Flask-WTF 1.0.1** + **WTForms 3.0.1** — formalar va xavfsiz validatsiya (CSRF himoyasi bilan).
- **Flask-Migrate 3.1.0** (Alembic) — ma'lumotlar bazasi migratsiyalari.
- **Flask-Bootstrap 3.3.7.1** — UI integratsiyasi.
- **Flask-Mail 0.9.1** — email yuborish (tasdiqlash, parol tiklash).
- **Flask-Moment 1.0.5** — sana va vaqtni qulay ko'rsatish.
- **Werkzeug 2.0.3** — xavfsizlik vositalari (parollarni `pbkdf2:sha256` bilan hashlash).
- **Jinja2 3.0.3** — HTML shablonlar dvigateli.
- **Gunicorn 21.2.0** — production muhiti uchun WSGI server.
- **requests 2.31.0** — AI API'ga HTTP so'rovlar yuborish.
- **BeautifulSoup4 4.12.3** — HTML parsing.
- **python-slugify 8.0.4** — chiroyli URL slug'lar yaratish.

### Ma'lumotlar bazasi
- **PostgreSQL 15-alpine** — production muhitida ishlatiladigan ishonchli relyatsion baza.
- **psycopg2-binary 2.9.9** — Python uchun PostgreSQL drayveri.
- **SQLite** — lokal development uchun yengil variant.
- **prodrigestivill/postgres-backup-local** — har kuni avtomatik zaxira nusxalar oladigan alohida konteyner.

### Frontend (Foydalanuvchi qismi)
- **HTML5** va **CSS3** — sahifaning tuzilishi va custom dizayn.
- **Vanilla JavaScript** (`helper.js`, `app.js`) — interaktivlik (kutubxonalarsiz).
- **Bootstrap** (Flask-Bootstrap orqali) — responsive grid va komponentlar.
- **Font Awesome 6.5.1** — ikonalar (CDN orqali).
- **marked.js** — AI chat'da Markdown javoblarni render qilish.
- **Google Fonts** — Plus Jakarta Sans (matn) va JetBrains Mono (kod).
- **Custom dark "glassmorphism" dizayn** — `backdrop-filter`, gradientlar va glass-card uslubi.

### DevOps va infratuzilma
- **Docker** + **docker-compose** — uchta servis (`web`, `db`, `db-backup`) bir xil muhitda ishlaydi.
- **Nginx** — reverse proxy, statik fayllar va trafikni boshqarish (`sites-available` / `sites-enabled`).
- **Let's Encrypt** + **Certbot** — bepul va avtomatik SSL sertifikatlari.
- **systemd** (`physicshub.service`) — serverda doimiy ishlash va avtomatik qayta ishga tushirish.
- **Domain**: fizikaonline.uz.

### Tashqi integratsiyalar
- **AI API: `api.u2s.uz/physics-ai`** — fizika bo'yicha sun'iy intellekt mentor, foydalanuvchilar savollariga real vaqt rejimida javob beradi.

### Nega aynan shu texnologiyalar?
**Flask** tanlandi, chunki u yengil, sodda va moslashuvchan — kichik jamoa uchun tezda prototip yasash va keyin bemalol kengaytirishga imkon beradi. **PostgreSQL** ishonchli, ACID-mos va katta hajmdagi o'quv kontentini bemalol ko'taradigan sanoat standartidagi baza hisoblanadi, kunlik avtomatik backup esa ma'lumot xavfsizligini ta'minlaydi. **Docker** + **docker-compose** loyiha development, test va production muhitlarida bir xil va qayta tiklanuvchan ishlashini kafolatlaydi, deploy jarayonini bir buyruqqa tushiradi. **Nginx** + **Let's Encrypt** + **Gunicorn** kombinatsiyasi esa yuqori tezlik, HTTPS xavfsizligi va barqarorlikni ta'minlab, fizikaonline.uz platformasini O'zbekistondagi minglab o'quvchilarga ishonchli yetkazib berishga xizmat qiladi.
