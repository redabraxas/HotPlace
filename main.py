﻿from flask import Flask, url_for,render_template, request,session,g,redirect,\
    abort,flash
import xml.etree.ElementTree as ET
import sqlite3

app = Flask(__name__)

#configuration
DATABASE='test.db'

app=Flask(__name__)
app.config.from_object(__name__) #대문자로 설정된 값들을 config에 추가

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():

    tree=ET.parse("population.xml")
    note=tree.getroot()

    con=sqlite3.connect("test.db")
    cur=con.cursor()
    sql='''create table if not exists population(num integer,p_year integer,p_month integer,p_day integer,
    isholiday text,p_time text,location text,mapx real,mapy real,
    weather text,man10 integer,man20 integer,man30 integer,man40 integer,man50 integer,
    woman10 integer,woman20 integer,woman30 integer,woman40 integer,woman50 integer);'''
    cur.execute(sql)

    for child in note.findall("record"):
        num=child.findtext("조사번호")
        day=child.findtext("조사일자") 
    
        temp=day.split("-")
        p_year=temp[0]
        p_month=temp[1]
        p_day=temp[2]

        isholiday=child.findtext("주구분")
        p_time=child.findtext("시간대")
        location=child.findtext("행정구역명")
        mapx=child.findtext("X좌표")
        mapy=child.findtext("Y좌표")
        weather=child.findtext("날씨")
        man10=child.findtext("남자10대")
        man20=child.findtext("남자20대")
        man30=child.findtext("남자30대")
        man40=child.findtext("남자40대")
        man50=child.findtext("남자50대")
        woman10=child.findtext("여자10대")
        woman20=child.findtext("여자20대")
        woman30=child.findtext("여자30대")
        woman40=child.findtext("여자40대")
        woman50=child.findtext("여자50대")

        insertsql='''insert into population values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);'''
        cur.execute(insertsql,(num,p_year,p_month,p_day,isholiday,p_time,location,mapx,mapy,weather,man10,man20,man30,man40,man50,woman10,woman20,woman30,woman40,woman50))
        #con.commit()
    
   
def read_db():
    con=sqlite3.connect("test.db")
    cur=con.cursor()
    cur.execute("select * from population ")
    print(cur.fetchall())


@app.before_request
def before_request():
    g.db=connect_db() #g:flask의 전역 클래스 인스턴스

@app.teardown_request
def teardown_request(exception):
    g.db.close()

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
    #init_db()
    app.debug=True
    app.run(port=5000)

