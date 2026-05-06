## Loyihaning Tarkibi va Arxitekturasi

"Physics Hub" (fizikaonline.uz) modulli tuzilishga ega bo'lgan, kengaytiriladigan veb-platforma sifatida ishlab chiqilgan. Loyiha qatlamli arxitektura tamoyiliga asoslanadi: foydalanuvchi interfeysi, biznes-mantiq va ma'lumotlar bazasi bir-biridan ajratilgan.

**1. Asosiy modullar (foydalanuvchi qismlari)**

- **Masalalar** — mavzular bo'yicha tasniflangan fizika masalalari to'plami va yechish interfeysi.
- **Testlar** — variantli savollar, avtomatik baholash va natijalarni saqlash.
- **Animatsiyalar (GIFs)** — fizik hodisalarni ko'rgazmali tushuntiruvchi animatsiyalar galereyasi.
- **AI Savol-Javob (chat-ai)** — sun'iy intellekt yordamida fizika bo'yicha tezkor maslahat olish.
- **Qo'llanma (Handbook)** — formulalar, ta'riflar va asosiy nazariy ma'lumotlar ma'lumotnomasi.
- **Virtual Laboratoriya** — brauzerda ishlaydigan 4 ta interaktiv tajriba (lab_workspace).
- **Reyting (Leaderboard)** — foydalanuvchilarning ballari bo'yicha tartiblangan ro'yxati.
- **Profil va Jamoa** — shaxsiy kabinet, yutuqlar va loyiha jamoasi haqida ma'lumot.

**2. Ma'lumotlar bazasi modeli**

SQLAlchemy ORM orqali boshqariladigan asosiy entitiyalar:

- **User** — foydalanuvchi hisoblari, pbkdf2:sha256 algoritmi bilan xeshlangan parollar.
- **Theme / Matter / Quiz** — mavzular, masalalar va testlar ierarxiyasi.
- **Labs** — virtual laboratoriya tajribalari ro'yxati.
- **ChatMessage** — AI bilan suhbat tarixini saqlash.
- **Gifs / HandbookItem** — animatsiyalar va qo'llanma yozuvlari.
- **MatterPoints, QuizPoints, SolvedProblems, TestResults** — foydalanuvchi yutuqlari, ballari va o'sish dinamikasini kuzatish jadvallari.

**3. Backend va Frontend qatlamlari**

- **Backend:** Python Flask freymvorki, `app/main/` ichida tashkil etilgan **Blueprint** strukturasi yordamida marshrutlar (views.py) modullarga bo'lingan.
- **Frontend:** Server tomonida render qilinadigan **Jinja2** shablonlari (`base.html`, `index.html`, `matters.html`, `tests.html`, `lab_workspace.html` va boshq.).
- **Static qatlam:** zamonaviy "glassmorphism" uslubidagi `style.css`, interaktivlik uchun `app.js` va `helper.js`, jamoa rasmlari hamda laboratoriya resurslari.
- **Autentifikatsiya:** Flask-Login orqali sessiya boshqaruvi va xavfsiz kirish.

**4. Admin panel**

`/admin` marshruti orqali kontent boshqaruvi amalga oshiriladi:

- Mavzular, masalalar, testlar, animatsiyalar, laboratoriyalar va qo'llanma yozuvlarini **qo'shish** (`/admin/add_*`).
- Mavjud yozuvlarni **tahrirlash** (`/api/edit_*`) va **o'chirish** (`/api/delete_*`) uchun API endpointlari.
- Foydalanuvchilarni va platformaning umumiy holatini nazorat qilish imkoniyati.

**5. Deployment va infratuzilma**

- **Docker + docker-compose** — `web`, **PostgreSQL** va kunlik avtomatik **backup** konteynerlari.
- **Gunicorn** — Flask ilovasini ishga tushiruvchi WSGI server.
- **Nginx** — teskari proksi-server (reverse proxy) va statik fayllarni uzatish.
- **Certbot (SSL)** — HTTPS shifrlash va xavfsiz ulanish.
- **Avtomatik zaxiralash** — ma'lumotlar bazasining har kuni saqlanishi orqali ma'lumotlar yo'qolishini oldini olish.
