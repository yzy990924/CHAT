#coding:utf-8
import socket
import threading
import sqlite3
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
dbfile = "Chat.db"

def create_sql():
    sql = sqlite3.connect(dbfile)
    sql.execute("""create table if not exists
        %s(
        %s integer primary key autoincrement,
        %s varchar(128),
        %s varchar(128)
        )"""
        % ('user',
            'id',
            'name',
            'passwd'
           ))
    sql.execute("""create table if not exists
        %s(
        %s varchar(128),
        %s varchar(128)
        )"""
        % ('userTime',
            'name',
            'time'
           ))
    sql.close()
 
def search_all_username():
    sql = sqlite3.connect(dbfile)
    try:
        sql = sqlite3.connect(dbfile)
        cur = sql.cursor()
        cur.execute("select name from user")
        return cur.fetchall()
    except sqlite3.Error as e:
        print e
    sql.close()

def search_passwd(input_name):
    input_name = input_name
    try:
        sql = sqlite3.connect(dbfile)
        cur = sql.cursor()
        cur.execute("select passwd from user where name  = (%s) "%(input_name))
        return cur.fetchall()[0][0]
    except sqlite3.Error as e:
        print e
    sql.close()

def add_user(input_name,input_password):
    print input_name
    sql = sqlite3.connect(dbfile)
    sql.execute("insert into user(name,passwd) values(?,?)",
                (input_name,input_password))
    sql.commit()
    sql.close()

def add_time(input_name,input_time):
    sql = sqlite3.connect(dbfile)
    try:
        cur = sql.cursor()
        cur.execute("select time from userTime where name = (%s) "%(input_name))
        print cur.fetchall()
        if cur.fetchall() != []:
            time = cur.fetchall()[0][0]
            sql.execute("update userTime set time = (?) where name = input_name",
                (input_time+time))
            sql.commit()
        else :
            sql.execute("insert into userTime(name,time) values(?,?)",
                (input_name,input_time))
            sql.commit()

    except sqlite3.Error as e:
        print e
    sql.close()

# def add_chatroon_data(room_name,room_note):
#     sql = sqlite3.connect(dbfile)
#     sql.execute("insert into chatroom(room_name,room_note) values(?,?)",
#                 (room_name,room_note))
#     sql.commit()

#     sql.close()




# def search_password(input_name):
# 	try:
#         sql = sqlite3.connect(dbfile)
#         cur = sql.cursor()
#         cur.execute("select passworld from user where name = input_name")
#         print (cur.fetchall())
#     except sqlite3.Error as e:
#         print (e)
#     sql.close()


def delete(): 

    try:
        sql = sqlite3.connect(dbfile)
        sql.execute("DELETE FROM user")
        sql.commit()

    except sqlite3.Error as e:
        print e
    sql.close()


