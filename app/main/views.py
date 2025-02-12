from flask import render_template, session, redirect, url_for, request, flash, current_app,jsonify
from .. import db
from ..models import User,Theme,Matter,get_all_themes
from ..email import send_email
from . import main
from .forms import SignInForm, SignUpForm,UpdateData
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, logout_user, login_user,current_user
import json

@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@main.route("/admin")
@login_required
def admin():
    if current_user.username == 'admin':
        return render_template('admin/index.html')
    else:
        return render_template('404.html')

@main.post("/admin/add_matter")
@login_required
def add_matter():
    res_data = json.loads(request.data)
    title = res_data['title']
    main = res_data['main']
    helper = res_data['helper']
    theme = res_data['theme']
    correct = res_data['correct']
    status = True 
    if current_user.username == 'admin':
        new_matter = Matter(title=title,main=main,helper=helper,theme=theme,correct=correct,status=True)
        db.session.add(new_matter)
        db.session.commit()
        return "Yeah!!!"
    else:
        return render_template('404.html')

# @main.get("/admin/add_quiz")
# def add_matter():
#     if current_user.username == 'admin':
#         return "Hi"
#     else:
#         return render_template('404.html')

@main.get("/admin/add_theme")
def add_theme():
    res_data = json.loads(request.data)
    name = res_data['name']
    about = res_data['about']
    if current_user.username == 'admin':
        new_theme = Theme(name=name,about=about)
        db.session.add(new_theme)
        db.session.commit()
        return "Yeah!!!"
    else:
        return render_template('404.html')


@main.route('/themes', methods=['GET'])
def get_themes():
    themes = [
        {"name": "minimalist", "about": "Soddalik va tartibga asoslangan dizayn."},
        {"name": "dark Mode", "about": "Qorong'u fon va yorqin matnlar bilan qulay ko'rinish."},
        {"name": "Cyberpunk", "about": "Neon ranglar va futuristik ko'rinish."},
        {"name": "Classic", "about": "An'anaviy va rasmiy dizayn."}
    ]
    return jsonify(themes)


@main.route('/matters/')
def matters():
    themes = [
        {"name": "Mexanika", "about": "Jismlarning harakati, kuchlar va muvozanat qonunlarini o‘rganadi. Masalan, Nyuton mexanikasi va klassik mexanika."},
        {"name": "Termodinamika", "about": "Issiqlik, energiya va ularning o‘zaro bog‘liqligini tadqiq qiladi. Masalan, issiqlik mashinalari va entropiya tushunchalari."},
        {"name": "Elektromagnetizm", "about": "Elektr va magnit maydonlarini o‘rganadi. Masalan, Maksvell tenglamalari, elektromagnit to‘lqinlar."},
        {"name": "Optika", "about": "Yorug‘likning tarqalishi, sinishi, aks etishi kabi xususiyatlarini o‘rganadi. Masalan, linzalar, nurlar interferensiyasi."},
        {"name": "Kvant mexanikasi", "about": "Mikro dunyodagi zarrachalar harakati va xususiyatlarini o‘rganadi. Masalan, elektronlarning holati, superpozitsiya prinsipi."},
        {"name": "Nisbiylik nazariyasi", "about": "Katta tezlik va gravitatsiya ta’siridagi jism harakatini o‘rganadi. Masalan, vaqtning nisbiyligi, E=mc² tenglamasi."},
        {"name": "Yadro fizikasi", "about": "Atom yadrosi va yadro reaksiyalarini o‘rganadi. Masalan, radioaktivlik, yadroviy energiya."},
        {"name": "Zarralar fizikasi", "about": "Elementar zarralar va ularning o‘zaro ta’sirini tadqiq qiladi. Masalan, kvarklar, leptonlar, Standart model."},
        {"name": "Kondensatlangan muhit fizikasi", "about": "Qattiq jism va suyuqliklarning xossalarini o‘rganadi. Masalan, yarimo‘tkazgichlar, supero‘tkazuvchanlik."},
        {"name": "Astrofizika", "about": "Kosmik jismlar va ularning fizik qonuniyatlarini o‘rganadi. Masalan, qora tuynuklar, koinot kengayishi."}
    ]
    return render_template('matters.html',themes=themes)

