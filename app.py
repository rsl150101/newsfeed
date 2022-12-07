import pymysql
from flask import Flask, render_template, request, flash, session, jsonify, redirect, url_for

db = pymysql.connect(host='hjdb.cmux79u98wpg.us-east-1.rds.amazonaws.com',
                     port=3306, user='master', passwd='Abcd!234', db='hjdb', charset='utf8')
app = Flask(__name__)
app.config["SECRET_KEY"] = "asdfasdfas21341oiwejvcval1eaf"


@app.route('/')
def home():
    page_title = "HOME"
    return render_template('index.html', pageTitle=page_title)


@app.route('/login')
def login():
    page_title = "LOGIN"
    return render_template('login.html', pageTitle=page_title)


@app.route('/login', methods=['POST'])
def signin():
    db = pymysql.connect(host='hjdb.cmux79u98wpg.us-east-1.rds.amazonaws.com',
                         port=3306, user='master', passwd='Abcd!234', db='hjdb', charset='utf8')
    cursor = db.cursor()  # db 문 열기

    details = request.form
    user_id = details.getlist('login-id')[0]
    user_pw = details.getlist('login-pw')[0]
    if len(user_id) == 0 or len(user_pw) == 0:
        flash("아이디 혹은 비밀번호가 입력되지 않았습니다.")
        return render_template('login.html')
    else:
        sql = """
            SELECT unique_id,user_id, user_pawward, user_name FROM users
            where user_id = (%s)
        """
        cursor.execute(sql, user_id)
        user_in_db = cursor.fetchone()

        if user_in_db == None:
            flash("존재하지 않는 아이디입니다.")
            db.commit()  # db 저장
            db.close()  # db 문 닫기
            return render_template('login.html')
        elif int(user_pw) == user_in_db[2]:
            user_name = user_in_db[3]
            session['login_flag'] = True
            session['user_id'] = user_id
            session['_id'] = user_in_db[0]
            message = "{}님 환영합니다!".format(user_name)
            flash(message)
            db.commit()
            db.close()
            return redirect(url_for('home'))
        else:
            flash("잘못된 비밀번호를 입력하셨습니다.")
            db.commit()
            db.close()
            return render_template('login.html')


@app.route('/logout')
def logout():
    flash("로그아웃 되었습니다.")
    session['login_flag'] = False
    session['user_id'] = ""
    return redirect(url_for('home'))


@app.route('/join')
def join():
    page_title = "JOIN"
    return render_template('join.html', pageTitle=page_title)


@app.route('/users/<user_id>/edit')
def edit_profile(user_id):
    page_title = f"#{user_id} EDIT"
    return render_template('edit-profile.html', pageTitle=page_title)


@app.route('/questions/<quiz_id>')
def get_quiz(quiz_id):
    page_title = f"Question. {quiz_id}"
    return render_template('question.html', pageTitle=page_title)


if __name__ == '__main__':

    app.run('0.0.0.0', port=5000, debug=True)
