from flask import (
    render_template, session, redirect, url_for, request, flash, current_app,
    jsonify, abort
)
from .. import db
from ..models import (
    User, Theme, Matter, Quiz,
    get_all_themes, save_user_progress, check_history,
    get_leaderboard, get_matter, get_quiz,Gifs,get_animation_func,Labs,get_labs
)
from ..email import send_email
from . import main
from .forms import SignInForm, SignUpForm, UpdateData
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, logout_user, login_user, current_user
import json
from werkzeug.utils import secure_filename
from datetime import datetime
import os

ALLOWED_EXTENSIONS = {'gif', 'mp4'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@main.route("/", methods=["GET", "POST"])
def home_page():
    return render_template("index.html")
    
@main.route("/gifs")
def show_gifs():
    gifs = Gifs.query.all()
    return render_template("gifs.html", gifs=gifs)

@main.route("/chat")
def chat():
    return render_template("chat-ai.html")

@main.route("/admin")
@login_required
def admin():
    if not current_user.username == "admin":
        abort(404)
    return render_template("admin/index.html")

@main.route("/admin/add_animation", methods=["POST"])
@login_required
def add_get():
    if current_user.username != "admin":
        abort(403)

    title = request.form.get("title")
    about = request.form.get("about")
    theme = request.form.get("theme")
    media = request.files.get("gif")  # gif yoki mp4 shu joyga keladi

    if not media or media.filename == '':
        return "No file provided", 400

    if allowed_file(media.filename):
        filename = secure_filename(f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{media.filename}")
        save_dir = os.path.join(current_app.root_path, 'static', 'gifs')
        os.makedirs(save_dir, exist_ok=True)  # agar yo'q bo‘lsa papkani yaratadi
        save_path = os.path.join(save_dir, filename)
        media.save(save_path)

        # Konsolga chiqarish
        res = {
            "title": title,
            "about": about,
            "theme": theme,
            "media": f"gifs/{filename}"
        }
        new_gif = Gifs(name=res["title"],about=res["about"],gif_path=res["media"],theme=res["theme"])
        db.session.add(new_gif)
        db.session.commit()
        return "Good"
    else:
        return "Only .gif or .mp4 files are allowed", 400

@main.route("/admin/add_matter", methods=["POST"])
@login_required
def add_matter():
    if current_user.username != "admin":
        abort(403)
    data = request.get_json(force=True)
    new_matter = Matter(
        title=data["title"],
        main=data["main"],
        helper=data["helper"],
        theme=data["theme"],
        correct=data["correct"],
        status=True,
        ball=int(data["ball"])
    )
    db.session.add(new_matter)
    db.session.commit()
    return jsonify({"message": "Matter added successfully"}), 201


@main.route("/admin/add_quiz", methods=["POST"])
@login_required
def add_quiz():
    if current_user.username != "admin":
        abort(403)
    data = request.get_json(force=True)
    print("quiz:::::g",data)
    if not data.get("title") or not data.get("theme"):
        return jsonify({"error": "Title va Theme kerak"}), 400
    new_quiz = Quiz(
        title=data["title"],
        theme=data["theme"].lower(),
        status=True,
        data=json.dumps(data.get("data", {}))
    )
    db.session.add(new_quiz)
    db.session.commit()
    return jsonify({"message": "Quiz added successfully"}), 201


@main.route("/admin/add_theme", methods=["POST"])
@login_required
def add_theme():
    if current_user.username != "admin":
        abort(403)
    data = request.get_json(force=True)
    new_theme = Theme(name=data["name"], about=data["about"])
    db.session.add(new_theme)
    db.session.commit()
    return jsonify({"message": "Theme added successfully"}), 201


@main.route("/api/themes", methods=["GET"])
def get_themes():
    return jsonify(get_all_themes())

@main.route("/api/get_animation",methods=["GET"])
def get_animation_list():
    prefix = request.args.get("prefix", "").lower()
    return jsonify(get_animation_func(prefix))

@main.route("/api/get_labs",methods=["GET"])
def get_labs_list():
    prefix = request.args.get("prefix", "").lower()
    return jsonify(get_labs(prefix))

@main.route("/api/get_quiz", methods=["GET"])
def get_quiz_list():
    prefix = request.args.get("prefix", "").lower()
    return jsonify(get_quiz(prefix))


@main.route("/api/get_matter", methods=["GET"])
def get_matter_list():
    prefix = request.args.get("prefix", "").lower()
    return jsonify(get_matter(prefix))


@main.route("/api/delete_animation/<int:item_id>",methods=["DELETE"])
@login_required
def delete_animation(item_id):
    if current_user.username !="admin":
        abort(403)
    item = Gifs.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Item deleted successfully"}), 200

@main.route("/api/delete_theme/<int:item_id>", methods=["DELETE"])
@login_required
def delete_theme(item_id):
    if current_user.username != "admin":
        abort(403)
    item = Theme.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Item deleted successfully"}), 200


@main.route("/api/delete_quiz/<int:item_id>", methods=["DELETE"])
@login_required
def delete_quiz(item_id):
    if current_user.username != "admin":
        abort(403)
    item = Quiz.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Item deleted successfully"}), 200


@main.route("/api/delete_matter/<int:item_id>", methods=["DELETE"])
@login_required
def delete_matter(item_id):
    if current_user.username != "admin":
        abort(403)
    item = Matter.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Item deleted successfully"}), 200


@main.route("/api/edit_quiz", methods=["PUT"])
@login_required
def edit_quiz():
    if current_user.username != "admin":
        abort(403)
    data = request.get_json(force=True)
    quiz = Quiz.query.get_or_404(data.get("id"))
    quiz.title = data.get("title", quiz.title)
    quiz.theme = data.get("theme", quiz.theme).lower()
    quiz.data = json.dumps(data.get("data", []))
    quiz.status = bool(data.get("status", quiz.status))
    db.session.commit()
    return jsonify({"status": "done"}), 200


@main.route("/api/toggle_quiz_status", methods=["PUT"])
@login_required
def toggle_quiz_status():
    if current_user.username != "admin":
        abort(403)
    data = request.get_json(force=True)
    quiz = Quiz.query.get_or_404(data.get("id"))
    quiz.status = not quiz.status
    db.session.commit()
    return jsonify({"status": "done", "new_status": quiz.status}), 200


@main.route("/api/edit_matter", methods=["PUT"])
@login_required
def edit_matter():
    if current_user.username != "admin":
        abort(403)
    data = request.get_json(force=True)
    matter = Matter.query.get_or_404(data.get("id"))
    matter.title = data.get("title", matter.title)
    matter.main = data.get("main", matter.main)
    matter.helper = data.get("helper", matter.helper)
    matter.theme = data.get("theme", matter.theme)
    matter.correct = data.get("correct", matter.correct)
    matter.ball = int(data.get("ball", matter.ball))
    matter.status = bool(data.get("status", matter.status))
    db.session.commit()
    return jsonify({"status": "done"}), 200


@main.route("/api/toggle_matter_status", methods=["PUT"])
@login_required
def toggle_matter_status():
    if current_user.username != "admin":
        abort(403)
    data = request.get_json(force=True)
    matter = Matter.query.get_or_404(data.get("id"))
    matter.status = not matter.status
    db.session.commit()
    return jsonify({"status": "done", "new_status": matter.status}), 200


@main.route("/matters/")
def matters():
    return render_template("matters.html", themes=get_all_themes())


@main.route("/tests/")
def tests():
    return render_template("tests.html", themes=get_all_themes())


@main.route("/tests/<name>")
def show_tests(name):
    tests = Quiz.query.filter_by(theme=name).all()
    user_id = current_user.id
    quiz_status = {test.id: check_history(user_id, test.id, "quiz") for test in tests}
    return render_template("show_tests.html", name=name, tests=tests, quiz_status=quiz_status)


@main.route("/tests/<theme>/<int:quiz_id>", methods=["GET", "POST"])
def calc_test(theme, quiz_id):
    quiz = Quiz.query.get_or_404(int(quiz_id))
    questions = json.loads(quiz.data)
    if request.method == "POST":
        answers = {f'question-{q["id"]}': request.form.get(f'question-{q["id"]}') for q in questions}
        users_ball = sum(int(q["ball"]) for q in questions if answers.get(f'question-{q["id"]}') == q["answer"])
        score = sum(1 for q in questions if answers.get(f'question-{q["id"]}') == q["answer"])
        save_user_progress(current_user.id, quiz.id, users_ball, "quiz")
        return render_template("result_test.html", ball=users_ball, score=score, total=len(questions))
    return render_template("calc_test.html", questions=questions, theme=theme)


@main.route("/matters/<name>")
def show_matter(name):
    page = request.args.get("page", 1, type=int)
    per_page = 10
    matters = Matter.query.filter_by(theme=name).paginate(page=page, per_page=per_page, error_out=False)
    user_id = current_user.id
    for matter in matters.items:
        matter.solved = check_history(user_id, matter.id, "matter")["status"]
    return render_template("show_matter.html", name=name, matters=matters)


@main.route("/matters/<theme>/<int:matter_id>", methods=["GET", "POST"])
def calc_matter(theme, matter_id):
    matter = Matter.query.get_or_404(matter_id)
    if request.method == "POST":
        user_answer = request.form["answer"].strip()
        if user_answer == matter.correct:
            save_user_progress(current_user.id, matter.id, matter.ball, "matter")
            flash(f"✅ To‘g‘ri javob! ({user_answer})", "success")
        else:
            flash(f"❌ Noto‘g‘ri javob... To‘g‘ri javob: {matter.correct}", "danger")
    return render_template("calc_matter.html", matter=matter, theme=theme)




@main.route("/team")
def team():
    return render_template("team.html")


@main.route("/leaderboard")
def leaderboard():
    top_users = get_leaderboard()
    ranked_users = [
        (rank + 1, user, total_points)
        for rank, (user, total_points) in enumerate(top_users)
    ]

    print("top_users:", top_users)
    print("ranked_users:", ranked_users)

    return render_template("leaderboard.html", ranked_users=ranked_users)


@main.route("/lab")
def lab():
    return render_template("lab_list.html")

@main.route("/labaratory/<id>")
def lab_page(id):
    return render_template(f"lab/{id}/index.html")


@main.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        try:
            name = form.name.data
            surname = form.surname.data
            username = form.username.data.replace(" ", "")
            university = form.university.data
            password = form.password.data

            user = User.query.filter_by(username=username).first()
            if user:
                flash("Bu taxallusda foydalanuvchi mavjud.", "error")
                return redirect(url_for("main.signup"))

            hashed_password = generate_password_hash(
                password, method="pbkdf2:sha256", salt_length=8
            )
            new_user = User(
                name=name,
                surname=surname,
                username=username,
                university=university,
                password=hashed_password,
            )
            db.session.add(new_user)
            db.session.commit()

            flash("Ma'lumotlar muvaffaqiyatli yuborildi!", "success")
            return redirect(url_for("main.login_page"))

        except Exception as e:
            current_app.logger.error(f"Signup error: {e}")
            flash("Noma'lum xatolik yuz berdi, iltimos qayta urinib ko'ring.", "error")
            return redirect(url_for("main.signup"))
    return render_template("signup.html", form=form)


@main.route("/signin", methods=["GET", "POST"])
def login_page():
    form = SignInForm()
    if form.validate_on_submit():
        username = form.username.data.replace(" ", "")
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if user and user.password and check_password_hash(user.password, password):
            login_user(user)
            flash("Kirish muvaffaqiyatli!", "success")
            if current_user.username == "admin":
                return redirect(url_for("main.admin"))
            else:
                return redirect(url_for("main.home_page"))

        flash("Taxallus yoki parol noto'g'ri", "error")
    return render_template("login.html", form=form)


@main.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = UpdateData()
    user = current_user
    ball = user.points
    if form.validate_on_submit():
        print("olindi")
        name = form.name.data
        surname = form.surname.data
        university = form.university.data
        password = form.password.data

        user.name = name
        user.surname = surname
        user.university = university
        if password:
            user.password = generate_password_hash(password)

        try:
            db.session.commit()
            flash("Malumotlar yangilandi!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Error updating profile: {str(e)}", "danger")

        return redirect(url_for("main.profile"))

    return render_template("profile.html", ball=ball, user=current_user, form=form)


@main.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Siz muvaffaqiyatli chiqdingiz.", "success")
    return redirect(url_for("main.login_page"))