@main.route("/tests/")
def tests():
    #themes = get_all_themes()
    themes = [
        {"name": "Mexanika", "about": "Jismlarning harakati, kuchlar va muvozanat qonunlarini o‘rganadi. Masalan, Nyuton mexanikasi va klassik mexanika."},
        {"name": "Termodinamika", "about": "Issiqlik, energiya va ularning o‘zaro bog‘liqligini tadqiq qiladi. Masalan, issiqlik mashinalari va entropiya tushunchalari."},
        {"name": "Elektromagnetizm", "about": "Elektr va magnit maydonlarini o‘rganadi. Masalan, Maksvell tenglamalari, elektromagnit to‘lqinlar."},
        {"name": "Optika", "about": "Yorug‘likning tarqalishi, sinishi, aks etishi kabi xususiyatlarini o‘rganadi. Masalan, linzalar, nurlar interferensiyasi."},
        {"name": "Kvant mexanikasi", "about": "Mikro dunyodagi zarrachalar harakati va xususiyatlarini o‘rganadi. Masalan, elektronlarning holati, superpozitsiya prinsipi."},
        {"name": "Nisbiylik nazariyasi", "about": "Katta tezlik va gravitatsiya ta’siridagi jism harakatini o‘rganadi. Masalan, vaqtning nisbiyligi, E=mc² tenglamasi."},
        {"name": "Yadro fizikasi", "about": "Atom yadrosi va yadro reaksiyalarini o‘rganadi. Masalan, radioaktivlik, yadroviy energiya."},
        {"name": "Zarralar fizikasi", "about": "Elementar zarralar va ularning o‘zaro ta’sirini tadqiq qiladi. Masalan, kvarklar, leptonlar, Standart model."},
        {"name": "Kondensatlangan muhit fizikasi", "about": "Qattiq jism va suyuqliklarning xossalarini o‘rganadi. Masalan, yarimo‘tkazgichlar, supero‘tkazuvchanlik."},
        {"name": "Astrofizika", "about": "Kosmik jismlar va ularning fizik qonuniyatlarini o‘rganadi. Masalan, qora tuynuklar, koinot kengayishi."}
    ]

    return render_template('tests.html',themes=themes)

@main.route('/matters/<name>')
def show_matter(name):
    matters = Matter.query.filter(Matter.theme == name).all()
    return render_template('show_matter.html', name=name, matters=matters)

@main.route('/matters/<theme>/<int:matter_id>', methods=["GET", "POST"])
def calc_matter(theme, matter_id):
    matter = Matter.query.filter_by(id=matter_id).first()

    if not matter: 
        abort(404)

    if request.method == 'POST':
        user_answer = request.form['answer'].strip()
        correct_answer = matter.correct

        if user_answer == correct_answer:
            flash(f"✅ To‘g‘ri javob! ({user_answer})", "success")
        else:
            flash(f"❌ Noto‘g‘ri javob! To‘g‘ri javob: {correct_answer}", "danger")

        return redirect(url_for('main.calc_matter', theme=theme, matter_id=matter_id)) 

    return render_template('calc_matter.html', problem=matter,theme=theme)



@main.route("/home")
def home_page():
    return "Hey"

@main.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        try:
            name = form.name.data
            surname = form.surname.data
            username = form.username.data
            university = form.university.data
            password = form.password.data

            user = User.query.filter_by(username=username).first()
            if user:
                flash("Bu taxallusda foydalanuvchi mavjud.", "error")
                return redirect(url_for("main.signup"))

            hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
            new_user = User(name=name, surname=surname, username=username, university=university, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            flash('Ma\'lumotlar muvaffaqiyatli yuborildi!', 'success')
            return redirect(url_for("main.login_page"))

        except Exception as e:
            current_app.logger.error(f"Signup error: {e}")
            flash("Noma'lum xatolik yuz berdi, iltimos qayta urinib ko'ring.", "error")
            return redirect(url_for("main.signup"))
    return render_template('signup.html', form=form)

@main.route("/signin", methods=["GET", "POST"])
def login_page():
    form = SignInForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if user and user.password and check_password_hash(user.password, password):
            login_user(user)
            flash("Kirish muvaffaqiyatli!", "success")
            if current_user.username == "admin":
                return redirect(url_for('main.admin'))
            else:
                return redirect(url_for('main.home_page'))

        flash("Taxallus yoki parol noto'g'ri", "error")
    return render_template("login.html", form=form)

@main.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = UpdateData()
    if form.validate_on_submit():
        print("olindi")
        # Formdagi ma'lumotlarni olish
        name = form.name.data
        surname = form.surname.data
        university = form.university.data
        password = form.password.data

        # current_user ob'ekti orqali malumotlarni yangilash
        user = current_user
        user.name = name
        user.surname = surname
        user.university = university

        if password:
            user.password = generate_password_hash(password)

        try:
            db.session.commit()  # Malumotlarni bazaga saqlash
            flash('Malumotlar yangilandi!', 'success')
        except Exception as e:
            db.session.rollback()  # Agar xato bo'lsa, rollback qilish
            flash(f'Error updating profile: {str(e)}', 'danger')

        return redirect(url_for('main.profile'))  # Yangi sahifaga qaytish

    return render_template('profile.html', user=current_user, form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Siz muvaffaqiyatli chiqdingiz.", "success")
    return redirect(url_for('main.login_page'))
