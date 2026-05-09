from flask import (
    render_template, redirect, url_for, request, flash, current_app,
    jsonify, abort
)
from .. import db
from . import main
from .forms import SignInForm, SignUpForm, UpdateData
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, logout_user, login_user, current_user
import json
import re
from werkzeug.utils import secure_filename
from datetime import datetime
from urllib.parse import urlparse, urljoin
import os
import zipfile
import shutil
import requests
from functools import wraps
from ..models import (
    get_leaderboard, get_matter, get_quiz, Gifs, get_animation_func, Labs, get_labs,
    get_lab_list, HandbookItem, ChatMessage, User, Matter, Quiz, Theme, MatterPoints, QuizPoints,
    SolvedProblems, TestResults, check_history, save_user_progress, get_all_themes,
    Lesson, get_all_lessons, get_lessons_by_prefix,
)

ALLOWED_GIF_EXTENSIONS = {'gif', 'mp4'}
ALLOWED_IMG_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}
ALLOWED_LESSON_EXTENSIONS = {'pdf', 'docx'}
MAX_CHAT_MESSAGE_LEN = 2000
SAFE_THEME_RE = re.compile(r"^[a-z0-9_\-]{1,80}$")
SAFE_LAB_ID_RE = re.compile(r"^[A-Za-z0-9_\-]{1,80}$")
RESERVED_USERNAMES = {"admin", "administrator", "root", "system", "superuser"}


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(401)
        if current_user.username != "admin":
            abort(403)
        return f(*args, **kwargs)
    return wrapper


def allowed_extension(filename, allowed):
    return (
        isinstance(filename, str)
        and '.' in filename
        and filename.rsplit('.', 1)[1].lower() in allowed
    )


def is_safe_internal_url(target):
    if not target:
        return False
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc


def normalize_theme(name):
    return (name or "").strip().lower()


@main.route("/", methods=["GET"])
def home_page():
    return render_template("index.html")


@main.route("/gifs")
def show_gifs():
    gifs = Gifs.query.all()
    return render_template("gifs.html", gifs=gifs)


@main.route("/chat")
@login_required
def chat():
    history = ChatMessage.query.filter_by(user_id=current_user.id).order_by(ChatMessage.timestamp).all()
    return render_template("chat-ai.html", history=history)


@main.route("/api/chat", methods=["POST"])
@login_required
def chat_api():
    data = request.get_json(silent=True) or {}
    user_message = (data.get("message") or "").strip()

    if not user_message:
        return jsonify({"error": "Empty message"}), 400
    if len(user_message) > MAX_CHAT_MESSAGE_LEN:
        return jsonify({"error": "Message too long"}), 413

    try:
        response = requests.get(
            'https://api.u2s.uz/physics-ai',
            params={'savol': user_message},
            timeout=10,
        )
        response.raise_for_status()
        ai_response = response.json().get('javob', "Uzr, javobni ololmadim.")
    except Exception as e:
        current_app.logger.error("AI API error: %s", e)
        ai_response = "Tizimda vaqtincha xatolik yuz berdi. Keyinroq urinib ko'ring."

    chat_entry = ChatMessage(
        user_id=current_user.id,
        message=user_message,
        response=ai_response,
    )
    db.session.add(chat_entry)
    db.session.commit()

    return jsonify({"javob": ai_response})


@main.route("/admin")
@admin_required
def admin():
    return render_template("admin/index.html")


