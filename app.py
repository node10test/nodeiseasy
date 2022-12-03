from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

@app.route('/')
def home():
return render_template('index.html')

@app.route("/bucket", methods=["POST"])
def bucket_post():
sample_receive = request.form['sample_give']
print(sample_receive)
return jsonify({'msg': 'POST(기록) 연결 완료!'})

@app.route("/bucket/done", methods=["POST"])
def bucket_done():
sample_receive = request.form['sample_give']
print(sample_receive)
return jsonify({'msg': 'POST(완료) 연결 완료!'})

@app.route("/bucket", methods=["GET"])
def bucket_get():
return jsonify({'msg': 'GET 연결 완료!'})

if __name__ == '__main__':
app.run('0.0.0.0', port=5000, debug=True)