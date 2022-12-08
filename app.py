import pymysql
from flask import Flask, render_template, request, flash, session, jsonify, redirect, url_for
import json

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


@app.route('/join', methods=['POST'])
def signup():
    db = pymysql.connect(host='hjdb.cmux79u98wpg.us-east-1.rds.amazonaws.com',
                         port=3306, user='master', passwd='Abcd!234', db='hjdb', charset='utf8')
    cursor = db.cursor()

    details = request.form
    user_id = details.getlist('join-id')[0]
    user_pw = details.getlist('join-pw')[0]
    pw_confirm = details.getlist('join-confirm')[0]
    name = details.getlist('join-username')[0]
    email = details.getlist('join-email')[0]
    sql = """
            SELECT * FROM users
            where user_id = (%s)
    """
    cursor.execute(sql, user_id)
    id_check_result = cursor.fetchone()
    if id_check_result != None:
        db.commit()
        db.close()
        flash("이미 가입된 아이디입니다. 다른 아이디를 선택하세요.")
        return render_template('register.html')
    else:
        sql = """
            SELECT * FROM users
            where email = (%s)
        """
        cursor.execute(sql, email)
        email_check_result = cursor.fetchone()
        if email_check_result != None:
            db.commit()
            db.close()
            flash("이미 가입된 이메일 입니다.")
            return render_template('register.html')
        elif user_pw == pw_confirm:
            sql = """
                INSERT INTO
                users(
                    user_id
                    , user_pawward
                    , user_name
                    , email
                    )
                    VALUES
                    (%s, %s, %s, %s)
            """
            cursor.execute(sql, (user_id, user_pw, name, email))
            db.commit()
            db.close()
            flash("회원가입이 완료되었습니다.")
            return redirect(url_for('login'))
        else:
            db.commit()
            db.close()
            flash("비밀번호 확인이 일치하지 않습니다.")
            return render_template('register.html')
    # return redirect(url_for('login'))


@app.route('/users/<user_id>/edit')
def edit_profile(user_id):
    page_title = f"#{user_id} EDIT"
    return render_template('edit-profile.html', pageTitle=page_title)


@app.route('/questions')
def get_problems():
    db = pymysql.connect(host='hjdb.cmux79u98wpg.us-east-1.rds.amazonaws.com',
                         user='master', db='hjdb', password='Abcd!234', charset='utf8')
    curs = db.cursor()

    sql = """
    SELECT *
    FROM problem
    """

    curs.execute(sql)

    rows = curs.fetchall()
    json_str = json.dumps(rows, indent=4, sort_keys=True,
                          default=str, ensure_ascii=False)
    db.commit()
    db.close()
    return json_str, 200


@app.route('/questions', methods=['POST'])
def save_problems():
    db = pymysql.connect(host='hjdb.cmux79u98wpg.us-east-1.rds.amazonaws.com',
                         user='master', db='hjdb', password='Abcd!234', charset='utf8')
    curs = db.cursor()
    print(request.form)
    title = request.form.getlist('question-add-form__title')[0]
    comment = request.form.getlist('question-add-form__content')[0]
    user_unique_id = session['_id']

    sql = """insert into problem (problem_title, problem_comment, user_unique_id)
         values (%s,%s,%s)
        """
    curs.execute(sql, (title, comment, user_unique_id))

    # # # rows = curs.fetchall()

    # # # json_str = json.dumps(rows, indent=4, sort_keys=True, default=str)
    db.commit()
    db.close()
    return redirect(url_for("home"))


@app.route('/questions/<quiz_id>')
def get_quiz(quiz_id):
    page_title = f"Question. {quiz_id}"
    db = pymysql.connect(host='hjdb.cmux79u98wpg.us-east-1.rds.amazonaws.com', user='master', password='Abcd!234',
                         db="hjdb", port=3306)
    curs = db.cursor()
    sql = """
    select p.problem_comment from problem as p 
    where p.problem_id =(%s)  """
    curs.execute(sql, quiz_id)
    rows = curs.fetchall()

    return render_template('question.html', pageTitle=page_title, quizId=quiz_id, quizContent=rows[0][0])


@app.route('/review')
def get_problem():
    db = pymysql.connect(host='hjdb.cmux79u98wpg.us-east-1.rds.amazonaws.com', user='master', password='Abcd!234',
                         db="hjdb", port=3306)
    curs = db.cursor()

    problem_id = int(request.args.get('problem_id_give'))

    sql = """
    select p.problem_id, p.problem_title , p.problem_comment,r.review_id,r.review_title,r.review_comment 
    from review as r 
    inner join problem as p 
    on r.problem_id = p.problem_id 
    where p.problem_id =(%s)  """
    curs.execute(sql, problem_id)
    rows = curs.fetchall()

    json_str = json.dumps(rows, indent=4, sort_keys=True,
                          default=str, ensure_ascii=False)
    db.commit()
    db.close()
    return json_str, 200


@app.route('/review', methods=['POST'])
def insert_review_post():
    db = pymysql.connect(host='hjdb.cmux79u98wpg.us-east-1.rds.amazonaws.com', user='master', password='Abcd!234',
                         db="hjdb", port=3306)
    curs = db.cursor()

    data = request.form
    problem_id = data.getlist('question-add-form__hashtag')[0][-1]
    review_title = data.getlist('question-add-form__title')
    review_comment = data.getlist('question-add-form__content')
    user_id = session['_id']

    sql = """insert into review (
                                                 problem_id,
                                                 review_title,
                                                 review_comment,
                                                 user_unique_id)
                                             values (%s,%s,%s,%s)"""
    curs.execute(sql, (problem_id, review_title, review_comment, user_id))

    db.commit()  # 확정
    db.close()  # 닫기
    return redirect(f"/questions/{problem_id}")


@app.route('/review', methods=['DELETE'])
def delete_review():
    db = pymysql.connect(host='hjdb.cmux79u98wpg.us-east-1.rds.amazonaws.com', user='master', password='Abcd!234',
                         db="hjdb", port=3306)
    curs = db.cursor()
    review_id_receive = request.form.get('review_id_give')
    print(review_id_receive)
    print(type(review_id_receive))
    sql = """ delete from review where review_id = (%s);"""
    curs.execute(sql, review_id_receive)

    db.commit()  # 확정
    db.close()  # 닫기
    return jsonify({'msg': '삭제완료!'})


@app.route('/review', methods=['UPDATE'])
def update_review():
    db = pymysql.connect(host='hjdb.cmux79u98wpg.us-east-1.rds.amazonaws.com', user='master', password='Abcd!234',
                         db="hjdb", port=3306)
    curs = db.cursor()
    review_id_receive = request.form.get(
        'review_id_give')  # id 번째 title, comment 를 받아와서 바꿔
    review_title_receive = request.form.get('review_title_give')
    review_comment_receive = request.form.get('review_comment_give')
    print(review_comment_receive, review_title_receive)
    sql = """ update review set review_title = (%s), review_comment = (%s) where review_id = (%s);"""
    curs.execute(sql, (review_title_receive,
                 review_comment_receive, review_id_receive))

    db.commit()  # 확정
    db.close()  # 닫기
    return jsonify({'msg': '수정완료!'})

if __name__ == '__main__':

    app.run('0.0.0.0', port=5000, debug=True)
