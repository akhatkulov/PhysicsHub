from flask import render_template, session, redirect, url_for, request, flash, current_app,jsonify
from .. import db
from ..models import User,Theme,Matter,Quiz,get_all_themes,save_user_progress,check_history,get_leaderboard,get_matter,get_quiz
from ..email import send_email
from . import main
from .forms import SignInForm, SignUpForm,UpdateData
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, logout_user, login_user,current_user
import json

@main.route('/', methods=['GET', 'POST'])
def home_page():
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
    ball = res_data['ball']
    status = True 
    if current_user.username == 'admin':
        new_matter = Matter(title=title,main=main,helper=helper,theme=theme,correct=correct,status=True,ball=int(ball))
        db.session.add(new_matter)
        db.session.commit()
        return "Yeah!!!"
    else:
        return render_template('404.html')

@main.post("/admin/add_quiz")
@login_required
def add_quiz():
    try:
        res_data = json.loads(request.data)
        print()
        print(res_data)
        title = res_data.get('title', '')
        theme = res_data.get('theme', '').lower()
        status = True
        data = json.dumps(res_data.get('data', {}))
        print(data)
        print()
        if not title or not theme:
            return jsonify({'error': 'Title va Theme kerak'}), 400
        
        if current_user.is_authenticated and current_user.username == 'admin':
            new_quiz = Quiz(title=title, theme=theme, status=status, data=data)
            db.session.add(new_quiz)
            db.session.commit()
            return jsonify({'message': 'Quiz qo\'shildi!'}), 201
        else:
            return render_template('404.html'), 403
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.post("/admin/add_theme")
@login_required
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

        
@main.route('/api/themes', methods=['GET'])
def get_themes():
    themes = get_all_themes()
    return jsonify(themes)

@main.route('/api/get_quiz', methods=['GET'])
def get_quiz_list():
    prefix = request.args.get('prefix', '').lower()
    return jsonify(get_quiz(prefix))


@main.route('/api/get_matter', methods=['GET'])
def get_matter_list():
    prefix = request.args.get('prefix', '').lower()
    return jsonify(get_matter(prefix))



@main.post('/api/edit_quiz')
@login_required
def edit_quiz():
    if current_user == 'admin':

        data = request.get_json()
        title = res_data.get('title')
        theme = res_data.get('theme').lower()
        status = Bool(res_data['status'])
        data = json.dumps(res_data.get('data'))
        quiz = Quiz.query.filter(Quiz.title ==  title).first()
        if quiz:
            quiz.title = title
            quiz.theme = theme 
            quiz.data = data 
            quiz.status = status 
            db.session.commit()
            return json({"status:":"done"}),200
        else:
            return jsonify({"error","mavjud emas"}),404
    else:
        abort(404)


@main.post('/api/edit_matter')
@login_required
def edit_matter():
    if current_user == 'admin':
        data = request.get_json()
        title = res_data['title']
        main = res_data['main']
        helper = res_data['helper']
        theme = res_data['theme']
        correct = res_data['correct']
        ball = int(res_data['ball'])
        status = Bool(res_data['status'])
        
        matter = Matter.query.filter(Quiz.title ==  title).first()
        if matter:
            matter.title = title
            matter.main = main 
            matter.helper = helper
            matter.theme = theme 
            matter.correct = correct
            matter.ball = ball  
            matter.status = status 
            db.session.commit()
            return json({"status:":"done"}),200
        else:
            return jsonify({"error","mavjud emas"}),404
    else:
        abort(404)

@main.route("/api/delete_theme/<int:item_id>", methods=["DELETE"])
@login_required
def delete_theme(item_id):
    if current_user == "admin":
        item = Theme.query.get(item_id)
        if item:
            db.session.delete(item)
            db.session.commit()
            return jsonify({"message": "Item deleted successfully"}), 200
        return jsonify({"error": "Item not found"}), 404
    else:
        return "Doom shot, Mother Fucker)"

@main.route('/api/get_quiz', methods=['GET'])
@login_required
def get_quiz_list():
    if current_user == "admin":
        prefix = request.args.get('prefix', '').lower()
        return jsonify(get_quiz(prefix))
    else:
        return render_template('404.html')

@main.route('/api/get_matter', methods=['GET'])
@login_required
def get_matter_list():
    if current_user == 'admin':
        prefix = request.args.get('prefix', '').lower()
        return jsonify(get_matter(prefix))
    else:
        return render_template('404.html')

@main.post('/api/edit_quiz')
@login_required
def edit_quiz():
    if current_user == 'admin':

        data = request.get_json()
        title = res_data.get('title')
        theme = res_data.get('theme').lower()
        status = Bool(res_data['status'])
        data = json.dumps(res_data.get('data'))
        quiz = Quiz.query.filter(Quiz.title ==  title).first()
        if quiz:
            quiz.title = title
            quiz.theme = theme 
            quiz.data = data 
            quiz.status = status 
            db.session.commit()
            return json({"status:":"done"}),200
        else:
            return jsonify({"error","mavjud emas"}),404
    else:
        abort(404)


