use ddl_mysql;


drop table if exists takes;
drop table if exists lesson;
drop table if exists course;
drop table if exists student;
drop table if exists id;
drop table if exists timeno;
drop table if exists proper;
drop table if exists psw;
drop table if exists build;


create table psw
	(ID		  varchar(10) not null, 
	psword    varchar(10) not null,
	 primary key (ID)
	);
    
create table build
	(b_no			varchar(10) not null, 
	b_name    nvarchar(6) check(b_name in ('综合楼','一教A','一教B','一教C','一教D','建环楼','体育场','二基楼','文科楼')),
	 primary key (b_no)
	);
  
  insert into build values('1','综合楼');
  insert into build values('2','一教A');
  insert into build values('3','一教B');
  insert into build values('4','一教C');
  insert into build values('5','一教D');
  insert into build values('6','建环楼');
  insert into build values('7','体育场');
  insert into build values('8','二基楼');
  insert into build values('9','文科楼');
  
create table proper
	(p_no			varchar(5) not null, 
	p_name nvarchar(4) check (p_name in ('必修','选修','任选')),
	 primary key (p_no)
	);

insert into proper values('1','必修');
insert into proper values('2','选修');
insert into proper values('3','任选');

create table student
	(ID			varchar(10) not null, 
	 student_name  nvarchar(8) not null,
     tot_GPA varchar(3) default '0.0',
     tot_credits int default 0,
	 primary key (ID)
	);

create table course
	(course_id		varchar(10) not null,
	 course_name	nvarchar(50) not null, 
	 course_year  varchar(4) not null, 
	 semester		nvarchar(2) check (semester in ('春','秋')),
     credits varchar(2) not null,
     p_no varchar(10) ,
     exam nvarchar(4) check(exam in ('考试','考查')), 
     department nvarchar(50) not null,
	 primary key (course_id,semester,course_year),
     foreign key(p_no) references proper(p_no)
     on delete cascade
        on update cascade
	);
    
create table timeno
    (time_no varchar(10) ,
    start_time time,
    end_time time,
    primary key(time_no));
    
    insert into timeno values('1','8:15','9:55');
    insert into timeno values('2','8:15','11:00');
    insert into timeno values('3','8:15','11:55');
    insert into timeno values('4','10:15','11:55');
    insert into timeno values('5','13:50','15:30');
    insert into timeno values('6','13:50','16:25');
    insert into timeno values('7','16:45','18:25');
    insert into timeno values('8','19:20','21:00');
    insert into timeno values('9','19:20','21:55');


create table lesson
	(course_id		varchar(10),
     course_year  varchar(4) not null, 
	 semester		nvarchar(2),
     lesson_id		varchar(10) not null,
	 teacher		nvarchar(8) not null,
	 days nvarchar(4) check(days in('周一','周二','周三','周四','周五','周六','周日')),
	 time_no varchar(10) ,
	b_no		varchar(10) ,
	 room_no	varchar(10) ,
	 primary key (course_id,course_year,semester,lesson_id),
	 foreign key (course_id,semester,course_year) references course(course_id,semester,course_year)
		on delete cascade
        on update cascade,
        foreign key (time_no) references timeno(time_no)
		on delete cascade
        on update cascade,
        foreign key (b_no) references build(b_no)
		on delete cascade
        on update cascade
	);

create table takes
	(ID			varchar(10) not null, 
	 course_year  varchar(4) not null,   
     semester		nvarchar(2) ,
     course_id		varchar(10) not null,
     lesson_id		varchar(10) not null,
     GPA varchar(3) default '0.0',
	 primary key (ID, course_year,semester,course_id),
     foreign key(ID) references student(ID),
     foreign key(course_id,semester,course_year) references course(course_id,semester,course_year)
     on delete cascade
        on update cascade,
        foreign key(course_id,course_year,semester,lesson_id) references lesson(course_id,course_year,semester,lesson_id)
     on delete cascade
        on update cascade
	);
    
   
    
    DELIMITER $
    create trigger totalcredits1 after insert on takes
    for each row
    begin 
    update student
    set tot_credits=tot_credits+(select credits from course where (new.course_id,new.course_year,new.semester)=(course.course_id,course.course_year,course.semester))
    where new.GPA>0 and ID=new.ID;/*自动将char转换为数值*/
    end $
    DELIMITER ;
    
     DELIMITER $
    create trigger totalcredits2 after update on takes
    for each row
    begin 
    update student
    set tot_credits=tot_credits+(select credits from course where (new.course_id,new.course_year,new.semester)=(course.course_id,course.course_year,course.semester))
    where new.GPA>0 and ID=new.ID;
    end $
    DELIMITER ;
    
 DELIMITER $
    create trigger totalcredits3 after delete on takes
    for each row
    begin 
    update student
    set tot_credits=tot_credits-(select credits from course where (old.course_id,old.course_year,old.semester)=(course.course_id,course.course_year,course.semester))
    where old.GPA>0 and ID=old.ID;
    end $
    DELIMITER ;
    
    drop view if exists totGPA;
    
    create view totGPA(ID,t,credits) as
    select ID,takes.GPA*course.credits,credits from takes natural join course;/*自动将char转换为数值*/ 
    
     DELIMITER $
    create trigger totalGPA1 after insert on takes
    for each row
    begin
    update student
    set tot_GPA=(select sum(distinct t) from totGPA where ID=new.ID)/(select sum(distinct credits) from totGPA where ID=new.ID)
    where new.GPA>0 and ID=new.ID;
    end $
    DELIMITER ;
    
   DELIMITER $
    create trigger totalGPA2 after update on takes
    for each row
    begin
    update student
    set tot_GPA=(select sum(distinct t) from totGPA where ID=new.ID)/(select sum(distinct credits) from totGPA where ID=new.ID)
    where new.GPA>0 and ID=new.ID;
    end $
    DELIMITER ;
    
     DELIMITER $
    create trigger totalGPA3 after delete on takes
    for each row
    begin
    update student
    set tot_GPA=(select sum(distinct t) from totGPA where ID=old.ID)/(select sum(distinct credits) from totGPA where ID=old.ID)
    where old.GPA>0 and ID=old.ID;
    end $
    DELIMITER ;

insert into psw values('1','123');


