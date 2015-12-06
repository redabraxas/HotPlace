from flask import Flask, url_for,render_template, request,session,g,redirect,\
    abort,flash,Markup
import xml.etree.ElementTree as ET
import sqlite3
import time



#configuration
DATABASE='test.db'
DEBUG=True
SECRET_KEY='development key'
USERNAME='admin'
PASSWORD='default'

app = Flask(__name__)
app.config.from_object(__name__) #대문자로 설정된 값들을 config에 추가


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])
def init_commdb():
    con=sqlite3.connect("test.db")
    cur=con.cursor()
    userSql = '''create table if not exists user(
        id varchar(20) not null,
        passwd varchar(20),
        nick varchar(20),
        primary key (id)

        );'''

    localCommSql='''create table if not exists localcomm(
        w_category varchar(10),
        w_area varchar(10),
        w_year integer,
        w_month integer,
        w_day integer,
        w_title text,
        w_content integer,
        w_num integer not null primary key autoincrement,
        w_userid varchar(20),
        foreign key (w_userid) references user(id) ON UPDATE CASCADE
        );'''
    localReplySql='''create table if not exists localReply(
        r_num integer not null primary key autoincrement,
        r_userid varchar(20),
        r_content text,
        r_year integer,
        r_month integer,
        r_day integer,
        foreign key(r_userid) references user(id) ON UPDATE CASCADE
        );'''
    cur.execute(userSql)
    cur.execute(localCommSql)

    cur.execute(localReplySql)
    con.commit()


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
        con.commit()

def init_userdb():
    db=connect_db()
    userSql = '''create table if not exists user(
    id string primary key,
    passwd string not null,
    nick string not null
    );
    '''
    db.cursor().execute(userSql)
    db.commit()

def init_bookmark():
    #con=sqlite3.connect("test.db")
    #cur=con.cursor()
    #즐겨찾기 테이블 추가
    #id 외래키로 가져오는 방법..?

    bookmarksql='''create table if not exists bookmark(
        b_num integer not null,
        b_id varchar(20) not null,
        mapx double,
        mapy double,
        zoom integer,
        p_year integer,
        p_month integer,
        p_day integer,
        isholiday varchar(10),
        p_time varchar(10),
        location varchar(30),
        weather varchar(10),
        man10 integer,
        man20 integer,
        man30 integer,
        man40 integer,
        man50 integer,
        woman10 integer,
        woman20 integer,
        woman30 integer,
        woman40 integer,
        woman50 integer,
        tag varchar(30),
        primary key(b_num)
    );'''

    cur.execute(bookmarksql)
    #con.commit()    
   
def read_db():
    con=sqlite3.connect("test.db")
    cur=con.cursor()
    cur.execute("select * from population ")
    print(cur.fetchall())


