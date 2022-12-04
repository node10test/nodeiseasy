from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
   return render_template('index.html')
@app.route('/index2')
def home2():
   return render_template('index2.html')



if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)