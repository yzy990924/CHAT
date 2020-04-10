#coding:utf-8
import socket
import Tkinter
import time
import tkMessageBox
import threading
import struct
import  client_gui

def get_config(path):
    f = open(path,'r')
    lines = f.readlines()
    IP = ''
    PORT = 0
    for line in lines:
        if line.find('IP') != -1:
            IP = line[line.find('IP') + 3:len(line) - 1]
        if line.find('PORT') != -1:
            PORT = eval(line[line.find('PORT') + 5:])
    return (IP,PORT)
class Connect_S:
    def __init__(self,clientp = None):
        self.server_ip,self.port = get_config('server_config.ini')
        print self.server_ip
        print self.port
        self.flag = True
        self.client = clientp # 客户端主类引用
        self.s = None

    def connection(self):
        if self.s != None:
            return
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.server_ip,self.port))
        except Exception:
            raise
        self.s = s
        self.t = threading.Thread(target=self.recv_mess)
        self.t.setDaemon(True)
        self.t.start()


    def bind_text(self,app):
        self.text = app

    def send_mess(self,mess_type,action_type,str_mess):  # 客户端发送消息  mess_type表示消息类型  action_type表示动作类型 str_mess 表示消息内容
       # send_data = str(mess_type) + str(action_type) + str_mess  # 长度为固定四个字节，也就是报头为6个字节
        send_len = str_mess.encode('utf-8')
        send_data = str(mess_type) + str(action_type) + struct.pack('<I',len(send_len)) + str_mess   # 长度为固定四个字节，也就是报头为6个字节
        self.s.send(send_data)

    def mess_process(self,mess_recv,head_str):
        if head_str == '02':
            self.client.stop_flag = '2'  # 用户不存在
        elif head_str == '01':
            self.client.stop_flag = '1' # 密码错误
        elif head_str == '00':
            self.client.stop_flag = '0' # 成功登录
        elif head_str == '03':
            self.client.stop_flag = '3' # 用户已在线
        elif head_str == '04':
            self.client.stop_flag = '4' # 用户名已存在
        elif head_str == '0B':
            self.client.stop_flag = 'B'# 注册成功
        elif head_str == '0C':
            self.client.stop_flag = 'C'# 注册成功
        elif head_str == '11':  # 大厅消息
            self.client.main_app.datingtext.insert(Tkinter.END, mess_recv)
        elif head_str == '12':  # 房间消息
            index = mess_recv.find('#')
            room_name = mess_recv[0:index]  # 得到房间名称
            mess_recv = mess_recv[index + 1:]
            if room_name in self.client.room_app:
                self.client.room_app[room_name].main_text.insert(Tkinter.END, mess_recv)
        elif head_str == '13': # 私人消息
            index = mess_recv.find('#')
            per_name = mess_recv[0:index]  # 得到用户名称
            mess_recv = mess_recv[index + 1:]
            if self.client.person_app.has_key(per_name): # 已经有私聊窗口
                self.client.person_app[per_name].main_text.insert(Tkinter.END, mess_recv)
            else:
                self.client.main_app.new_person = per_name
                self.client.main_app.after_idle(self.client.main_app.create_new_person)
                time.sleep(1)
                self.client.person_app[per_name].main_text.insert(Tkinter.END, mess_recv)
        elif head_str == '09': #所有上线用户
            on_user = mess_recv.split('#')
            for u in on_user:
                if u != '':
                    self.client.main_app.all_player.insert(Tkinter.END,u)
        elif head_str == '0A': #所有房间
            on_room = mess_recv.split('#')
            for u in on_room:
                if u != '':
                    self.client.main_app.allroom.insert(Tkinter.END,u)
        elif head_str == '07': # 创建新房间
            self.client.main_app.allroom.insert(Tkinter.END, mess_recv)
        elif head_str == '05':  # 用户登录
            self.client.main_app.all_player.insert(Tkinter.END, mess_recv)
        elif head_str == '06':  # 用户退出
            for i in range(self.client.main_app.all_player.size()):  # 删除退出用户
                if self.client.main_app.all_player.get(i) == mess_recv:
                    print self.client.main_app.all_player.get(i)
                    self.client.main_app.all_player.delete(i)
                    break



    def recv_mess(self):
        sock = self.s
        all_buffer = ''  # 该套接字接收缓冲区
        one_buffer = ''  # 该套接字正在接收的单个数据包部分
        flag = False  # 报头已得到标识
        head_str = ''  # 报头的字符串表示
        data_body_len = 0  # 此数据报数据部分应该接受的长度
        recive_len = 0  # 当前数据报已收到的长度
        while self.flag:
            tmp_buffer = sock.recv(1024)  # 本次获取的数据
            all_buffer = all_buffer + tmp_buffer
            if not tmp_buffer:
                break
            while True:
                if flag:  # 如果已得到报头
                    tmp_len = data_body_len - recive_len
                    if len(all_buffer) < tmp_len:  # 不能收到完整数据包
                        one_buffer += all_buffer  # 将所有数据放到单个包里,准备继续接收
                        recive_len += len(all_buffer)  # 改变已接受长度
                        all_buffer = ''  # 清空接收缓冲区
                        break
                    else:  # 已经收到完整数据包
                        one_buffer += all_buffer[0:tmp_len]
                        all_buffer = all_buffer[tmp_len + 1:]  # 清空已经放到单个包的缓冲区数据
                        ###
                        # 处理
                        self.mess_process(one_buffer, head_str)
                        ###
                        flag = False  # 变成未接收到报头
                        one_buffer = ''  # 清空单包数据
                        head_str = ''
                        recive_len = 0  # 清空长度
                else:  # 未接收到报头
                    all_len = len(all_buffer)  # 当前已经有的数据包长度
                    if all_len >= 6:
                        head_str = all_buffer[0:2]  # 头部表示
                        print head_str
                        print repr(all_buffer[2:6])
                        print struct.unpack('<I', all_buffer[2:6])
                        data_body_len = (struct.unpack('<I', all_buffer[2:6]))[0]
                        print data_body_len
                        flag = True
                        recive_len = 0
                        all_buffer = all_buffer[6:]
                        one_buffer = ''
                        if len(all_buffer) >= data_body_len:
                            one_buffer = all_buffer[:data_body_len]
                            all_buffer = all_buffer[data_body_len + 1:]
                            ###
                            # 处理
                            self.mess_process(one_buffer, head_str)
                            flag = False  # 变成未接收到报头
                            one_buffer = ''  # 清空单包数据
                            head_str = ''
                            recive_len = 0  # 清空长度
                        else:
                            break
                    else:
                        break
                        ###############################################

    def close_connection(self):
        self.flag = False
        if self.s:
            self.s.shutdown(True)