@main.route("/admin/add_animation", methods=["POST"])
@admin_required
def add_get():
    title = (request.form.get("title") or "").strip()
    about = (request.form.get("about") or "").strip()
    theme = normalize_theme(request.form.get("theme"))
    media = request.files.get("gif")

    if not title or not about or not theme:
        return jsonify({"error": "Majburiy maydonlar to'ldirilmagan"}), 400
    if not media or media.filename == '':
        return jsonify({"error": "Fayl yuborilmagan"}), 400
    if not allowed_extension(media.filename, ALLOWED_GIF_EXTENSIONS):
        return jsonify({"error": "Faqat .gif yoki .mp4 fayllar ruxsat etilgan"}), 400

    filename = secure_filename(f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{media.filename}")
    save_dir = os.path.join(current_app.root_path, 'static', 'gifs')
    os.makedirs(save_dir, exist_ok=True)
    media.save(os.path.join(save_dir, filename))

    new_gif = Gifs(name=title, about=about, gif_path=f"gifs/{filename}", theme=theme)
    db.session.add(new_gif)
    db.session.commit()
    return jsonify({"message": "Animation added"}), 201


def _safe_extract_zip(zip_path, target_dir):
    """Extract a ZIP archive, refusing entries that escape target_dir (zip slip)."""
    target_dir = os.path.realpath(target_dir)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for member in zip_ref.namelist():
            member_path = os.path.realpath(os.path.join(target_dir, member))
            if not member_path.startswith(target_dir + os.sep) and member_path != target_dir:
                raise ValueError(f"Unsafe ZIP entry: {member}")
        zip_ref.extractall(target_dir)


@main.route("/admin/add_lab", methods=["POST"])
@admin_required
def add_lab_v2():
    title = (request.form.get("title") or "").strip()
    about = (request.form.get("about") or "").strip()
    link = (request.form.get("link") or "").strip()
    pic = request.files.get("pic")
    zip_file = request.files.get("zip")

    if not title or not about:
        return jsonify({"error": "Majburiy maydonlar to'ldirilmagan"}), 400
    if not pic or pic.filename == '':
        return jsonify({"error": "Rasm yuborilmagan"}), 400
    if not allowed_extension(pic.filename, ALLOWED_IMG_EXTENSIONS):
        return jsonify({"error": "Rasm formati noto'g'ri"}), 400

    pic_filename = secure_filename(f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{pic.filename}")
    pic_save_dir = os.path.join(current_app.root_path, 'static', 'pics')
    os.makedirs(pic_save_dir, exist_ok=True)
    pic.save(os.path.join(pic_save_dir, pic_filename))

    final_link = link if link.startswith('/') or link.startswith('http') else ""

    if zip_file and zip_file.filename and zip_file.filename.endswith('.zip'):
        slug = secure_filename(title).lower() or f"lab_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        lab_dir = os.path.join(current_app.root_path, 'static', 'labs', slug)
        os.makedirs(lab_dir, exist_ok=True)

        zip_path = os.path.join(lab_dir, secure_filename(zip_file.filename))
        zip_file.save(zip_path)

        try:
            _safe_extract_zip(zip_path, lab_dir)
            os.remove(zip_path)

            if os.path.exists(os.path.join(lab_dir, 'index.html')):
                final_link = f"/static/labs/{slug}/index.html"
            else:
                items = [i for i in os.listdir(lab_dir) if not i.startswith('.')]
                if len(items) == 1 and os.path.isdir(os.path.join(lab_dir, items[0])):
                    subfolder = items[0]
                    if os.path.exists(os.path.join(lab_dir, subfolder, 'index.html')):
                        final_link = f"/static/labs/{slug}/{subfolder}/index.html"
        except Exception as e:
            current_app.logger.error("ZIP error: %s", e)
            shutil.rmtree(lab_dir, ignore_errors=True)
            return jsonify({"error": "ZIP faylni ochishda xatolik"}), 400

    new_lab = Labs(name=title, about=about, pic_path=f"pics/{pic_filename}", link=final_link or "")
    db.session.add(new_lab)
    db.session.commit()
    return jsonify({"message": "Lab added"}), 201


def _validate_matter_payload(data):
    required = ("title", "main", "helper", "correct", "theme", "ball")
    missing = [k for k in required if data.get(k) in (None, "")]
    if missing:
        return f"Maydon(lar) yetishmaydi: {', '.join(missing)}"
    try:
        int(data["ball"])
    except (TypeError, ValueError):
        return "Ball son bo'lishi kerak"
    return None


@main.route("/admin/add_matter", methods=["POST"])
@admin_required
def add_matter():
    data = request.get_json(silent=True) or {}
    err = _validate_matter_payload(data)
    if err:
        return jsonify({"error": err}), 400

    new_matter = Matter(
        title=data["title"].strip(),
        main=data["main"].strip(),
        helper=data["helper"].strip(),
        theme=normalize_theme(data["theme"]),
        correct=data["correct"].strip(),
        status=True,
        ball=int(data["ball"]),
    )
    db.session.add(new_matter)
    db.session.commit()
    return jsonify({"message": "Matter added successfully"}), 201


@main.route("/admin/add_quiz", methods=["POST"])
@admin_required
def add_quiz():
    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()
    theme = normalize_theme(data.get("theme"))
    quiz_data = data.get("data", [])
    if not title or not theme:
        return jsonify({"error": "Title va Theme kerak"}), 400
    if not isinstance(quiz_data, list):
        return jsonify({"error": "Data ro'yxat (list) bo'lishi kerak"}), 400

    new_quiz = Quiz(
        title=title,
        theme=theme,
        status=True,
        data=json.dumps(quiz_data),
    )
    db.session.add(new_quiz)
    db.session.commit()
    return jsonify({"message": "Quiz added successfully"}), 201


@main.route("/admin/add_theme", methods=["POST"])
@admin_required
def add_theme():
    data = request.get_json(silent=True) or {}
    name = normalize_theme(data.get("name"))
    about = (data.get("about") or "").strip()
    if not name or not about:
        return jsonify({"error": "Nom va izoh majburiy"}), 400
    if Theme.query.filter_by(name=name).first():
        return jsonify({"error": "Bunday bo'lim allaqachon mavjud"}), 409

    new_theme = Theme(name=name, about=about)
    db.session.add(new_theme)
    db.session.commit()
    return jsonify({"message": "Theme added successfully"}), 201


@main.route("/api/themes", methods=["GET"])
def get_themes():
    return jsonify(get_all_themes())


@main.route("/api/edit_theme", methods=["PUT"])
@admin_required
def edit_theme():
    data = request.get_json(silent=True) or {}
    theme = Theme.query.get_or_404(data.get("id"))
    new_name = normalize_theme(data.get("name") or theme.name)
    new_about = (data.get("about") or theme.about).strip()

    if not new_name or not new_about:
        return jsonify({"error": "Nom va izoh majburiy"}), 400

    if new_name != theme.name:
        clash = Theme.query.filter(Theme.name == new_name, Theme.id != theme.id).first()
        if clash:
            return jsonify({"error": "Bunday nomli bo'lim allaqachon mavjud"}), 409
        # Cascade rename foreign references (theme is stored as a string label, not an FK)
        old_name = theme.name
        Matter.query.filter_by(theme=old_name).update({"theme": new_name})
        Quiz.query.filter_by(theme=old_name).update({"theme": new_name})
        Gifs.query.filter_by(theme=old_name).update({"theme": new_name})
        theme.name = new_name

    theme.about = new_about
    db.session.commit()
    return jsonify({"status": "done"}), 200


@main.route("/api/get_animation", methods=["GET"])
def get_animation_list():
    prefix = (request.args.get("prefix") or "").lower()
    return jsonify(get_animation_func(prefix))


@main.route("/api/get_labs", methods=["GET"])
def get_labs_list():
    prefix = (request.args.get("prefix") or "").lower()
    return jsonify(get_labs(prefix))


@main.route("/api/get_quiz", methods=["GET"])
def get_quiz_list():
    prefix = (request.args.get("prefix") or "").lower()
    return jsonify(get_quiz(prefix))


@main.route("/api/get_matter", methods=["GET"])
def get_matter_list():
    prefix = (request.args.get("prefix") or "").lower()
    return jsonify(get_matter(prefix))


def _remove_lab_folder(link):
    """Given a lab link like /static/labs/<slug>/index.html, rmtree the slug folder safely."""
    if not link or "/static/labs/" not in link:
        return
    parts = link.split('/')
    if len(parts) < 4:
        return
    slug = secure_filename(parts[3])
    if not slug:
        return
    static_root = os.path.realpath(os.path.join(current_app.root_path, 'static'))
    lab_dir = os.path.realpath(os.path.join(current_app.root_path, 'static', 'labs', slug))
    if lab_dir.startswith(static_root + os.sep) and os.path.exists(lab_dir):
        try:
            shutil.rmtree(lab_dir)
        except OSError as e:
            current_app.logger.error("Error removing lab folder %s: %s", lab_dir, e)


@main.route("/admin/edit_lab", methods=["POST"])
@admin_required
def edit_lab():
    item_id = request.form.get("id")
    if not item_id:
        return jsonify({"error": "id majburiy"}), 400
    item = Labs.query.get_or_404(int(item_id))

    title = (request.form.get("title") or "").strip()
    about = (request.form.get("about") or "").strip()
    link = (request.form.get("link") or "").strip()
    pic = request.files.get("pic")
    zip_file = request.files.get("zip")

    if title:
        item.name = title
    if about:
        item.about = about

    if pic and pic.filename:
        if not allowed_extension(pic.filename, ALLOWED_IMG_EXTENSIONS):
            return jsonify({"error": "Rasm formati noto'g'ri"}), 400
        pic_filename = secure_filename(f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{pic.filename}")
        pic_save_dir = os.path.join(current_app.root_path, 'static', 'pics')
        os.makedirs(pic_save_dir, exist_ok=True)
        pic.save(os.path.join(pic_save_dir, pic_filename))
        old_pic = item.pic_path
        item.pic_path = f"pics/{pic_filename}"
        _safe_remove_static_file(old_pic)

    if zip_file and zip_file.filename and zip_file.filename.endswith('.zip'):
        # Replace the lab folder
        slug = secure_filename(item.name).lower() or f"lab_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        new_lab_dir = os.path.join(current_app.root_path, 'static', 'labs', slug)
        # Remove old folder if any
        _remove_lab_folder(item.link)
        os.makedirs(new_lab_dir, exist_ok=True)
        zip_path = os.path.join(new_lab_dir, secure_filename(zip_file.filename))
        zip_file.save(zip_path)
        try:
            _safe_extract_zip(zip_path, new_lab_dir)
            os.remove(zip_path)
            if os.path.exists(os.path.join(new_lab_dir, 'index.html')):
                item.link = f"/static/labs/{slug}/index.html"
            else:
                items = [i for i in os.listdir(new_lab_dir) if not i.startswith('.')]
                if len(items) == 1 and os.path.isdir(os.path.join(new_lab_dir, items[0])):
                    sub = items[0]
                    if os.path.exists(os.path.join(new_lab_dir, sub, 'index.html')):
                        item.link = f"/static/labs/{slug}/{sub}/index.html"
        except Exception as e:
            current_app.logger.error("ZIP error on edit_lab: %s", e)
            shutil.rmtree(new_lab_dir, ignore_errors=True)
            return jsonify({"error": "ZIP faylni ochishda xatolik"}), 400
    elif link and link != item.link:
        # External link override (only allow / or http(s))
        if link.startswith('/') or link.startswith('http'):
            # If the previous link was a managed lab folder, remove it
            if item.link and "/static/labs/" in item.link and "/static/labs/" not in link:
                _remove_lab_folder(item.link)
            item.link = link

    db.session.commit()
    return jsonify({"status": "done"}), 200


@main.route("/api/delete_labs/<int:item_id>", methods=["DELETE"])
@admin_required
def delete_labs(item_id):
    item = Labs.query.get_or_404(item_id)
    _safe_remove_static_file(item.pic_path)
    _remove_lab_folder(item.link)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Item deleted successfully"}), 200


def _safe_remove_static_file(rel_path):
    """Delete a file under static/ if it really is under static/."""
    if not rel_path:
        return
    static_root = os.path.realpath(os.path.join(current_app.root_path, 'static'))
    full = os.path.realpath(os.path.join(current_app.root_path, 'static', rel_path))
    if full.startswith(static_root + os.sep) and os.path.exists(full) and os.path.isfile(full):
        try:
            os.remove(full)
        except OSError as e:
            current_app.logger.error("Error removing %s: %s", full, e)


@main.route("/admin/edit_animation", methods=["POST"])
@admin_required
def edit_animation():
    item_id = request.form.get("id")
    if not item_id:
        return jsonify({"error": "id majburiy"}), 400
    item = Gifs.query.get_or_404(int(item_id))

    title = (request.form.get("title") or "").strip()
    about = (request.form.get("about") or "").strip()
    theme = normalize_theme(request.form.get("theme"))
    media = request.files.get("gif")

    if title:
        item.name = title
    if about:
        item.about = about
    if theme:
        item.theme = theme

    if media and media.filename:
        if not allowed_extension(media.filename, ALLOWED_GIF_EXTENSIONS):
            return jsonify({"error": "Faqat .gif yoki .mp4 fayllar ruxsat etilgan"}), 400
        filename = secure_filename(f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{media.filename}")
        save_dir = os.path.join(current_app.root_path, 'static', 'gifs')
        os.makedirs(save_dir, exist_ok=True)
        media.save(os.path.join(save_dir, filename))
        old_path = item.gif_path
        item.gif_path = f"gifs/{filename}"
        _safe_remove_static_file(old_path)

    db.session.commit()
    return jsonify({"status": "done"}), 200


@main.route("/api/delete_animation/<int:item_id>", methods=["DELETE"])
@admin_required
def delete_animation(item_id):
    item = Gifs.query.get_or_404(item_id)
    _safe_remove_static_file(item.gif_path)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Item deleted successfully"}), 200


@main.route("/api/delete_theme/<int:item_id>", methods=["DELETE"])
@admin_required
def delete_theme(item_id):
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
        "about": i.about,
    } for i in items])


@main.route("/admin/add_handbook", methods=["POST"])
@admin_required
def add_handbook():
    data = request.get_json(silent=True) or {}
    category = (data.get("category") or "").strip()
    title = (data.get("title") or "").strip()
    content = (data.get("content") or "").strip()
    if not (category and title and content):
        return jsonify({"error": "Kategoriya, nom va mazmun majburiy"}), 400

    new_item = HandbookItem(
        category=category,
        title=title,
        content=content,
        about=(data.get("about") or "").strip(),
    )
    db.session.add(new_item)
    db.session.commit()
    return jsonify({"message": "Handbook item added successfully"}), 201


@main.route("/api/delete_handbook/<int:item_id>", methods=["DELETE"])
@admin_required
def delete_handbook(item_id):
    item = HandbookItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Item deleted successfully"}), 200


@main.route("/api/edit_handbook", methods=["PUT"])
@admin_required
def edit_handbook():
    data = request.get_json(silent=True) or {}
    item = HandbookItem.query.get_or_404(data.get("id"))
    category = (data.get("category") or "").strip()
    title = (data.get("title") or "").strip()
    content = (data.get("content") or "").strip()
    if not (category and title and content):
        return jsonify({"error": "Kategoriya, nom va mazmun majburiy"}), 400
    item.category = category
    item.title = title
    item.content = content
    item.about = (data.get("about") or "").strip()
    db.session.commit()
    return jsonify({"status": "done"}), 200


# ----- User management -----

@main.route("/api/users", methods=["GET"])
@admin_required
def list_users():
    prefix = (request.args.get("prefix") or "").strip().lower()
    q = User.query
    if prefix:
        q = q.filter(User.username.ilike(f"{prefix}%"))
    users = q.order_by(User.id.asc()).limit(200).all()
    return jsonify([
        {
            "id": u.id,
            "username": u.username,
            "name": u.name,
            "surname": u.surname,
            "university": u.university,
            "points": u.points,
            "problems_solved": u.problems_solved,
            "tests_passed": u.tests_passed,
            "is_admin": u.username == "admin",
        }
        for u in users
    ])


@main.route("/api/edit_user", methods=["PUT"])
@admin_required
def edit_user():
    data = request.get_json(silent=True) or {}
    user = User.query.get_or_404(data.get("id"))
    name = (data.get("name") or "").strip()
    surname = (data.get("surname") or "").strip()
    university = (data.get("university") or "").strip()
    if not (name and surname and university):
        return jsonify({"error": "Ism, familiya va o'qish joyi majburiy"}), 400
    user.name = name
    user.surname = surname
    user.university = university
    db.session.commit()
    return jsonify({"status": "done"}), 200


# ----- Lessons (Mavzular) — PDF/DOCX theoretical materials -----

def _get_file_ext(filename):
    if not filename or '.' not in filename:
        return ''
    return filename.rsplit('.', 1)[1].lower()


def _convert_docx_to_html(docx_full_path, html_full_path):
    """Convert .docx → sanitized HTML alongside the original file."""
    try:
        import mammoth
        import bleach
    except ImportError as e:
        current_app.logger.error("mammoth/bleach not installed: %s", e)
        return False
    try:
        with open(docx_full_path, 'rb') as f:
            result = mammoth.convert_to_html(f)
        raw_html = result.value or ""
        allowed_tags = list(bleach.sanitizer.ALLOWED_TAGS) + [
            'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'br', 'hr',
            'table', 'thead', 'tbody', 'tr', 'th', 'td',
            'img', 'figure', 'figcaption', 'sub', 'sup', 'span', 'div',
        ]
        allowed_attrs = {
            **bleach.sanitizer.ALLOWED_ATTRIBUTES,
            'img': ['src', 'alt', 'width', 'height', 'style'],
            'span': ['style'],
            'div': ['style'],
            'p': ['style'],
            'td': ['colspan', 'rowspan', 'style'],
            'th': ['colspan', 'rowspan', 'style'],
        }
        clean = bleach.clean(raw_html, tags=allowed_tags, attributes=allowed_attrs, strip=True)
        with open(html_full_path, 'w', encoding='utf-8') as f:
            f.write(clean)
        return True
    except Exception as e:
        current_app.logger.error("DOCX→HTML conversion failed: %s", e)
        return False


def _save_lesson_file(uploaded):
    """Save uploaded PDF/DOCX under static/lessons/ and produce companion HTML for docx.
    Returns (rel_file_path, ext, rel_html_path_or_None) or raises ValueError."""
    ext = _get_file_ext(uploaded.filename)
    if ext not in ALLOWED_LESSON_EXTENSIONS:
        raise ValueError("Faqat .pdf yoki .docx fayllar ruxsat etilgan")

    base = secure_filename(uploaded.filename) or f"lesson.{ext}"
    fname = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{base}"
    save_dir = os.path.join(current_app.root_path, 'static', 'lessons')
    os.makedirs(save_dir, exist_ok=True)
    full_path = os.path.join(save_dir, fname)
    uploaded.save(full_path)

    rel_path = f"lessons/{fname}"
    rel_html = None
    if ext == 'docx':
        html_full = full_path + ".html"
        if _convert_docx_to_html(full_path, html_full):
            rel_html = rel_path + ".html"
    return rel_path, ext, rel_html


@main.route("/admin/add_lesson", methods=["POST"])
@admin_required
def add_lesson():
    title = (request.form.get("title") or "").strip()
    about = (request.form.get("about") or "").strip()
    uploaded = request.files.get("file")
    if not title:
        return jsonify({"error": "Sarlavha majburiy"}), 400
    if not uploaded or not uploaded.filename:
        return jsonify({"error": "Fayl yuborilmagan"}), 400
    try:
        rel_path, ext, rel_html = _save_lesson_file(uploaded)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    lesson = Lesson(
        title=title,
        about=about,
        file_path=rel_path,
        file_type=ext,
        html_path=rel_html,
    )
    db.session.add(lesson)
    db.session.commit()
    return jsonify({"message": "Lesson added", "id": lesson.id}), 201


@main.route("/admin/edit_lesson", methods=["POST"])
@admin_required
def edit_lesson():
    item_id = request.form.get("id")
    if not item_id:
        return jsonify({"error": "id majburiy"}), 400
    lesson = Lesson.query.get_or_404(int(item_id))

    title = (request.form.get("title") or "").strip()
    about = (request.form.get("about") or "").strip()
    uploaded = request.files.get("file")

    if title:
        lesson.title = title
    # about can be cleared explicitly
    if "about" in request.form:
        lesson.about = about

    if uploaded and uploaded.filename:
        try:
            rel_path, ext, rel_html = _save_lesson_file(uploaded)
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        # Cleanup old files
        old_file = lesson.file_path
        old_html = lesson.html_path
        lesson.file_path = rel_path
        lesson.file_type = ext
        lesson.html_path = rel_html
        _safe_remove_static_file(old_file)
        if old_html:
            _safe_remove_static_file(old_html)

    db.session.commit()
    return jsonify({"status": "done"}), 200


@main.route("/api/get_lessons", methods=["GET"])
def api_get_lessons():
    prefix = (request.args.get("prefix") or "").lower()
    return jsonify(get_lessons_by_prefix(prefix))


@main.route("/api/delete_lesson/<int:item_id>", methods=["DELETE"])
@admin_required
def delete_lesson(item_id):
    lesson = Lesson.query.get_or_404(item_id)
    _safe_remove_static_file(lesson.file_path)
    if lesson.html_path:
        _safe_remove_static_file(lesson.html_path)
    db.session.delete(lesson)
    db.session.commit()
    return jsonify({"message": "Lesson deleted"}), 200


# ----- User-facing lesson views -----

@main.route("/lessons")
def lessons_list():
    page = request.args.get("page", 1, type=int)
    per_page = 12
    pagination = Lesson.query.order_by(Lesson.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    return render_template("lessons.html", lessons=pagination)


@main.route("/lessons/<int:lesson_id>")
def lesson_view(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    html_content = None
    if lesson.file_type == 'docx' and lesson.html_path:
        html_full = os.path.join(current_app.root_path, 'static', lesson.html_path)
        if os.path.exists(html_full):
            try:
                with open(html_full, 'r', encoding='utf-8') as f:
                    html_content = f.read()
            except OSError as e:
                current_app.logger.error("Failed to read lesson HTML: %s", e)
    return render_template("lesson_view.html", lesson=lesson, html_content=html_content)


@main.route("/api/delete_user/<int:user_id>", methods=["DELETE"])
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.username == "admin":
        return jsonify({"error": "Admin foydalanuvchisini o'chirib bo'lmaydi"}), 400
    if current_user.id == user.id:
        return jsonify({"error": "O'zingizni o'chirib bo'lmaydi"}), 400

    # Cascade remove related rows (no FK cascade declared in models)
    MatterPoints.query.filter_by(user_id=user.id).delete(synchronize_session=False)
    QuizPoints.query.filter_by(user_id=user.id).delete(synchronize_session=False)
    SolvedProblems.query.filter_by(user_id=user.id).delete(synchronize_session=False)
    TestResults.query.filter_by(user_id=user.id).delete(synchronize_session=False)
    ChatMessage.query.filter_by(user_id=user.id).delete(synchronize_session=False)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"}), 200


@main.route("/api/delete_quiz/<int:item_id>", methods=["DELETE"])
@admin_required
def delete_quiz(item_id):
    item = Quiz.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Item deleted successfully"}), 200


@main.route("/api/delete_matter/<int:item_id>", methods=["DELETE"])
@admin_required
def delete_matter(item_id):
    item = Matter.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Item deleted successfully"}), 200


@main.route("/api/edit_quiz", methods=["PUT"])
@admin_required
def edit_quiz():
    data = request.get_json(silent=True) or {}
    quiz = Quiz.query.get_or_404(data.get("id"))
    if "title" in data and data["title"]:
        quiz.title = data["title"].strip()
    if "theme" in data and data["theme"]:
        quiz.theme = normalize_theme(data["theme"])
    if "data" in data:
        if not isinstance(data["data"], list):
            return jsonify({"error": "Data ro'yxat bo'lishi kerak"}), 400
        quiz.data = json.dumps(data["data"])
    if "status" in data:
        quiz.status = bool(data["status"])
    db.session.commit()
    return jsonify({"status": "done"}), 200


@main.route("/api/toggle_quiz_status", methods=["PUT"])
@admin_required
def toggle_quiz_status():
    data = request.get_json(silent=True) or {}
    quiz = Quiz.query.get_or_404(data.get("id"))
    quiz.status = not quiz.status
    db.session.commit()
    return jsonify({"status": "done", "new_status": quiz.status}), 200


@main.route("/api/edit_matter", methods=["PUT"])
@admin_required
def edit_matter():
    data = request.get_json(silent=True) or {}
    matter = Matter.query.get_or_404(data.get("id"))
    matter.title = (data.get("title") or matter.title).strip()
    matter.main = (data.get("main") or matter.main).strip()
    matter.helper = (data.get("helper") or matter.helper).strip()
    matter.theme = normalize_theme(data.get("theme") or matter.theme)
    matter.correct = (data.get("correct") or matter.correct).strip()
    try:
        matter.ball = int(data.get("ball", matter.ball))
    except (TypeError, ValueError):
        return jsonify({"error": "Ball son bo'lishi kerak"}), 400
    matter.status = bool(data.get("status", matter.status))
    db.session.commit()
    return jsonify({"status": "done"}), 200


@main.route("/api/toggle_matter_status", methods=["PUT"])
@admin_required
def toggle_matter_status():
    data = request.get_json(silent=True) or {}
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
    name = normalize_theme(name)
    tests = Quiz.query.filter_by(theme=name, status=True).all()
    user_id = current_user.id
    quiz_status = {test.id: check_history(user_id, test.id, "quiz") for test in tests}
    return render_template("show_tests.html", name=name, tests=tests, quiz_status=quiz_status)


@main.route("/tests/<theme>/<int:quiz_id>", methods=["GET", "POST"])
@login_required
def calc_test(theme, quiz_id):
    quiz = Quiz.query.get_or_404(int(quiz_id))
    questions = json.loads(quiz.data)
    if request.method == "POST":
        users_ball = sum(
            int(q.get("ball", 0))
            for q in questions
            if request.form.get(f'question-{q["id"]}') == q["answer"]
        )
        score = sum(
            1 for q in questions
            if request.form.get(f'question-{q["id"]}') == q["answer"]
        )
        save_user_progress(current_user.id, quiz.id, users_ball, "quiz")
        return render_template("result_test.html", ball=users_ball, score=score, total=len(questions))
    return render_template("calc_test.html", questions=questions, theme=theme)


@main.route("/matters/<name>")
@login_required
def show_matter(name):
    name = normalize_theme(name)
    page = request.args.get("page", 1, type=int)
    per_page = 10
    matters = Matter.query.filter_by(theme=name, status=True).paginate(
        page=page, per_page=per_page, error_out=False
    )
    user_id = current_user.id

    if matters.items:
        ids = [m.id for m in matters.items]
        solved_ids = {
            row.matter_id for row in
            SolvedProblems.query.with_entities(SolvedProblems.matter_id)
            .filter(SolvedProblems.user_id == user_id, SolvedProblems.matter_id.in_(ids))
            .all()
        }
        for matter in matters.items:
            matter.solved = matter.id in solved_ids

    return render_template("show_matter.html", name=name, matters=matters)


@main.route("/matters/<theme>/<int:matter_id>", methods=["GET", "POST"])
@login_required
def calc_matter(theme, matter_id):
    matter = Matter.query.get_or_404(matter_id)
    if request.method == "POST":
        user_answer = (request.form.get("answer") or "").strip()
        if not user_answer:
            flash("Iltimos, javobingizni kiriting.", "error")
        elif user_answer == matter.correct:
            save_user_progress(current_user.id, matter.id, matter.ball, "matter")
            flash(f"To'g'ri javob! ({user_answer})", "success")
        else:
            flash(f"Noto'g'ri javob! ({user_answer})", "error")
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
    return render_template("leaderboard.html", ranked_users=ranked_users)


@main.route('/lab')
def lab_list_view():
    labs = get_lab_list()
    return render_template('lab_list.html', labs=labs)


@main.route('/handbook')
def handbook_view():
    items = HandbookItem.query.all()
    categories = [c[0] for c in db.session.query(HandbookItem.category).distinct().all()]
    return render_template('handbook.html', items=items, categories=categories)


@main.route("/labaratory/<lab_id>")
def lab_page(lab_id):
    if not SAFE_LAB_ID_RE.match(lab_id):
        abort(404)
    template_path = f"lab/{lab_id}/index.html"
    template_full = os.path.realpath(
        os.path.join(current_app.root_path, "templates", template_path)
    )
    templates_root = os.path.realpath(
        os.path.join(current_app.root_path, "templates", "lab")
    )
    if not template_full.startswith(templates_root + os.sep):
        abort(404)
    if not os.path.exists(template_full):
        abort(404)
    return render_template(template_path)


@main.route("/lab/workspace")
def lab_workspace():
    src = request.args.get('src', '').strip()
    title = (request.args.get('title') or 'Laboratoriya').strip()[:120]
    if not src:
        flash("Laboratoriya yo'li topilmadi.", "error")
        return redirect(url_for('main.lab_list_view'))
    if not (src.startswith('/static/labs/') or src.startswith('/labaratory/')):
        flash("Ruxsat etilmagan laboratoriya yo'li.", "error")
        return redirect(url_for('main.lab_list_view'))
    return render_template("lab_workspace.html", src=src, title=title)


@main.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))

    form = SignUpForm()
    if form.validate_on_submit():
        try:
            name = form.name.data.strip()
            surname = form.surname.data.strip()
            username = form.username.data.replace(" ", "").lower()
            university = form.university.data.strip()
            password = form.password.data

            if len(username) < 3 or len(username) > 80:
                flash("Taxallus 3 dan 80 belgigacha bo'lishi kerak.", "error")
                return render_template("signup.html", form=form)
            if not re.match(r'^[a-z0-9_]+$', username):
                flash("Taxallusda faqat lotin harflari, raqam va '_' ishlatilishi mumkin.", "error")
                return render_template("signup.html", form=form)
            if username in RESERVED_USERNAMES:
                flash("Bu taxallus zahiralangan.", "error")
                return render_template("signup.html", form=form)
            if len(password) < 8:
                flash("Parol kamida 8 belgidan iborat bo'lishi kerak.", "error")
                return render_template("signup.html", form=form)

            if User.query.filter_by(username=username).first():
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

            login_user(new_user)
            flash("Ro'yxatdan o'tish muvaffaqiyatli yakunlandi!", "success")
            return redirect(url_for("main.profile"))

        except Exception as e:
            current_app.logger.error("Signup error: %s", e)
            db.session.rollback()
            flash("Tizimda xatolik yuz berdi. Iltimos, qayta urinib ko'ring.", "error")
            return render_template("signup.html", form=form)

    if request.method == "POST" and form.errors:
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
        username = form.username.data.replace(" ", "").lower()
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if user and user.password and check_password_hash(user.password, password):
            login_user(user)
            flash("Xush kelibsiz!", "success")
            next_page = request.args.get("next")
            if next_page and is_safe_internal_url(next_page):
                return redirect(next_page)
            return redirect(url_for("main.profile"))

        flash("Taxallus yoki parol noto'g'ri.", "error")

    return render_template("login.html", form=form)


@main.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = UpdateData()
    user = current_user
    ball = user.points
    if form.validate_on_submit():
        user.name = form.name.data.strip()
        user.surname = form.surname.data.strip()
        user.university = form.university.data.strip()
        password = form.password.data
        if password:
            if len(password) < 8:
                flash("Yangi parol kamida 8 belgidan iborat bo'lishi kerak.", "error")
                return redirect(url_for("main.profile"))
            user.password = generate_password_hash(password, method='pbkdf2:sha256')

        try:
            db.session.commit()
            flash("Ma'lumotlar yangilandi!", "success")
        except Exception as e:
            db.session.rollback()
            current_app.logger.error("Profile update error: %s", e)
            flash("Profilni yangilashda xatolik yuz berdi.", "error")

        return redirect(url_for("main.profile"))

    return render_template("profile.html", ball=ball, user=current_user, form=form)


@main.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Siz muvaffaqiyatli chiqdingiz.", "success")
    return redirect(url_for("main.login_page"))
