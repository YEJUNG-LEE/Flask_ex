from flask import current_app, flash, request, redirect, session, render_template, url_for, jsonify
from . import main
from ..models import User
from .. import db
from sqlalchemy.sql.expression import func
import os


@main.route('/')
def index():
    # 메인 페이지
    user = None
    if 'id' in session:
        user = User.query.filter_by(id = session['id']).first_or_404()

    return render_template('main.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    # 로그인
    if request.method == 'POST':
        id = request.form['id']
        pw = request.form['password']
        password_hash = db.session.query(func.sha2(pw, 224))
        user = User.query.filter_by(user_id = id, password_hash = password_hash).first()

        if not user:
            flash('존재하지 않는 아이디거나 비밀번호가 올바르지 않습니다')
            return redirect(url_for('.login'))

        session['id']=user.id

        return redirect(url_for('.index'))

    return render_template('main/login.html')


@main.route('/register', methods=['GET', 'POST'])
def register():
    # 회원가입
    if request.method == 'POST':
        data = request.get_json
        if 'id' in data:
            user = User.query.filter_by(user_id = data['user_id']).first()

            if user:
                return jsonify(data = False)
            else:
                return jsonify(data = True)
        
        elif 'user_name' in data:
            # 닉네임 중복체크
            user = User.query.filter_by(username = data['user_name']).first()

            if user:
                return jsonify(data = False)
            else:
                return jsonify(data = True)
        elif 'form' in data:
            # 회원가입 submit
            try:
                password_hash = db.session.query(func.sha2(data["form"]["password"], 224))
                user = User(user_id = data['form']['id'], username = data["form"]["username"], password_hash = password_hash)
                db.session.add(user)
                db.session.commit()
                os.mkdir(os.path.join(current_app.config['PROFILE_PATH'], user.user_id))
            except Exception as e:
                return jsonify(data = False, msg = e)

            return jsonify(data = True)
    return render_template('main/register.html')