from flask import Flask, url_for,render_template, request
app = Flask(__name__)



# 기본루트페이지
@app.route('/')
def index():
    return render_template('map.html')
#hhhh
@app.route('/map/', methods=['POST'])
def map():
    if request.method == 'POST':
        data={
            #'sex' : request.form['sex'],
            #'age' : request.form['age']
            'sex' : request.form.get('sex', None)
        }
        return render_template('map.html', data=data)
    else:
        return render_template('map.html')


# 커뮤니티
@app.route('/community/')
def community():
    return render_template('community.html')

# 로그인
@app.route('/login')
@app.route('/login/<name>')
def hello(name=None):
    return render_template('login.html', name=name)



################### 예제 그냥 남겨놓은거 #################
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
######################################################


if __name__ == '__main__':
    app.debug=True
    app.run(port=5000)

