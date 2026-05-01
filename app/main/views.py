from flask import (
    render_template, session, redirect, url_for, request, flash, current_app,
    jsonify, abort
)
from .. import db
from ..email import send_email
from . import main
from .forms import SignInForm, SignUpForm, UpdateData
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, logout_user, login_user, current_user
import json
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import zipfile
import shutil
import requests
from ..models import (
    get_leaderboard, get_matter, get_quiz, Gifs, get_animation_func, Labs, get_labs,
    get_lab_list, HandbookItem, ChatMessage, User, Matter, Quiz, Theme, MatterPoints, QuizPoints, 
    SolvedProblems, TestResults, check_history, save_user_progress, get_all_themes
)

ALLOWED_EXTENSIONS = {'gif', 'mp4', 'jpg', 'jpeg', 'png'}

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
@login_required
def chat():
    # Load chat history for the user
    history = ChatMessage.query.filter_by(user_id=current_user.id).order_by(ChatMessage.timestamp).all()
    return render_template("chat-ai.html", history=history)

@main.route("/api/chat", methods=["POST"])
@login_required
def chat_api():
    data = request.get_json(force=True)
    user_message = data.get("message", "").strip()
    
    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    try:
        # Call external AI API
        response = requests.get('https://api.u2s.uz/physics-ai', params={'savol': user_message}, timeout=10)
        response.raise_for_status()
        ai_response = response.json().get('javob', "Uzr, javobni ololmadim.")
    except Exception as e:
        current_app.logger.error(f"AI API error: {e}")
        ai_response = "Tizimda vaqtincha xatolik yuz berdi. Keyinroq urinib ko'ring."

    # Save to DB
    chat_entry = ChatMessage(
        user_id=current_user.id,
        message=user_message,
        response=ai_response
    )
    db.session.add(chat_entry)
    db.session.commit()

    return jsonify({"javob": ai_response})

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

