from flask import Flask, url_for,render_template, request,session,g,redirect,\
    abort,flash,Markup
import xml.etree.ElementTree as ET
import sqlite3
import time
from urllib.request import urlopen
from urllib.parse import urljoin, urlencode
from bs4 import BeautifulSoup
import json

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
    #userSql = '''create table if not exists user(
    #    id varchar(20) not null,
    #    passwd varchar(20),
    #    nick varchar(20),
    #    primary key (id)

    #    );'''

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
        r_wnum integer,
        r_num integer not null primary key autoincrement,
        r_userid varchar(20),
        r_content text,
        r_year integer,
        r_month integer,
        r_day integer,
        foreign key(r_userid) references user(id) ON UPDATE CASCADE
        foreign key(r_wnum) references localcomm(w_num) ON UPDATE CASCADE
        );'''
    infoCommSql='''create table if not exists information(
        i_category varchar(10),
        i_year integer,
        i_month integer,
        i_day integer,
        i_title text,
        i_content integer,
        i_num integer not null primary key autoincrement,
        i_userid varchar(20),
        foreign key (i_userid) references user(id) ON UPDATE CASCADE
        );'''
    infoReplySql='''create table if not exists infoReply(
        ir_year integer,
        ir_month integer,
        ir_day integer,
        ir_content text,
        ir_num integer not null primary key autoincrement,
        ir_userid varchar(20),
        ir_inum integer,
        foreign key (ir_userid) references user(id) ON UPDATE CASCADE
        foreign key (ir_inum) references information(i_num) ON UPDATE CASCADE
        );'''
    partnerSql='''create table if not exists partner(
        p_category varchar(10),
        p_area varchar(10),
        p_year integer,
        p_month integer,
        p_day integer,
        p_title text,
        p_content integer,
        p_num integer not null primary key autoincrement,
        p_userid varchar(20),
        foreign key (p_userid) references user(id) ON UPDATE CASCADE
        );'''
    partnerReplySql='''create table if not exists partnerReply(
        pr_year integer,
        pr_month integer,
        pr_day integer,
        pr_content text,
        pr_num integer not null primary key autoincrement,
        pr_userid varchar(20),
        pr_pnum integer,
        foreign key (pr_userid) references user(id) ON UPDATE CASCADE
        foreign key (pr_pnum) references partner(p_num) ON UPDATE CASCADE
        );'''
    serviceSql='''create table if not exists service(
        s_category varchar(10),
        s_year integer,
        s_month integer,
        s_day integer,
        s_title text,
        s_content integer,
        s_num integer not null primary key autoincrement,
        s_userid varchar(20),
        foreign key (s_userid) references user(id) ON UPDATE CASCADE
        );'''
    serviceReplySql='''create table if not exists serviceReply(
        sr_year integer,
        sr_month integer,
        sr_day integer,
        sr_content text,
        sr_num integer not null primary key autoincrement,
        sr_userid varchar(20),
        sr_snum integer,
        foreign key (sr_userid) references user(id) ON UPDATE CASCADE
        foreign key (sr_snum) references information(s_num) ON UPDATE CASCADE
        );'''
    cur.execute(localCommSql)
    cur.execute(localReplySql)
    cur.execute(infoCommSql)
    cur.execute(infoReplySql)
    cur.execute(partnerSql)
    cur.execute(partnerReplySql)
    cur.execute(serviceSql)
    cur.execute(serviceReplySql)
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
    con=sqlite3.connect("test.db")
    cur=con.cursor()
    #cur.execute('drop table bookmark')
    #con.commit()
    #즐겨찾기 테이블 추가
    #id 외래키로 가져오는 방법..?

    bookmarksql='''create table if not exists bookmark(
        b_num integer not null,
        p_year integer,
        p_month integer,
        p_day integer,
        isholiday text,
        p_time text,
        location text,
        mapx real,
        mapy real,
        weather text,
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
        b_id varchar(20) not null,
        tag text,
        man integer,
        woman integer,
        p_num10 integer,
        p_num20 integer,
        p_num30 integer,
        p_num40 integer,
        p_num50 integer,
        m1 integer,
        m2 integer,
        m3 integer,
        m4 integer,
        m5 integer,
        m6 integer,
        m7 integer,
        m8 integer,
        m9 integer,
        m10 integer,
        m11 integer,
        m12 integer,
        evening integer,
        afternoon integer,
        primary key(b_num)
        foreign key(b_id) references user(id) ON UPDATE CASCADE
    );'''

    cur.execute(bookmarksql)
    con.commit()    
   
def read_db():
    con=sqlite3.connect("test.db")
    cur=con.cursor()
    cur.execute("select * from population ")
    print(cur.fetchall())


def insert_query(data):
    ageflag = [0]*10
    where_query = "where "
    #위치 추가
    locationtemp = data['addr']
    #스트링 비었을 때
    if locationtemp :
        where_query+= "location like '%"
        where_query+= locationtemp
        where_query+= "%' and "
    
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
        where_query+='  or '
    for i in range(len(data['time'])):
        timetemp = data['time'].pop() 
        where_query+='p_time like'
        if('afternoon' == timetemp):
            where_query+=" '%12시%'"
        elif('evening' == timetemp):

            where_query+=" '%19시%'"    
        where_query+='  or '
    
    #and 제거
    where_query = where_query[:len(where_query)-5]
    where_query += " group by num"
    return where_query, ageflag

def insert_query2(ageflag) :
    #where_query2 = ",(select Max("
    where_query2 = ",(select ("
    
    agetemp2=0
    query_flag=False
    for i in range(10):
        if(ageflag[i]==1):
            where_query2+="SUM("
            if(i>=5):
                agetemp2=50
                where_query2+="wo"
            where_query2+="man"
            where_query2+=str(50-i*10+agetemp2)
            where_query2+=")+ "
            #where_query2+=", "
            query_flag=True
     #쉼표 제거
    where_query2 = where_query2[:len(where_query2)-2]
    where_query2+=")) as maxpop"
    if query_flag:
        return where_query2
    else:
        return ""

def getSearchMap(data):

    # data.sex, data.age, data.month, data.time -> 전부 리스트 타입으로 사용자가 택한 값만 들어있습니다.
    # ex) data['sex'] = [man, woman]  data.age=[0,0,0,10,40] data.month =[1,5,6]  data.time=[afternoon, evening]
    where_query,ageflag = insert_query(data)
    where_query2 = insert_query2(ageflag)
    if where_query2:
        where_query+=" order by maxpop desc;"
    wherefinal_query = 'select *'+where_query2+' from population '+where_query
    #wherefinal_query = 'select * from population '+where_query
    print(wherefinal_query)
    cur = g.db.execute(wherefinal_query)
    print(cur.fetchone())
    #부속질의문 사용 끝
    #cur = g.db.execute('select * from population where man10>100')
    
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
            'time' : request.form.getlist('time', None),
            'addr' : request.form['addr']
        }

        addr = request.form['addr']
        if addr:
            NAVERKEY  = "7f988a1d3bc4b0767fef224ef85d1743"

            params = {
                "query": addr,
                "output": "xml",
                "key": NAVERKEY,
                "encoding" : "utf-8",
                "coord" : "tm128"
            }

            queryString = urlencode(params)
            respon = urlopen("http://openapi.map.naver.com/api/geocode?" + queryString).read().decode('utf-8')
            
            soup = BeautifulSoup(respon, "html.parser")
            
            point = {
                'x' : soup.x.string,
                'y' : soup.y.string
            }


        else :
            point = {
                'x' : 307677,
                'y' : 549510
            }
        
        entries= getSearchMap(data=data);
        return render_template('map.html', data=data, entries=entries, point= point)
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
            return redirect(url_for('join'))
        
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
@app.route('/localcomm/<page>')
def localcomm(page):
    if page=="1":
        cur = g.db.execute('select w_category,w_area,w_title,w_content,w_year,w_month,w_day,w_userid, w_num from localcomm order by w_num desc')
        entries = [dict(category=row[0], area=row[1],title=row[2],content=row[3],year=row[4],month=row[5],day=row[6],userid=row[7],num=row[8]) for row in cur.fetchall()]
        print(entries)
        return render_template('localcomm.html', entries = entries, page=page)
    elif page=="2":
        cur = g.db.execute('select i_category,i_title,i_content,i_year,i_month,i_day,i_userid, i_num from information order by i_num desc')
        entries = [dict(category=row[0], title=row[1],content=row[2],year=row[3],month=row[4],day=row[5],userid=row[6],num=row[7]) for row in cur.fetchall()]
        print(entries)
        return render_template('localcomm.html', entries = entries, page=page)
    elif page=="3":
        cur = g.db.execute('select p_category,p_area,p_title,p_content,p_year,p_month,p_day,p_userid, p_num from partner order by p_num desc')
        entries = [dict(category=row[0], area=row[1],title=row[2],content=row[3],year=row[4],month=row[5],day=row[6],userid=row[7],num=row[8]) for row in cur.fetchall()]
        print(entries)
        return render_template('localcomm.html', entries = entries, page=page)
    elif page=="4":
        cur = g.db.execute('select s_category,s_title,s_content,s_year,s_month,s_day,s_userid, s_num from service order by s_num desc')
        entries = [dict(category=row[0],title=row[1],content=row[2],year=row[3],month=row[4],day=row[5],userid=row[6],num=row[7]) for row in cur.fetchall()]
        print(entries)
        return render_template('localcomm.html', entries = entries, page=page)
@app.route('/community/')
def community():
    #cur = g.db.execute('select w_category,w_area,w_title,w_content,w_year,w_month,w_day,w_userid, w_num from localcomm order by w_num desc')
    #entries = [dict(category=row[0], area=row[1],title=row[2],content=row[3],year=row[4],month=row[5],day=row[6],userid=row[7],num=row[8]) for row in cur.fetchall()]
    #print(entries)
    return redirect(url_for('localcomm',page=1))
    
@app.route('/add/<page>')
def add(page):
    return render_template('add.html',page=page)

@app.route('/adding/<page>', methods=['POST'])
def adding(page):
    now = time.localtime()
    Category = request.form['category']
    if page!="2" and page!="4":
        Area = request.form['area']
    Title = request.form['title']
    Content = request.form['content']
    Year = now.tm_year
    Month = now.tm_mon
    Day = now.tm_mday
    Writer = session['nick']
    #Id = request.form['category']
    if page=="1":
        g.db.execute('insert into localcomm (w_category,w_area,w_title,w_content,w_year,w_month,w_day,w_userid) values (?,?,?,?,?,?,?,?);',(Category,Area,Title,Content,Year,Month,Day,Writer,));
        g.db.commit()
        return redirect(url_for('localcomm',page=1))
    elif page=="2":
        g.db.execute('insert into information (i_category,i_title,i_content,i_year,i_month,i_day,i_userid) values (?,?,?,?,?,?,?);',(Category,Title,Content,Year,Month,Day,Writer,));
        g.db.commit()
        return redirect(url_for('localcomm',page=2))
    elif page=="3":
        g.db.execute('insert into partner (p_category,p_area,p_title,p_content,p_year,p_month,p_day,p_userid) values (?,?,?,?,?,?,?,?);',(Category,Area,Title,Content,Year,Month,Day,Writer,));
        g.db.commit()
        return redirect(url_for('localcomm',page=3))
    elif page=="4":
        g.db.execute('insert into service (s_category,s_title,s_content,s_year,s_month,s_day,s_userid) values (?,?,?,?,?,?,?);',(Category,Title,Content,Year,Month,Day,Writer,));
        g.db.commit()
        return redirect(url_for('localcomm',page=4))


#@app.route('/showpost/<wnum>', methods=['POST'])
#def showpost(wnum):
#    num=int(wnum);
#    cur = g.db.execute('select w_category,w_area,w_title,w_content,w_year,w_month,w_day,w_num from localcomm where w_num=num;')
#    entries2 = [dict(w_category=row[0], w_area=row[1],w_title=row[2],w_content=row[3],w_year=row[4],w_month=row[5],w_day=row[6],w_num=row[7]) for row in cur.fetchall()]
#    return render_template('showpost.html', entries2 = entries2)
@app.route('/showpost/<page>/<num>')
def showpost(page,num):
    num=int(num);
    if page=="1":
        cur = g.db.execute('select w_category,w_area,w_title,w_content,w_year,w_month,w_day,w_userid,w_num from localcomm where w_num=(?);',(num,))
        entries2 = [dict(category=row[0], area=row[1],title=row[2],content=row[3],year=row[4],month=row[5],day=row[6],userid=row[7],num=row[8]) for row in cur.fetchall()]
        cur2 = g.db.execute('select r_userid,r_content,r_year,r_month,r_day from localReply where r_wnum=(?) order by r_num desc;',(num,))
        entries3 = [dict(userid=row[0], content=row[1],year=row[2],month=row[3],day=row[4]) for row in cur2.fetchall()]
        return render_template('showpost.html', entries2 = entries2, entries3=entries3, num=num, page=page)
    elif page=="2":
        cur = g.db.execute('select i_category,i_title,i_content,i_year,i_month,i_day,i_userid,i_num from information where i_num=(?);',(num,))
        entries2 = [dict(category=row[0], title=row[1],content=row[2],year=row[3],month=row[4],day=row[5],userid=row[6],num=row[7]) for row in cur.fetchall()]
        cur2 = g.db.execute('select ir_userid,ir_content,ir_year,ir_month,ir_day from infoReply where ir_inum=(?) order by ir_num desc;',(num,))
        entries3 = [dict(userid=row[0], content=row[1],year=row[2],month=row[3],day=row[4]) for row in cur2.fetchall()]
        return render_template('showpost.html', entries2 = entries2, entries3=entries3, num=num, page=page)
    elif page=="3":
        cur = g.db.execute('select p_category,p_area,p_title,p_content,p_year,p_month,p_day,p_userid,p_num from partner where p_num=(?);',(num,))
        entries2 = [dict(category=row[0], area=row[1],title=row[2],content=row[3],year=row[4],month=row[5],day=row[6],userid=row[7],num=row[8]) for row in cur.fetchall()]
        cur2 = g.db.execute('select pr_userid,pr_content,pr_year,pr_month,pr_day from partnerReply where pr_pnum=(?) order by pr_num desc;',(num,))
        entries3 = [dict(userid=row[0], content=row[1],year=row[2],month=row[3],day=row[4]) for row in cur2.fetchall()]
        return render_template('showpost.html', entries2 = entries2, entries3=entries3, num=num, page=page)
    elif page=="4":
        cur = g.db.execute('select s_category,s_title,s_content,s_year,s_month,s_day,s_userid,s_num from service where s_num=(?);',(num,))
        entries2 = [dict(category=row[0], title=row[1],content=row[2],year=row[3],month=row[4],day=row[5],userid=row[6],num=row[7]) for row in cur.fetchall()]
        cur2 = g.db.execute('select sr_userid,sr_content,sr_year,sr_month,sr_day from serviceReply where sr_snum=(?) order by sr_num desc;',(num,))
        entries3 = [dict(userid=row[0], content=row[1],year=row[2],month=row[3],day=row[4]) for row in cur2.fetchall()]
        return render_template('showpost.html', entries2 = entries2, entries3=entries3, num=num, page=page)    

@app.route('/delpost/<page>/<num>')
def delpost(page,num):
    num=int(num)
    if page=="1":
        cur=g.db.execute('select w_userid from localcomm where w_num=(?);',(num,))
        for row in cur:
            wname=row[0]
        if (session['nick']==wname) or (session['nick']=="admin"):
            g.db.execute('delete from localcomm where w_num=(?)',(num,))
            g.db.commit()
            return redirect(url_for('localcomm',page=1))
        else:
            return render_template('no.html')
    elif page=="2":
        cur=g.db.execute('select i_userid from information where i_num=(?);',(num,))
        for row in cur:
            wname=row[0]
        if (session['nick']==wname) or (session['nick']=="admin"):
            g.db.execute('delete from information where i_num=(?)',(num,))
            g.db.commit()
            return redirect(url_for('localcomm',page=2))
        else:
            return render_template('no.html')
    elif page=="3":
        cur=g.db.execute('select p_userid from partner where p_num=(?);',(num,))
        for row in cur:
            wname=row[0]
        if (session['nick']==wname) or (session['nick']=="admin"):
            g.db.execute('delete from partner where p_num=(?)',(num,))
            g.db.commit()
            return redirect(url_for('localcomm',page=3))
        else:
            return render_template('no.html')
    elif page=="4":
        cur=g.db.execute('select s_userid from service where s_num=(?);',(num,))
        for row in cur:
            wname=row[0]
        if (session['nick']==wname) or (session['nick']=="admin"):
            g.db.execute('delete from service where s_num=(?)',(num,))
            g.db.commit()
            return redirect(url_for('localcomm',page=4))
        else:
            return render_template('no.html')

@app.route('/addreply/<page>/<wnum>', methods=['POST'])
def addreply(page,wnum):
    num=int(wnum)
    now = time.localtime()
    Writer = session['nick']
    Year = now.tm_year
    Month = now.tm_mon
    Day = now.tm_mday
    Content = request.form['content']
    if page=="1":
        g.db.execute('insert into localReply (r_userid,r_content,r_year,r_month,r_day,r_wnum) values (?,?,?,?,?,?);',(Writer,Content,Year,Month,Day,num,));
        g.db.commit()
        return redirect(url_for('showpost',page=1,num=num))
    elif page=="2":
        g.db.execute('insert into infoReply (ir_userid,ir_content,ir_year,ir_month,ir_day,ir_inum) values (?,?,?,?,?,?);',(Writer,Content,Year,Month,Day,num,));
        g.db.commit() 
        return redirect(url_for('showpost',page=2,num=num))
    elif page=="3":
        g.db.execute('insert into partnerReply (pr_userid,pr_content,pr_year,pr_month,pr_day,pr_pnum) values (?,?,?,?,?,?);',(Writer,Content,Year,Month,Day,num,));
        g.db.commit()
        return redirect(url_for('showpost',page=3,num=num))
    elif page=="4":
        g.db.execute('insert into serviceReply (sr_userid,sr_content,sr_year,sr_month,sr_day,sr_snum) values (?,?,?,?,?,?);',(Writer,Content,Year,Month,Day,num,));
        g.db.commit()
        return redirect(url_for('showpost',page=4,num=num))    
#######end local community part #######





#######start bookmark part #######

@app.route('/bookmark')
def getBookmarkList():
    # session['id'] 를 이용하여  북마크 전체 결과를 entries 에 저장
    #cur = g.db.execute('select * from bookmark where b_id = "A"')
    cur = g.db.execute('select * from bookmark where b_id = '+session['nick'])
    entries = [dict(b_num = row[0], year=row[1], month=row[2],  day=row[3],  time=row[5], isholiday=row[4],  
        location=row[6], mapx=row[7], mapy=row[8], weather=row[9], 
        man10=row[10], man20=row[11], man30=row[12], man40=row[13], man50=row[14],
        woman10=row[15], woman20=row[16], woman30=row[17], woman40=row[18], woman50=row[19],
        id=row[20], tag=row[21], man =row[22], woman = row[23], p_num10 = row[24],
        p_num20 = row[25], p_num30 = row[26], p_num40 = row[27], p_num50 = row[28], m1= row[29],
        m2 = row[30], m3 = row[31], m4 = row[32], m5 = row[33], m6 = row[34],
        m7 = row[35], m8 = row[36], m9 = row[37], m10 = row[38], m11 = row[39],
        m12 = row[40],evening = row[41], afternoon = row[42])for row in cur.fetchall()]
    return render_template('bookmark.html', entries=entries)

@app.route('/bookmark/', methods=['POST'])
def addBookmark():

    if request.method == 'POST':
        data={
            'sex' :request.form.getlist('sex', None),
            'age' : request.form.getlist('age[]', None),
            'month' : request.form.getlist('month', None),
            'time' : request.form.getlist('time', None),
            'addr' : request.form['addr']
        }
    # data 를 이용하여 bookmark table에 저장하고, 사용자의 전체 북마크 리스트를 entries에 반환
    #입력할 최고의 수치
    where_query = ""
    where_qeury2 = ""
    where_query,ageflag = insert_query(data)
    where_query2 = insert_query2(ageflag)
    if where_query2 :
        where_query+= " order by maxpop desc;"

    finalwhere_query =  'select *'+where_query2+' from population '+where_query
    cur = g.db.execute(finalwhere_query)
    m_row = cur.fetchone()
    print(m_row)

    #여기 수정 / 테이블 수정
    addbookmark_sql = '''insert into bookmark(
    p_year,p_month,p_day,isholiday,p_time,
    location,mapx,mapy,weather,man10,
    man20,man30,man40,man50,woman10,
    woman20,woman30,woman40,woman50,b_id,
    tag,man,woman,p_num10,p_num20,
    p_num30,p_num40,p_num50,m1,m2,
    m3,m4,m5,m6,m7,
    m8,m9,m10,m11,m12,
    evening,afternoon) values(
    ?,?,?,?,?,
    ?,?,?,?,?,
    ?,?,?,?,?,
    ?,?,?,?,?,
    ?,?,?,?,?,
    ?,?,?,?,?,
    ?,?,?,?,?,
    ?,?,?,?,?,
    ?,?)'''

    
    #bool입력할 것들
    #성별
    #user = session['id']
    user = "A"
    s1 = False
    s2 = False
    while data['sex']:
        s_temp = data['sex'].pop()
        if(s_temp=='man'):
            s1 = True
        elif(s_temp=='woman'):
            s2 = True

    p_count=0 
    p_num5=0
    p_num4=0
    p_num3=0
    p_num2=0
    p_num1=0
    while data['age']:
        p_temp = data['age'].pop()
        if(p_count==0):
            p_num5 = p_temp
        elif(p_count==1):
            p_num4 = p_temp
        elif(p_count==2):
            p_num3 = p_temp
        elif(p_count==3):
            p_num2 = p_temp
        elif(p_count==4):
            p_num1 = p_temp
        p_count= p_count+1
    
    m1 = False
    m2 = False
    m3 = False
    m4 = False
    m5 = False
    m6 = False
    m7 = False
    m8 = False
    m9 = False
    m10 = False
    m11 = False
    m12 = False

    while data['month']:
        m_temp = data['month'].pop()
        if(m_temp == 1):
            m1 = True
        elif(m_temp==2):
            m2 = True
        elif(m_temp==3):
            m3 = True
        elif(m_temp==4):
            m4 = True
        elif(m_temp==5):
            m5 = True
        elif(m_temp==6):
            m6 = True
        elif(m_temp==7):
            m7 = True
        elif(m_temp==8):
            m8 = True
        elif(m_temp==9):
            m9 = True
        elif(m_temp==10):
            m10 = True
        elif(m_temp==11):
            m11 = True
        elif(m_temp==12):
            m12 = True
    
    d1 = False
    d2 = False
    while data['time']:
        d_temp = data['time'].pop()
        if(d_temp == 'evening'):
            d1 = True
        elif(d_temp == 'afternoon'):
            d2 = True
    
    my_tag = " "
    if data['addr'] :
        my_tag = data['addr']

    #여기서 값이 잘못 들어 간것
    g.db.execute(addbookmark_sql,(m_row[1],m_row[2],m_row[3],m_row[4],m_row[5],m_row[6],m_row[7],m_row[8],m_row[9],m_row[10],m_row[11],m_row[12],m_row[13],m_row[14],m_row[15],m_row[16],m_row[17],m_row[18],m_row[19],user,my_tag,s1,s2,p_num1,p_num2,p_num3,p_num4,p_num5,m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,m12,d1,d2))
    g.db.commit()
        #19개
        #
        #entry 
        #id라고 써도 되나
    cur = g.db.execute('select * from bookmark')
    testrow = cur.fetchone()
    entries = [dict(b_num = row[0], year=row[1], month=row[2],  day=row[3],  time=row[5], isholiday=row[4],  
        location=row[6], mapx=row[7], mapy=row[8], weather=row[9], 
        man10=row[10], man20=row[11], man30=row[12], man40=row[13], man50=row[14],
        woman10=row[15], woman20=row[16], woman30=row[17], woman40=row[18], woman50=row[19],
        id=row[20], tag=row[21], man =row[22], woman = row[23], p_num10 = row[24],
        p_num20 = row[25], p_num30 = row[26], p_num40 = row[27], p_num50 = row[28], m1= row[29],
        m2 = row[30], m3 = row[31], m4 = row[32], m5 = row[33], m6 = row[34],
        m7 = row[35], m8 = row[36], m9 = row[37], m10 = row[38], m11 = row[39],
        m12 = row[40],evening = row[41], afternoon = row[42])for row in cur.fetchall()]
    return render_template('bookmark.html', entries=entries)

@app.route('/map/<bnum>', methods=['GET','POST'])
def clickBookmark(bnum):
    # bnum 을 이용한 map검색 결과를 entries에 저장 
    
    cur = g.db.execute('select * from bookmark where b_num =(?)',(bnum,))
    mys = [dict(b_num = row[0], year=row[1], month=row[2],  day=row[3],  time=row[5], isholiday=row[4],  
        location=row[6], mapx=row[7], mapy=row[8], weather=row[9], 
        man10=row[10], man20=row[11], man30=row[12], man40=row[13], man50=row[14],
        woman10=row[15], woman20=row[16], woman30=row[17], woman40=row[18], woman50=row[19],
        id=row[20], tag=row[21], man =row[22], woman = row[23], p_num10 = row[24],
        p_num20 = row[25], p_num30 = row[26], p_num40 = row[27], p_num50 = row[28], m1= row[29],
        m2 = row[30], m3 = row[31], m4 = row[32], m5 = row[33], m6 = row[34],
        m7 = row[35], m8 = row[36], m9 = row[37], m10 = row[38], m11 = row[39],
        m12 = row[40],evening = row[41], afternoon = row[42])for row in cur.fetchall()]
    
    my_query = "select * from population where "
    

    #tag
    for my in  mys:
        print(my['tag'])
        if not my['tag'] == " ":
            my_query += "tag = '"
            my_query += my['tag']
            my_query += "' and "
    
        #boy
        agetemp = 0
        if my['man'] == 1:
            agetemp = my['p_num50']
            my_query += 'man50>'
            my_query += agetemp    
            my_query += ' and ' 
            
            agetemp = my['p_num40']
            my_query += 'man40>'
            my_query += agetemp    
            my_query += ' and ' 
            
            agetemp = my['p_num30']
            my_query += 'man30>'
            my_query += agetemp    
            my_query += ' and ' 
            
            agetemp = my['p_num20']
            my_query += 'man20>'
            my_query += agetemp    
            my_query += ' and ' 
            
            agetemp = my['p_num10']
            my_query += 'man10>'
            my_query += agetemp    
            my_query += ' and ' 
            
        if my['woman'] == 1:
            agetemp = my['p_num50']
            my_query += 'woman50>'
            my_query += agetemp    
            my_query += ' and ' 
            
            agetemp = my['p_num40']
            my_query += 'woman40>'
            my_query += agetemp    
            my_query += ' and ' 
            
            agetemp = my['p_num30']
            my_query += 'woman30>'
            my_query += agetemp    
            my_query += ' and ' 
            
            agetemp = my['p_num20']
            my_query += 'woman20>'
            my_query += agetemp    
            my_query += ' and ' 
            
            agetemp = my['p_num10']
            my_query += 'woman10>'
            my_query += agetemp    
            my_query += ' and ' 
            
        if(my['m1']==1):
            my_query += 'p_month = 1  or '
        if(my['m2']==1):
            my_query += 'p_month = 2  or '
        if(my['m3']==1):
            my_query += 'p_month = 3  or '
        if(my['m4']==1):
            my_query += 'p_month = 4  or '
        if(my['m5']==1):
            my_query += 'p_month = 5  or '
        if(my['m6']==1):
            my_query += 'p_month = 6  or '
        if(my['m7']==1):
            my_query += 'p_month = 7  or '
        if(my['m8']==1):
            my_query += 'p_month = 8  or '
        if(my['m9']==1):
            my_query += 'p_month = 9  or '
        if(my['m10']==1):
            my_query += 'p_month = 10  or '
        if(my['m11']==1):
            my_query += 'p_month = 11  or '
        if(my['m12']==1):
            my_query += 'p_month = 12  or '
    
        if(my['evening']==1):
            my_query += "p_time like '%12시%'  or "
        if(my['afternoon']==1):
            my_query += "p_time like '%19시%'  or "
    
    my_query = my_query[:len(my_query)-4]
    cur = g.db.execute(my_query)
    
    entries = [dict(b_num = row[0], year=row[1], month=row[2],  day=row[3],  time=row[5], isholiday=row[4],  
        location=row[6], mapx=row[7], mapy=row[8], weather=row[9], 
        man10=row[10], man20=row[11], man30=row[12], man40=row[13], man50=row[14],
        woman10=row[15], woman20=row[16], woman30=row[17], woman40=row[18], woman50=row[19]
        )for row in cur.fetchall()]
    #point #data
    return render_template('map.html',entries=entries)

#######end bookmark part #######





if __name__ == '__main__':
    #init_db()
    init_userdb()
    init_bookmark()
    #connect_db()
    init_commdb()
    
    app.debug=True
    app.run(port=5000)