@main.post('/api/edit_matter')
@login_required
def edit_matter():
    if current_user == 'admin':
        data = request.get_json()
        title = res_data['title']
        main = res_data['main']
        helper = res_data['helper']
        theme = res_data['theme']
        correct = res_data['correct']
        ball = int(res_data['ball'])
        status = Bool(res_data['status'])
        
        matter = Matter.query.filter(Quiz.title ==  title).first()
        if matter:
            matter.title = title
            matter.main = main 
            matter.helper = helper
            matter.theme = theme 
            matter.correct = correct
            matter.ball = ball  
            matter.status = status 
            db.session.commit()
            return json({"status:":"done"}),200
        else:
            return jsonify({"error","mavjud emas"}),404
    else:
        abort(404)

@main.route("/api/delete_theme/<int:item_id>", methods=["DELETE"])
@login_required
def delete_theme(item_id):
    if current_user == "admin":
        item = Theme.query.get(item_id)
        if item:
            db.session.delete(item)
            db.session.commit()
            return jsonify({"message": "Item deleted successfully"}), 200
        return jsonify({"error": "Item not found"}), 404
    else:
        return "Doom shot, Mother Fucker)"

@main.route("/api/delete_quiz/<int:item_id>", methods=["DELETE"])
@login_required
def delete_quiz(item_id):
    if current_user == "admin":
        item = Quiz.query.get(item_id)
        if item:
            db.session.delete(item)
            db.session.commit()
            return jsonify({"message": "Item deleted successfully"}), 200
        return jsonify({"error": "Item not found"}), 404
    else:
        return "Doom shot, Mother Fucker)"

@main.route("/api/delete_matter/<int:item_id>", methods=["DELETE"])
@login_required
def delete_matter(item_id):
    if current_user == "admin":
        item = Matter.query.get(item_id)
        if item:
            db.session.delete(item)
            db.session.commit()
            return jsonify({"message": "Item deleted successfully"}), 200
        return jsonify({"error": "Item not found"}), 404
    else:
        return "Doom shot, Mother Fucker)"
         
    
@main.route('/matters/')
def matters():
    themes = get_all_themes()
    return render_template('matters.html',themes=themes)


@main.route("/tests/")
def tests():
    themes = get_all_themes()
    return render_template('tests.html',themes=themes)

@main.route('/tests/<name>')
def show_tests(name):
    tests = Quiz.query.filter(Quiz.theme == name).all()
    user_id = current_user.id 
    quiz_status = {}
    for test in tests:
        quiz_status[test.id] = check_history(user_id, test.id, "quiz")

    return render_template('show_tests.html', name=name, tests=tests, quiz_status=quiz_status)


@main.route('/tests/<theme>/<int:quiz_id>', methods=["GET", "POST"])
def calc_test(theme, quiz_id):
    quiz = Quiz.query.filter_by(id=quiz_id).first()
    print(quiz.data)
    if not quiz: 
        abort(404)
    
    questions = json.loads(quiz.data)
    if request.method == 'POST':    
        questions_dict = {f'question-{q["id"]}': q for q in questions}
        answers = {f'question-{q["id"]}': request.form.get(f'question-{q["id"]}') for q in questions}
        correct_answers = {f'question-{q["id"]}': q['answer'] for q in questions} 
        score = users_ball = 0  
        for qid, answer in answers.items(): 
            correct_answer = correct_answers.get(qid)  
            if answer == correct_answer:  
                score += 1  
                users_ball += int(questions_dict[qid]['ball'])
        
        save_user_progress(user_id=current_user.id,item_id=quiz.id,points=users_ball,x_type="quiz")
        return render_template('result_test.html',ball=users_ball, score=score, total=len(correct_answers))
    else:
        return render_template('calc_test.html', questions=questions,theme=theme)

@main.route('/matters/<name>')
def show_matter(name):
    page = request.args.get('page', 1, type=int)
    per_page = 10

    matters = Matter.query.filter(Matter.theme == name).paginate(page=page, per_page=per_page, error_out=False)

    user_id = current_user.id 

    for matter in matters.items:
        history = check_history(user_id, matter.id, "matter")
        matter.solved = history['status']

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
            save_user_progress(user_id=current_user.id,item_id=matter.id,points=matter.ball,x_type="matter")
            flash(f"✅ To‘g‘ri javob! ({user_answer})", "success")
            
        else:
            flash(f"❌ Noto‘g‘ri javob! To‘g‘ri javob: {correct_answer}", "danger")

        return redirect(url_for('main.calc_matter', theme=theme, matter_id=matter_id)) 

    return render_template('calc_matter.html', problem=matter,theme=theme)

@main.route("/team")
def team():
    return render_template("team.html")

@main.route('/leaderboard')
def leaderboard():
    top_users = get_leaderboard()
    ranked_users = [(rank + 1, user, total_points) for rank, (user, total_points) in enumerate(top_users)]

    print("top_users:", top_users)
    print("ranked_users:", ranked_users)

    return render_template('leaderboard.html', ranked_users=ranked_users)
    
@main.route('/lab')
def lab():
    return render_template('lab_list.html')

@main.route('/lab/<id>')
def show_lab(id):
    return render_template('lab.html',id=id)

@main.route("/labaratory/<int:id>")
def lab_page(id):
    return render_template(f'lab/{id}/index.html')

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
        username = form.username.data.replace(" ", "")
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
            flash('Malumotlar yangilandi!', 'success')
        except Exception as e:
            db.session.rollback() 
            flash(f'Error updating profile: {str(e)}', 'danger')

        return redirect(url_for('main.profile'))

    return render_template('profile.html',ball=ball, user=current_user, form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Siz muvaffaqiyatli chiqdingiz.", "success")
    return redirect(url_for('main.login_page'))