@main.route("/admin/add_lab", methods=["POST"])
@login_required
def add_lab_v2():
    if current_user.username != "admin":
        abort(403)

    title = request.form.get("title")
    about = request.form.get("about")
    link = request.form.get("link")
    pic = request.files.get("pic")
    zip_file = request.files.get("zip")

    if not pic or pic.filename == '':
        return "No picture provided", 400

    pic_filename = secure_filename(f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{pic.filename}")
    pic_save_dir = os.path.join(current_app.root_path, 'static', 'pics')
    os.makedirs(pic_save_dir, exist_ok=True)
    pic_save_path = os.path.join(pic_save_dir, pic_filename)
    pic.save(pic_save_path)

    final_link = link
    if zip_file and zip_file.filename.endswith('.zip'):
        slug = secure_filename(title).lower()
        if not slug:
            slug = f"lab_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        lab_dir = os.path.join(current_app.root_path, 'static', 'labs', slug)
        os.makedirs(lab_dir, exist_ok=True)
        
        zip_path = os.path.join(lab_dir, secure_filename(zip_file.filename))
        zip_file.save(zip_path)
        
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(lab_dir)
            os.remove(zip_path)
            
            # Check if there's an index.html in the extracted files
            if os.path.exists(os.path.join(lab_dir, 'index.html')):
                final_link = f"/static/labs/{slug}/index.html"
            else:
                # Maybe it extracted into a subfolder
                items = [i for i in os.listdir(lab_dir) if not i.startswith('.')]
                if len(items) == 1 and os.path.isdir(os.path.join(lab_dir, items[0])):
                    subfolder = items[0]
                    if os.path.exists(os.path.join(lab_dir, subfolder, 'index.html')):
                        final_link = f"/static/labs/{slug}/{subfolder}/index.html"
        except Exception as e:
            current_app.logger.error(f"ZIP error: {e}")
            # If ZIP fails, we still have the pic and possibly the manual link

    new_lab = Labs(name=title, about=about, pic_path=f"pics/{pic_filename}", link=final_link or "")
    db.session.add(new_lab)
    db.session.commit()
    return "Good"

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

@main.route("/api/delete_labs/<int:item_id>",methods=["DELETE"])
@login_required
def delete_labs(item_id):
    if current_user.username !="admin":
        abort(403)

    item = Labs.query.get_or_404(item_id)
    
    # Try to delete the picture
    if item.pic_path:
        try:
            pic_path = os.path.join(current_app.root_path, 'static', item.pic_path)
            if os.path.exists(pic_path):
                os.remove(pic_path)
        except Exception as e:
            current_app.logger.error(f"Error deleting lab pic: {e}")
            
    # Try to delete the lab folder if it's dynamic
    if item.link and "/static/labs/" in item.link:
        try:
            # item.link is like "/static/labs/slug/index.html"
            parts = item.link.split('/')
            if len(parts) >= 4:
                slug = parts[3]
                lab_dir = os.path.join(current_app.root_path, 'static', 'labs', slug)
                if os.path.exists(lab_dir):
                    shutil.rmtree(lab_dir)
        except Exception as e:
            current_app.logger.error(f"Error deleting lab folder: {e}")

    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Item deleted successfully"}), 200

@main.route("/api/delete_animation/<int:item_id>",methods=["DELETE"])
@login_required
def delete_animation(item_id):
    if current_user.username !="admin":
        abort(403)
    item = Gifs.query.get_or_404(item_id)
    
    # Try to delete the gif/media file
    if item.gif_path:
        try:
            file_path = os.path.join(current_app.root_path, 'static', item.gif_path)
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            current_app.logger.error(f"Error deleting animation file: {e}")

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

@main.route("/api/handbook", methods=["GET"])
def get_handbook():
    items = HandbookItem.query.all()
    return jsonify([{
        "id": i.id,
        "category": i.category,
        "title": i.title,
        "content": i.content,
        "about": i.about
    } for i in items])

@main.route("/admin/add_handbook", methods=["POST"])
@login_required
def add_handbook():
    if current_user.username != "admin":
        abort(403)
    data = request.get_json(force=True)
    new_item = HandbookItem(
        category=data["category"],
        title=data["title"],
        content=data["content"],
        about=data.get("about", "")
    )
    db.session.add(new_item)
    db.session.commit()
    return jsonify({"message": "Handbook item added successfully"}), 201

@main.route("/api/delete_handbook/<int:item_id>", methods=["DELETE"])
@login_required
def delete_handbook(item_id):
    if current_user.username != "admin":
        abort(403)
    item = HandbookItem.query.get_or_404(item_id)
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
@login_required
def show_tests(name):
    tests = Quiz.query.filter_by(theme=name).all()
    user_id = current_user.id
    quiz_status = {test.id: check_history(user_id, test.id, "quiz") for test in tests}
    return render_template("show_tests.html", name=name, tests=tests, quiz_status=quiz_status)


@main.route("/tests/<theme>/<int:quiz_id>", methods=["GET", "POST"])
@login_required
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
@login_required
def show_matter(name):
    page = request.args.get("page", 1, type=int)
    per_page = 10
    matters = Matter.query.filter_by(theme=name).paginate(page=page, per_page=per_page, error_out=False)
    user_id = current_user.id
    for matter in matters.items:
        matter.solved = check_history(user_id, matter.id, "matter")["status"]
    return render_template("show_matter.html", name=name, matters=matters)


@main.route("/matters/<theme>/<int:matter_id>", methods=["GET", "POST"])
@login_required
def calc_matter(theme, matter_id):
    matter = Matter.query.get_or_404(matter_id)
    if request.method == "POST":
        user_answer = request.form["answer"].strip()
        if user_answer == matter.correct:
            save_user_progress(current_user.id, matter.id, matter.ball, "matter")
            flash(f"✅ To‘g‘ri javob! ({user_answer})", "success")
        else:
            flash(f"❌ Noto‘g‘ri javob! ({user_answer})", "error")
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


@main.route('/lab')
def lab_list_view():
    labs = get_lab_list()
    return render_template('lab_list.html', labs=labs)

@main.route('/handbook')
def handbook_view():
    items = HandbookItem.query.all()
    categories = db.session.query(HandbookItem.category).distinct().all()
    categories = [c[0] for c in categories]
    return render_template('handbook.html', items=items, categories=categories)

@main.route("/labaratory/<id>")
def lab_page(id):
    return render_template(f"lab/{id}/index.html")

@main.route("/lab/workspace")
def lab_workspace():
    src = request.args.get('src')
    title = request.args.get('title', 'Laboratoriya')
    if not src:
        flash("Laboratoriya yo'li topilmadi.", "error")
        return redirect(url_for('main.lab_list_view'))
    return render_template("lab_workspace.html", src=src, title=title)


@main.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))
        
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
                flash("Bu taxallus allaqachon band qilingan.", "error")
                return render_template("signup.html", form=form)

            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            new_user = User(
                name=name,
                surname=surname,
                username=username,
                university=university,
                password=hashed_password,
            )
            db.session.add(new_user)
            db.session.commit()

            # Auto-login after signup
            login_user(new_user)
            flash("Ro'yxatdan o'tish muvaffaqiyatli yakunlandi!", "success")
            return redirect(url_for("main.profile"))

        except Exception as e:
            current_app.logger.error(f"Signup error: {e}")
            db.session.rollback()
            flash("Tizimda xatolik yuz berdi. Iltimos, qayta urinib ko'ring.", "error")
            return render_template("signup.html", form=form)
    
    # Show strict validation errors
    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{getattr(form, field).label.text}: {error}", "error")

    return render_template("signup.html", form=form)


@main.route("/signin", methods=["GET", "POST"])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))

    form = SignInForm()
    if form.validate_on_submit():
        username = form.username.data.replace(" ", "")
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if user and user.password and check_password_hash(user.password, password):
            login_user(user)
            flash("Xush kelibsiz!", "success")
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("main.profile"))
        
        flash("Taxallus yoki parol noto'g'ri.", "error")
    
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