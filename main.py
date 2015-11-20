from flask import Flask, url_for,render_template
app = Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/main/<name>')
def main(name=None):
    return render_template('main.html', name=name)

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/hello2/')
@app.route('/hello2/<title>&<name>')
def hello2(name=None, title=None):
    data={
        'title' : title,
        'name' : name   
    }
    return render_template('hello2.html', **data)

@app.route('/hello3/')
def hello3():
    data=[dict(href="http://naver.com", caption="네이버"), 
          dict(href="http://www.google.com", caption="구글")]
    return render_template('hello3.html', items=data)



if __name__ == '__main__':
    app.debug=True
    app.run(port=5000)

