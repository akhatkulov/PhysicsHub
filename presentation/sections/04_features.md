## Imkoniyatlar va Funksionallik

Physics Hub platformasi fizika faniga bag'ishlangan keng qamrovli o'quv ekotizimi bo'lib, foydalanuvchilarga nazariy bilim, amaliy mashq va interaktiv tajriba imkonini bir joyda taqdim etadi. Quyida loyihaning asosiy o'nta yo'nalishi batafsil keltirilgan, har bir modul alohida vazifani bajaradi va birgalikda yaxlit ta'limiy oqimni shakllantiradi.

### Masalalar tizimi
Mavzular bo'yicha tartiblangan fizika masalalari to'plami. Har bir masala sarlavha, asosiy shart, yordamchi izoh, to'g'ri javob va ball qiymatiga ega bo'lib, foydalanuvchi yechgan sayin tajriba orttiradi. Yechilgan masalalar `SolvedProblems` jadvalida belgilanadi, to'plangan ballar esa `MatterPoints` orqali saqlanib boriladi.

### Testlar va viktorinalar
Mavzular kesimida ko'p savolli testlar JSON formatida saqlanadi va avtomatik ravishda baholanadi. Natijalar `QuizPoints` hamda `TestResults` jadvallarida qayd etilib, foydalanuvchi o'z taraqqiyotini va zaif tomonlarini aniq kuzatib boradi.

### Animatsiyalar galereyasi
Fizika qonunlari va hodisalarini ko'rgazmali tushuntiruvchi GIF va MP4 formatidagi animatsiyalar to'plami. Mavzulashgan tartibda joylashtirilib, abstrakt tushunchalarni vizual obrazlar orqali soddalashtiradi va o'zlashtirishni tezlashtiradi.

### AI Savol-Javob
`api.u2s.uz/physics-ai` xizmatiga ulangan suniy intellekt yordamchisi bilan jonli muloqot imkoniyati. Har bir foydalanuvchining chat tarixi `ChatMessage` jadvalida saqlanadi, javoblar esa `marked.js` kutubxonasi orqali Markdown ko'rinishida chiroyli formatlanib chiqariladi.

### Virtual Laboratoriya
HTML va JavaScript texnologiyalarida yozilgan interaktiv simulyatsiyalar `/lab/workspace?src=...&title=...` yo'li orqali embed qilinadi. Hozirda to'rtta laboratoriya ishlamoqda: induktiv qarshilik, sindirish ko'rsatkichi, transformator va yoritilganlik tajribalari.

### Qo'llanma
Formulalar, fizik o'zgarmaslar va ma'lumotnomalar to'plami `HandbookItem` modelida toifalarga ajratilgan. Har bir element kategoriya, sarlavha, asosiy mazmun va qisqa izohga ega bo'lib, tezkor qidiruv va keraksiz vaqt sarfsiz murojaat uchun moslashgan.

### Reyting jadvali
Umumiy ball bo'yicha eng faol o'nta foydalanuvchi ko'rsatiladi. Jadvalda o'rin, daraja (ball/100+1), yechilgan masalalar va topshirilgan testlar soni aks etadi, bu esa sog'lom raqobat muhitini shakllantiradi va motivatsiyani oshiradi.

### Foydalanuvchi profili
Ism, familiya, login, oliy o'quv yurti va xeshlangan parol bilan xavfsiz ro'yxatdan o'tish. Profil sahifasida shaxsiy statistika: jami ballar, daraja, reytingdagi o'rni, yechilgan masalalar va o'tilgan testlar soni jamlanib, o'sish dinamikasini ko'rsatadi.

### Admin paneli
Kontentni boshqarish uchun maxsus interfeys: masala, test, animatsiya va laboratoriyalarni qo'shish, tahrirlash hamda o'chirish funksiyalari. Laboratoriyalarni ZIP arxiv ko'rinishida yuklab, avtomatik chiqarib olish imkoniyati mavjud, shuningdek mavzular va qo'llanma elementlarini boshqarish ham bir nechta klikda bajariladi.

### Moslashuvchan UI
Glassmorphism uslubidagi qorong'i mavzu va mobil qurilmalarga to'liq moslashgan zamonaviy dizayn. Burger-menyu, silliq animatsiyalar, kontrastli ranglar va sezgir kompozitsiya tufayli platforma telefon, planshet hamda kompyuterda bir xil samarali va estetik ishlaydi.

Ushbu o'nta modul birgalikda yaxlit o'quv tajribasini hosil qiladi: nazariyani o'qish, formulani topish, masalani yechish, testdan o'tish, simulyatsiyada sinab ko'rish, AI bilan maslahatlashish va reyting jadvalida o'z o'rnini egallash. Shu tariqa Physics Hub passiv kontent iste'molidan faol o'rganish modeliga o'tishni rag'batlantiradi va o'qituvchilarga ham, o'quvchilarga ham qulay, hozirgi davr talablariga javob beradigan raqamli ta'lim muhitini yaratadi.
