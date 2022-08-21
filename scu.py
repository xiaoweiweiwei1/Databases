from asyncio.windows_events import NULL
from gettext import NullTranslations
import pymysql
import easygui as t
import prettytable as pt
import sys


message = ['数据库名','密码']
s =t.multenterbox('输入信息:','力学软件班级选课情况及成绩',message)

try:
    conn=pymysql.Connect(

    host='localhost',

    port=3306,

    user='root',

    passwd=s[1],

    db=s[0],
#ddl_mysql
    charset='utf8'

    )
    t.msgbox(msg='连接数据库成功', title='success', ok_button='ok')

except:
    t.msgbox(msg='连接数据库失败', title='fail', ok_button='ok')

cursor=conn.cursor()

while True:
    a = t.buttonbox(msg = "力学软件班级选课情况及成绩",title = "力学软件班级选课情况及成绩",choices = ("注册","登录"))
    if a=="注册":
        message = ['编号','密码']
        s =t.multenterbox('输入信息:','力学软件班级选课情况及成绩',message)
        try:
            affected_rows = cursor.execute('insert into psw values (%s, %s)',(s[0],s[1]) )
            if s[0]=='' or s[1]=='':
                         t.msgbox(msg='输入非空！', title='fail', ok_button='ok')
            if affected_rows == 1:
                    t.msgbox(msg='注册成功', title='success', ok_button='ok')
                    conn.commit()
        except pymysql.MySQLError:
                    conn.rollback()
                    t.msgbox(msg='注册失败', title='fail', ok_button='ok')

    else:
        message = ['编号','密码']
        s =t.multpasswordbox('输入信息：','力学软件班级选课情况及成绩',message)
        cursor.execute('select * from psw where ID=%s',s[0] )
        c=cursor.fetchone()
        if c[1]==s[1]:
              t.msgbox(msg='登录成功', title='success', ok_button='ok')
        

              while True:
                b = t.buttonbox(msg = "                            选择功能:",title = "力学软件班级选课情况及成绩",choices = ("输入学生信息","显示学生信息","删除学生信息","插入课程","显示课程列表","删除课程","增加一位同学的选课","删除一位同学的选课","显示一位同学在某学期的课表","显示一位同学的总学分和GPA","退出"))
                
                if b=="显示学生信息":
                         cursor.execute('select ID,student_name from student')
                         rr=cursor.fetchall()
                         tb = pt.PrettyTable( ["学号","姓名"])
                         for row in rr:
                          tb.add_row([row[0],row[1]] )
                         t.msgbox(msg=tb, title='success', ok_button='ok')
                         if t.ccbox("回到功能页？","choose"):
                             pass           
                         else:
                             sys.exit(0)    

                if b=="显示课程列表":
                         cursor.execute('select course_id,course_name,lesson_id,course_year,semester,teacher,credits,p_name,exam,department,b_name,room_no,days,start_time,end_time\
                         from lesson natural join course natural join timeno natural join proper natural join build ')
                         rr=cursor.fetchall()
                         tb = pt.PrettyTable( ["课程号","课程名","课序号","学年","学期","教师","学分","属性","考察方式","学院","教学楼","教室","星期","开始时间","结束时间"])
                         for row in rr:
                          tb.add_row([row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14]] )
                         t.msgbox(msg=tb, title='success', ok_button='ok')
                         if t.ccbox("回到功能页？","choose"):
                             pass           
                         else:
                             sys.exit(0)  

                if b=="退出":
                    sys.exit(0)  

                if b=="输入学生信息":
                        message = ['学号(最多10位)','姓名']
                        s =t.multenterbox('输入信息:','力学软件班级选课情况及成绩',message)
                        if s[0]=='' or s[1]=='':
                         t.msgbox(msg='输入非空！', title='fail', ok_button='ok')
                         if t.ccbox("回到功能页？","choose"):
                             pass           
                         else:
                             sys.exit(0)    
                        else:
                            try:
                                affected_rows = cursor.execute('insert into student(ID,student_name) values (%s, %s)',(s[0],s[1]) )
                                if affected_rows == 1:
                                        t.msgbox(msg='输入成功', title='success', ok_button='ok')
                                        conn.commit()
                            except pymysql.MySQLError:
                                        conn.rollback()
                                        t.msgbox(msg='输入失败', title='fail', ok_button='ok')
                    
                            if t.ccbox("回到功能页？","choose"):
                             pass           
                            else:
                             sys.exit(0)   

                if b=="插入课程":
                    message = ['课程号(最多10位)','课程名','学年','学期（输入春/秋）','课序号（最多10位）','老师','学分','属性号（输入1~3）','考察方式（输入考试/考察）','学院','教学楼号（输入1~9）','教室','星期(中文输入周几)','时段号（输入1~9）']
                    tb1 = pt.PrettyTable( ["属性号", "属性"])
                    tb1.add_row(["1","必修"])
                    tb1.add_row(["2","选修"])
                    tb1.add_row(["3","任选"])
                    tb2 = pt.PrettyTable( ["教学楼号", "教学楼"])
                    tb2.add_row(["1","综合楼"])
                    tb2.add_row(["2","一教A"])
                    tb2.add_row(["3","一教B"])
                    tb2.add_row(["4","一教C"])
                    tb2.add_row(["5","一教D"])
                    tb2.add_row(["6","建环楼"])
                    tb2.add_row(["7","体育场"])
                    tb2.add_row(["8","二基楼"])
                    tb2.add_row(["9","文科楼"])
                    tb3 = pt.PrettyTable( ["时段号", "时段"])
                    tb3.add_row(["1","8:15~9:55"])
                    tb3.add_row(["2","8:15~11:00"])
                    tb3.add_row(["3","8:15~11:55"])
                    tb3.add_row(["4","10:15~11:55"])
                    tb3.add_row(["5","13:50~15:30"])
                    tb3.add_row(["6","13:50~16:25"])
                    tb3.add_row(["7","16:45~18:25"])
                    tb3.add_row(["8","19:20~21:00"])
                    tb3.add_row(["9","19:20~21:55"])
                    t.msgbox(msg=tb1, title='', ok_button='ok')
                    t.msgbox(msg=tb2, title='', ok_button='ok')
                    t.msgbox(msg=tb3, title='', ok_button='ok')
                    
                    s =t.multenterbox('输入信息:\n','力学软件班级选课情况及成绩',message)       
                    if s[0]=='' or s[1]=='' or s[2]=='' or s[3]=='' or s[4]==''or s[5]==''or s[6]==''or s[7]==''or s[8]==''or s[9]==''or s[10]==''or s[12]=='':
                         t.msgbox(msg='除了教室、时段，其余输入需非空！', title='fail', ok_button='ok')
                         if t.ccbox("回到功能页？","choose"):
                             pass           
                         else:
                             sys.exit(0)    

                    else:
                            try:
                                affected_rows = cursor.execute('insert into course values (%s, %s, %s, %s, %s, %s, %s, %s)',(s[0],s[1],s[2],s[3],s[6],s[7],s[8],s[9]) )
                                if affected_rows == 1:
                                        conn.commit()
                                        t.msgbox(msg='course表插入成功！', title='success', ok_button='ok')
                            except pymysql.MySQLError:
                                        conn.rollback()
                                        t.msgbox(msg='输入失败', title='fail', ok_button='ok')
                            try:
                                affected_rows = cursor.execute('insert into lesson values (%s, %s, %s, %s, %s, %s, %s, %s, %s)',(s[0],s[2],s[3],s[4],s[5],s[12],s[13],s[10],s[11]) )
                                if affected_rows == 1:
                                        conn.commit()
                                        t.msgbox(msg='lesson表插入成功！', title='success', ok_button='ok')
                            except pymysql.MySQLError:
                                        conn.rollback()
                                        t.msgbox(msg='输入失败', title='fail', ok_button='ok')
                           
                            if t.ccbox("回到功能页？","choose"):
                             pass           
                            else:
                             sys.exit(0)    

                if b=="删除课程":    
                    message = ['课程号(最多10位)','学年','学期（输入春/秋）']
                    s =t.multenterbox('输入信息:\n','力学软件班级选课情况及成绩',message) 
                    if s[0]=='' or s[1]=='' or s[2]=='' :
                         t.msgbox(msg='输入需非空！', title='fail', ok_button='ok')
                         if t.ccbox("回到功能页？","choose"):
                             pass           
                         else:
                             sys.exit(0) 
                    else:
                            try:
                                affected_rows = cursor.execute('delete from course where (course_id,semester,course_year)=(%s, %s, %s)',(s[0],s[2],s[1]) )
                                if affected_rows == 1:
                                        conn.commit()
                                        t.msgbox(msg='删除成功！', title='success', ok_button='ok')
                            except pymysql.MySQLError:
                                        conn.rollback()
                                        t.msgbox(msg='删除失败', title='fail', ok_button='ok')   

                            if t.ccbox("回到功能页？","choose"):
                             pass           
                            else:
                             sys.exit(0)     
                                  
                if b=="删除学生信息":    
                    message = ['学号(最多10位)']
                    s =t.multenterbox('输入信息:\n','力学软件班级选课情况及成绩',message) 
                    if s[0]=='':
                         t.msgbox(msg='输入需非空！', title='fail', ok_button='ok')
                         if t.ccbox("回到功能页？","choose"):
                             pass           
                         else:
                             sys.exit(0) 
                    else:
                            try:
                                affected_rows = cursor.execute('delete from student where ID=%s',s[0] )
                                if affected_rows == 1:
                                        conn.commit()
                                        t.msgbox(msg='删除成功！', title='success', ok_button='ok')
                            except pymysql.MySQLError:
                                        conn.rollback()
                                        t.msgbox(msg='删除失败', title='fail', ok_button='ok')   

                            if t.ccbox("回到功能页？","choose"):
                             pass           
                            else:
                             sys.exit(0)           
                 
                if b=="显示一位同学在某学期的课表":
                     message = ['学号(最多10位)','学年','学期（输入春/秋）']
                     s =t.multenterbox('输入信息:\n','力学软件班级选课情况及成绩',message) 
                     if s[0]=='' or s[1]=='' or s[2]=='' :
                         t.msgbox(msg='输入需非空！', title='fail', ok_button='ok')
                         if t.ccbox("回到功能页？","choose"):
                             pass           
                         else:
                             sys.exit(0) 
                     else:
                         cursor.execute('select course_id,course_name,lesson_id,teacher,credits,p_name,exam,department,b_name,room_no,days,start_time,end_time\
                         from takes natural join course natural join lesson natural join timeno natural join proper natural join build where (ID,course_year,semester)=(%s,%s,%s)',\
                          (s[0],s[1],s[2]))
                         rr=cursor.fetchall()
                         tb = pt.PrettyTable( ["课程号", "课程名","课序号","教师","学分","属性","考察方式","学院","教学楼","教室","星期","开始时间","结束时间"])
                         for row in rr:
                          tb.add_row([row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12]] )
                         t.msgbox(msg=tb, title='success', ok_button='ok')
                         if t.ccbox("回到功能页？","choose"):
                             pass           
                         else:
                             sys.exit(0)  

                     
                if b=="显示一位同学的总学分和GPA":
                    message = ['学号(最多10位)']
                    s =t.multenterbox('输入信息:\n','力学软件班级选课情况及成绩',message) 
                    if s[0]=='' :
                         t.msgbox(msg='输入需非空！', title='fail', ok_button='ok')
                         if t.ccbox("回到功能页？","choose"):
                             pass           
                         else:
                             sys.exit(0) 
                    else:
                         cursor.execute('select student_name,tot_GPA,tot_credits from student where ID=%s',s[0])
                         rr=cursor.fetchall()
                         tb = pt.PrettyTable( ["姓名", "平均GPA","总学分"])
                         for row in rr:
                          tb.add_row([row[0],row[1],row[2]] )
                         t.msgbox(msg=tb, title='success', ok_button='ok')
                         if t.ccbox("回到功能页？","choose"):
                             pass           
                         else:
                             sys.exit(0)  

                if b=="增加一位同学的选课":
                    message = ['学号(最多10位)','课程号(最多10位)','学年','学期(输入春/秋)','课序号(最多10位)','GPA(0.0~4.0,0.0指没有分数或不及格)']
                    s =t.multenterbox('输入信息:\n','力学软件班级选课情况及成绩',message) 
                    if s[0]==''or s[1]=='' or s[2]==''or s[3]==''or s[4]==''or s[5]=='':
                         t.msgbox(msg='输入需非空！', title='fail', ok_button='ok')
                         if t.ccbox("回到功能页？","choose"):
                             pass           
                         else:
                             sys.exit(0) 
                    else:
                         try:
                                affected_rows = cursor.execute('insert into takes(ID, course_year,semester,course_id,lesson_id,GPA) values(%s,%s,%s,%s,%s,%s)',(s[0],s[2],s[3],s[1],s[4],s[5]))
                                if affected_rows == 1:
                                        conn.commit()
                                        t.msgbox(msg='takes表插入成功！', title='success', ok_button='ok')
                         except pymysql.MySQLError:
                                        conn.rollback()
                                        t.msgbox(msg='插入失败', title='fail', ok_button='ok')
                         if t.ccbox("回到功能页？","choose"):
                             pass           
                         else:
                             sys.exit(0)


                if b=="删除一位同学的选课":
                    message = ['学号(最多10位)','课程号(最多10位)','学年','学期(输入春/秋)']
                    s =t.multenterbox('输入信息:\n','力学软件班级选课情况及成绩',message) 
                    if s[0]==''or s[1]=='' or s[2]==''or s[3]=='':
                         t.msgbox(msg='输入需非空！', title='fail', ok_button='ok')
                         if t.ccbox("回到功能页？","choose"):
                             pass           
                         else:
                             sys.exit(0) 
                    else:
                         try:
                                affected_rows = cursor.execute('delete from takes where(ID, course_year,semester,course_id) =(%s,%s,%s,%s)',(s[0],s[2],s[3],s[1]))
                                if affected_rows == 1:
                                        conn.commit()
                                        t.msgbox(msg='删除成功！', title='success', ok_button='ok')
                         except pymysql.MySQLError:
                                        conn.rollback()
                                        t.msgbox(msg='删除失败', title='fail', ok_button='ok')
                         if t.ccbox("回到功能页？","choose"):
                             pass           
                         else:
                             sys.exit(0)

                                
                


        else:
         t.msgbox(msg='登录失败', title='fail', ok_button='ok')