def getSearchMap(data):

    # data.sex, data.age, data.month, data.time -> 전부 리스트 타입으로 사용자가 택한 값만 들어있습니다.
    # ex) data['sex'] = [man, woman]  data.age=[10,40] data.month =[1,5,6]  data.time=[afternoon, evening]
    
    ageflag = [0]*10
    where_query = "where "
    for i in range(len(data['sex'])):
        sextemp = data['sex'].pop()
        if('man' == sextemp):
            agecount=5
            agesize = len(data['age'])
            for i in range(agesize):
                #마지막 원소를 첫원소에 저장
                agetemp2 = data['age'].pop()
                data['age'].insert(0,agetemp2)
                if(agetemp2 == 0):
                    agecount=agecount-1
                    continue
                else:
                    agetemp = str(agetemp2)
                    if(5 == agecount):
                        where_query+='man50>'
                        where_query+=agetemp
                        where_query+=' and '
                        ageflag[0]=1;
                    elif(4 == agecount):
                        where_query+='man40>'
                        where_query+=agetemp
                        where_query+=' and '
                        ageflag[1]=1;
                    elif(3 == agecount):
                        where_query+='man30>'
                        where_query+=agetemp
                        where_query+=' and '
                        ageflag[2]=1;
                    elif(2 == agecount):
                        where_query+='man20>'
                        where_query+=agetemp
                        where_query+=' and '
                        ageflag[3]=1;
                    elif(1 == agecount):
                        where_query+='man10>'
                        where_query+=agetemp
                        where_query+=' and '
                        ageflag[4]=1;
                    agecount=agecount-1
                
        elif('woman' == sextemp):
            agecount=5
            agesize = len(data['age'])
            for i in range(agesize):
                agetemp2 = data['age'].pop()
                data['age'].insert(0,agetemp2)
                if(agetemp2 == 0):
                    agecount=agecount-1
                    continue
                else:
                    agetemp = str(agetemp2)
                    if(5 == agecount):
                        where_query+='woman50>'
                        where_query+=agetemp
                        where_query+=' and '
                        ageflag[5]=1;
                    elif(4 == agecount):
                        where_query+='woman40>'
                        where_query+=agetemp
                        where_query+=' and '
                        ageflag[6]=1;
                    elif(3 == agecount):
                        where_query+='woman30>'
                        where_query+=agetemp
                        where_query+=' and '
                        ageflag[7]=1;
                    elif(2 == agecount):
                        where_query+='woman20>'
                        where_query+=agetemp
                        where_query+=' and '
                        ageflag[8]=1;
                    elif(1 == agecount):
                        where_query+='woman10>'
                        where_query+=agetemp
                        where_query+=' and '
                        ageflag[9]=1;
                    agecount=agecount-1                
    for i in range(len(data['month'])):
        where_query+='p_month='
        where_query+=str(data['month'].pop())
        where_query+=' and '
    for i in range(len(data['time'])):
        timetemp = data['time'].pop() 
        where_query+='p_time like'
        if('afternoon' == timetemp):
            where_query+=" '%12시%'"
        elif('evening' == timetemp):
            where_query+=" '%19시%'"    
        where_query+=' and '
    
    #and 제거
    where_query = where_query[:len(where_query)-5]
    where_query+= " order by maxpop desc;"

    #부속질의문 사용
    #man10 - woman50
    where_query2 = "(select Max("
    agetemp2=0
    for i in range(10):
        if(ageflag[i]==1):
            if(i>=5):
                agetemp2=50
                where_query2+="wo"
            where_query2+="man"
            where_query2+=str(50-i*10+agetemp2)
            where_query2+=", "
    #쉼표 제거
    where_query2 = where_query2[:len(where_query2)-2]
    where_query2+=")) as maxpop"
    
    cur = g.db.execute('select *, '+where_query2+' from population '+where_query)
    #부속질의문 사용 끝
    
    entries = [dict(year=row[1], month=row[2],  day=row[3],  time=row[5], isholiday=row[4],  
        location=row[6], mapx=row[7], mapy=row[8], weather=row[9], 
        man10=row[10], man20=row[11], man30=row[12], man40=row[13], man50=row[14],
        woman10=row[15], woman20=row[16], woman30=row[17], woman40=row[18], woman50=row[19]
        ) for row in cur.fetchall()]
    return entries;

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
            'sex' :request.form.getlist('sex', None),
            'age' : request.form.getlist('age[]', None),
            'month' : request.form.getlist('month', None),
            'time' : request.form.getlist('time', None)
        }

        entries= getSearchMap(data=data);
        return render_template('map.html', data=data, entries=entries)
    else:
        return render_template('map.html')





# 로그인
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    if request.method == 'POST':
        query="select id, passwd, nick from user where (id = '" +request.form['id']+ "') and (passwd = '" +request.form['passwd']+"')"
        cur=g.db.execute(query)
        row=cur.fetchone()

        if row==None:
            flash('아이디와 비밀번호를 확인해주세요.')
            return redirect(url_for('login'))
        else:
            session['logged_in'] = True
            session['nick']=row[2]
            #flash('You were logged in')
            return redirect(url_for('index'))


