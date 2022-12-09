import os
import pymysql
from flask import Flask, render_template, jsonify, request, redirect, flash, session
from werkzeug.utils import secure_filename
import urllib.request
from datetime import datetime

UPLOAD_FOLDER = 'static/img'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # flash 사용
app.config["SECRET_KEY"] = "1234"

db = pymysql.connect(user="root", passwd="qwe1357asd!", host="localhost", db="dailycafe", charset="utf8")
curs = db.cursor()

@app.route('/')
def home():
    return redirect('/my_page')

@app.route('/my_page')
def my_page():
    return render_template('my_page.html')

@app.route('/edit_page')
def edit_page():
    return render_template('edit_page.html')

@app.route('/users/<id>', methods=['GET'])
def get_users(id):
    db = pymysql.connect(user="root",
                         passwd="qwe1357asd!",
                         host="localhost",
                         db="dailycafe",
                         charset="utf8")
    # connection 으로부터 cursor(fetch 역할) 생성
    curs = db.cursor()
    # 쿼리문 작성
    sql = '''SELECT `name`,`desc`,`img` FROM `users` AS u WHERE u.id = %s'''

    # 쿼리 실행
    curs.execute(sql, id)

    # 결과 받고 컨트롤 하기 / 전체 데이터 패치
    rows = curs.fetchall()

    # print(rows)

    db.commit()
    db.close()
    # 결과 값 저장
    result = {
        "name": rows[0][0],
        "desc": rows[0][1],
        "img": rows[0][2]
    }

    return jsonify({'users': result}), 200


@app.route('/users/<id>', methods=['POST'])
def post_users(id):
    db = pymysql.connect(user="root", passwd="qwe1357asd!", host="localhost", db="dailycafe", charset="utf8")
    curs = db.cursor()

    name_receive = request.form['name']
    desc_receive = request.form['desc']

    sql = '''UPDATE `users` SET name=%s, `desc`=%s  WHERE id=%s;'''

    curs.execute(sql, (name_receive, desc_receive, id))

    db.commit()
    db.close()

    flash("수정이 완료되었습니다")
    return render_template("my_page.html")


# 파일 업로드
# rsplit은 뒤에서 부터의 값을 끊어주는 것 = 파일의 확장자명 저장
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route("/upload", methods=['GET', 'POST'])
def upload():
    # 아래 섹션 나중에 지워야됨
    session['email'] = "haebin1622@naver.com"
    db = pymysql.connect(user="root", passwd="qwe1357asd!", host="localhost", db="dailycafe", charset="utf8")
    cur = db.cursor(pymysql.cursors.DictCursor)
    # 저장 시간 저장
    now = datetime.now()
    # 이메일 세션 저장
    up_email = session['email']
    # method = post 이면
    if request.method == 'POST':
         # input 타입의 태그 이름을 files에 저장
        files = request.files.getlist('files[]')
        for file in files:
            # 만약 파일이 {'png', 'jpg', 'jpeg'} 이와 같은 확장자와 일치하면
            if file and allowed_file(file.filename):
                # 어려워
                filename = secure_filename(file.filename)
                # 이건 더
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                # users 테이블 안에 있는 세션 저장한 email의 img, upload_time의 컬럼 값을 변경
                sql = f'UPDATE users SET img="{filename}",upload_time="{now}" WHERE email="{up_email}";'
                # sql 쿼리문 실행
                cur.execute(sql)
                # 커밋 및 연결 종료
                db.commit()
                db.close()
        # alert 띄워주기
        flash('사진이 성공적으로 업로드 되었어요!')
    # edit 페이지로 돌아가기
    return redirect('/edit_page')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
