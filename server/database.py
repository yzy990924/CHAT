import socket
import threading
import sqlite3

dbfile = "chatplat.db"
#建一个数据库
def create_sql():
    sql = sqlite3.connect(dbfile)
    sql.execute("""create table if not exists
        %s(
        %s integer primary key autoincrement,
        %s varchar(128),
        %s varchar(128),
        %s integer
        )"""
        % ('user',
            'id',
            'name',
            'passworld',
            'room_id'
           ))
    sql.execute("""create table if not exists
        %s(
        %s integer primary key autoincrement,
        %s varchar(128),
        %s varchar(128),
        %s integer
        )"""
        % ('chatroom',
            'room_id',
            'room_name',
            'room_note',
            'id'
           ))
    sql.close()
 
# user表增加数据
def add_user_data(input_name,input_passworld):
    sql = sqlite3.connect(dbfile)
    sql.execute("insert into user(name,passworld) values(?,?)",
                (input_name,input_passworld))
    sql.commit()
    print("用户添加成功")
    sql.close()

#chatroom增加数据
def add_chatroon_data(room_name,room_note):
    sql = sqlite3.connect(dbfile)
    sql.execute("insert into chatroom(room_name,room_note) values(?,?)",
                (room_name,room_note))
    sql.commit()
    print("聊天室添加成功")
    sql.close()

#用户加入已存在的聊天室
def join_chatroom():

#按照用户名查找密码
def search_password(input_name):
	try:
        sql = sqlite3.connect(dbfile)
        cur = sql.cursor()
        cur.execute("select passworld from user where name = input_name")
        print (cur.fetchall())
    except sqlite3.Error as e:
        print (e)
    sql.close()

#当用户注销时, 删除此用户记录
def delete(input_name):
	try:
        sql = sqlite3.connect(dbfile)
 		sql.execute("DELETE FROM user WHERE name = input_name" % id)
        sql.commit()
        print ('用户注销成功')
    except sqlite3.Error as e:
        print (e)
    sql.close()