#회원가입
@app.route('/join',methods=['GET','POST'])
def join():
    if request.method=='GET':
        return render_template('join.html')
    elif request.method=='POST':
        #logid=request.form['id']
        #logpass=request.form['passwd']
        #lognick=request.form['nick']

        query="select id from user where id = '" +request.form['id']+ "'";
        query2="select nick from user where nick = '" +request.form['nick']+ "'";
        
        #아이디 중복체크
        cur=g.db.execute(query)
        row=cur.fetchone()

        #닉네임 중복체크
        cur2=g.db.execute(query2)
        row2=cur2.fetchone()

        print(row)
        if row!=None:
            flash('동일한 아이디가 이미 존재합니다.')
            return redirect(url_for('join'))
        elif row2!=None:
            flash('동일한 닉네임이 이미 존재합니다.')
            return redirect(url_for('join'))
        else:
            g.db.execute('insert into user(id,passwd,nick) values(?,?,?)',
                         [request.form['id'],request.form['passwd'],request.form['nick']])
            g.db.commit()
            flash('회원가입이 완료되었습니다.')
            return redirect(url_for('index'))
        
        #return render_template('join.html')
    else:
        abort(405)
    #if not session.get('logged_in'):
    #    abort(401)
    

#로그아웃
@app.route('/logout')
def logout():
    session.pop('logged_in',None)
    #flash('You were logged out')
    return redirect(url_for('index'))

#######start local community part #######
@app.route('/localcomm/')
def localcomm():
    cur = g.db.execute('select w_category,w_area,w_title,w_content,w_year,w_month,w_day,w_userid, w_num from localcomm order by w_num desc')
    entries = [dict(w_category=row[0], w_area=row[1],w_title=row[2],w_content=row[3],w_year=row[4],w_month=row[5],w_day=row[6],w_userid=row[7],num=row[8]) for row in cur.fetchall()]
    print(entries)
    return render_template('localcomm.html', entries = entries)
    
@app.route('/community/')
def community():
    return render_template('community.html')

@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/adding', methods=['POST'])
def adding():
    now = time.localtime()
    Category = request.form['category']
    Area = request.form['area']
    Title = request.form['title']
    Content = request.form['content']
    Year = now.tm_year
    Month = now.tm_mon
    Day = now.tm_mday
    Writer = session['nick']
    #Id = request.form['category']
    g.db.execute('insert into localcomm (w_category,w_area,w_title,w_content,w_year,w_month,w_day,w_userid) values (?,?,?,?,?,?,?,?);',(Category,Area,Title,Content,Year,Month,Day,Writer,));
    g.db.commit()
    return redirect(url_for('localcomm'))

#@app.route('/showpost/<wnum>', methods=['POST'])
#def showpost(wnum):
#    num=int(wnum);
#    cur = g.db.execute('select w_category,w_area,w_title,w_content,w_year,w_month,w_day,w_num from localcomm where w_num=num;')
#    entries2 = [dict(w_category=row[0], w_area=row[1],w_title=row[2],w_content=row[3],w_year=row[4],w_month=row[5],w_day=row[6],w_num=row[7]) for row in cur.fetchall()]
#    return render_template('showpost.html', entries2 = entries2)
@app.route('/showpost/<wnum>')
def showpost(wnum):
    num=int(wnum);
    cur = g.db.execute('select w_category,w_area,w_title,w_content,w_year,w_month,w_day,w_userid,w_num from localcomm where w_num=(?);',(num,))
    entries2 = [dict(w_category=row[0], w_area=row[1],w_title=row[2],w_content=row[3],w_year=row[4],w_month=row[5],w_day=row[6],userid=row[7],num=row[8]) for row in cur.fetchall()]
    return render_template('showpost.html', entries2 = entries2)

@app.route('/delpost/<wnum>')
def delpost(wnum):
    num=int(wnum)
    cur=g.db.execute('select w_userid from localcomm where w_num=(?);',(num,))
    for row in cur:
        wname=row[0]
    if (session['nick']==wname) or (session['nick']=="admin"):
        g.db.execute('delete from localcomm where w_num=(?)',(wnum,))
        g.db.commit()
        return redirect(url_for('localcomm'))
    else:
        return session['nick']



#######end local community part #######



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
    #init_userdb()
    #init_bookmark()
    #init_commdb()
    #connect_db()
    app.debug=True
    app.run(port=5000)

