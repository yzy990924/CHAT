# coding:utf-8
import Tkinter
import tkMessageBox
import time
import Connect_Server
# 登陆主界面
class Login_application(Tkinter.Frame):
    def __init__(self, master=None,clientp = None):
        Tkinter.Frame.__init__(self, master)
        self.grid(row = 0,column = 0,padx = 50,pady = 50)
        self.master.title('聊天客户端')
        self.master.geometry('400x200+700+300')
        self.client = clientp   # 客户端主类指针
        self.createWidgets()

    def createWidgets(self):
        self.idLabel = Tkinter.Label(self, text='账户名:')
        self.idLabel.grid(row = 0)
        self.id_input = Tkinter.Entry(self)
        self.id_input.grid(row = 0, column = 1)
        #############################
        self.passwdLabel = Tkinter.Label(self,text = '密码:')
        self.passwdLabel.grid(row = 1)
        self.passwd_input = Tkinter.Entry(self,show='*')
        self.passwd_input.bind('<Key-Return>',self.quick_login)
        self.passwd_input.grid(row = 1,column = 1)
        ########################################
        self.bpassButton = Tkinter.Button(self, text='忘记密码',command = self.back_pass)
        self.bpassButton.grid(row = 2,column = 2,sticky = Tkinter.E,ipadx = 3,ipady = 3)
        #######################################
        self.loginButton = Tkinter.Button(self, text='登录',command = self.login)
        self.loginButton.grid(row=2, column=0,ipadx = 20,ipady = 5)
        #######################################
        self.registerButton = Tkinter.Button(self, text='注册', command=self.new_user)
        self.registerButton.grid(row = 2,column = 1,ipadx = 20,ipady = 5)

    def new_user(self):          # 注册用户事件
        self.grid_remove()
        Register_application(clientp=self.client)

    def back_pass(self):
        self.grid_remove()
        Backpass_application(clientp=self.client)

    def login(self):     # 登录事件
        if self.id_input.get() == '':
            tkMessageBox.showinfo('提示','请输入账号')
            return
        try:
            self.client.conn_sock.connection() # 连接服务器
            self.client.conn_sock.send_mess('0','2',self.id_input.get() + '@@' + self.passwd_input.get())   # 发送登陆信息
        except IOError:
            tkMessageBox.showerror('错误','无法连接服务器')
            self.quit()
            return
        while self.client.stop_flag == None:
            time.sleep(0.1)
            print 'waiting...'
        if self.client.stop_flag == '0':
            self.grid_remove()
            Main_Room_application(clientp = self.client,username = self.id_input.get())
            print self.id_input.get() + '用户上线'
        elif self.client.stop_flag == '2':
            tkMessageBox.showerror('错误', '用户不存在')
        elif self.client.stop_flag == '1':
            tkMessageBox.showerror('错误', '密码错误')
        elif self.client.stop_flag == '3':
            tkMessageBox.showinfo('提示', '用户已在线')
        self.client.stop_flag = None

    def quick_login(self,event):
        self.login()

class Backpass_application(Tkinter.Frame):
    def __init__(self, master=None, clientp = None):
        Tkinter.Frame.__init__(self, master)
        self.grid(row = 0,column = 0,padx = 40,pady = 40)
        self.client = clientp           # 获得客户端主类指针
        self.master.title('找回密码')
        self.createWidgets()
     
    def createWidgets(self):
        self.idLabel = Tkinter.Label(self, text='账户名:')
        self.idLabel.grid(row = 0)
        self.id_input = Tkinter.Entry(self)
        self.id_input.grid(row = 0, column = 1)
        #############################
        self.passwdLabel = Tkinter.Label(self,text = '密码:')
        self.passwdLabel.grid(row = 1)
        self.passwd_input = Tkinter.Entry(self,show='*')
        self.passwd_input.grid(row = 1,column = 1)
        ########################################
        self.passwdLabel1 = Tkinter.Label(self, text='确认密码:')
        self.passwdLabel1.grid(row=2)
        self.passwd_input1 = Tkinter.Entry(self,show = '*')
        self.passwd_input1.grid(row=2, column=1)
        self.passwd_input1.bind('<Key-Return>',self.quick_summit)
        #################################################
        self.okButton = Tkinter.Button(self, text='确认',command = self.summit)
        self.okButton.grid(row=3, column=0,ipadx = 20)
        #######################################
        ######################################
        self.backButton = Tkinter.Button(self, text='返回', command=self.back_login)
        self.backButton.grid(row=3, column=1,sticky = Tkinter.E,ipadx = 50)
    def summit(self):
        if self.id_input.get() == '':
            tkMessageBox.showerror('错误','用户名不能为空!')
            return
        if self.passwd_input1.get() != self.passwd_input.get():
            tkMessageBox.showerror('错误', '两次输入的密码不一致!')
            return
        if self.passwd_input.get() == '':
            tkMessageBox.showerror('错误', '密码不能为空!')
            return
        if self.id_input.get().find('@') != -1:
            tkMessageBox.showerror('错误', '用户名不能包含@字符')
            return
        if self.passwd_input.get().find('@') != -1:
            tkMessageBox.showerror('错误', '密码不能包含@字符')
            return
        try:
            self.client.conn_sock.connection()
            self.client.conn_sock.send_mess('0','0',self.id_input.get() + '@@'+ self.passwd_input.get())
        except IOError:
            tkMessageBox.showerror('错误','无法连接服务器')
            self.quit()
            return
        while self.client.stop_flag == None:
            time.sleep(0.1)
            print 'waiting...'
        if self.client.stop_flag == 'D':
            tkMessageBox.showinfo('消息', '找回密码失败: ' + '用户名不存在')
        elif self.client.stop_flag == 'C':
            tkMessageBox.showinfo('消息', '密码找回成功\n')
        self.client.stop_flag = None

    def quick_summit(self,event):
        self.summit()

    def reset_input(self):
        self.id_input.delete(0, Tkinter.END)
        self.passwd_input.delete(0, Tkinter.END)
        self.passwd_input1.delete(0, Tkinter.END)
        return
    def back_login(self):
        self.grid_remove()
        Login_application(clientp=self.client)

# 注册界面
class Register_application(Tkinter.Frame):       #注册界面
    def __init__(self, master=None, clientp = None):
        Tkinter.Frame.__init__(self, master)
        self.grid(row = 0,column = 0,padx = 40,pady = 40)
        self.client = clientp           # 获得客户端主类指针
        self.master.title('注册界面')
        self.createWidgets()

    def createWidgets(self):
        self.idLabel = Tkinter.Label(self, text='账户名:')
        self.idLabel.grid(row = 0)
        self.id_input = Tkinter.Entry(self)
        self.id_input.grid(row = 0, column = 1)
        #############################
        self.passwdLabel = Tkinter.Label(self,text = '密码:')
        self.passwdLabel.grid(row = 1)
        self.passwd_input = Tkinter.Entry(self,show='*')
        self.passwd_input.grid(row = 1,column = 1)
        ########################################
        self.passwdLabel1 = Tkinter.Label(self, text='确认密码:')
        self.passwdLabel1.grid(row=2)
        self.passwd_input1 = Tkinter.Entry(self,show = '*')
        self.passwd_input1.grid(row=2, column=1)
        self.passwd_input1.bind('<Key-Return>',self.quick_summit)
        #################################################
        self.okButton = Tkinter.Button(self, text='确认',command = self.summit)
        self.okButton.grid(row=3, column=0,ipadx = 20)
        #######################################
        ######################################
        self.backButton = Tkinter.Button(self, text='返回', command=self.back_login)
        self.backButton.grid(row=3, column=1,sticky = Tkinter.E,ipadx = 50)
    def summit(self):
        if self.id_input.get() == '':
            tkMessageBox.showerror('错误','用户名不能为空!')
            return
        if self.passwd_input1.get() != self.passwd_input.get():
            tkMessageBox.showerror('错误', '两次输入的密码不一致!')
            return
        if self.passwd_input.get() == '':
            tkMessageBox.showerror('错误', '密码不能为空!')
            return
        if self.id_input.get().find('@') != -1:
            tkMessageBox.showerror('错误', '用户名不能包含@字符')
            return
        if self.passwd_input.get().find('@') != -1:
            tkMessageBox.showerror('错误', '密码不能包含@字符')
            return
        try:
            self.client.conn_sock.connection()
            self.client.conn_sock.send_mess('0','1',self.id_input.get() + '@@'+ self.passwd_input.get())
        except IOError:
            tkMessageBox.showerror('错误','无法连接服务器')
            self.quit()
            return
        while self.client.stop_flag == None:
            time.sleep(0.1)
            print 'waiting...'
        if self.client.stop_flag == '4':
            tkMessageBox.showinfo('消息', '注册失败: ' + '用户名已存在')
        elif self.client.stop_flag == 'B':
            tkMessageBox.showinfo('消息', '注册成功\n' + '用户名:' + self.id_input.get())
        self.client.stop_flag = None

    def quick_summit(self,event):
        self.summit()

    def reset_input(self):
        self.id_input.delete(0, Tkinter.END)
        self.passwd_input.delete(0, Tkinter.END)
        self.passwd_input1.delete(0, Tkinter.END)
        return
    def back_login(self):
        self.grid_remove()
        Login_application(clientp=self.client)

# 大厅主界面
class Main_Room_application(Tkinter.Frame):

    def __init__(self, master=None,clientp=None,username = None):
        Tkinter.Frame.__init__(self, master)
        self.grid(row = 0,column = 0,padx = 60,pady = 60)
        self.master.protocol("WM_DELETE_WINDOW", self.back_login)
        self.client = clientp
        print 'plain mainwindow.....'
        self.client.main_app = self   # 此时已经打开主界面，在主类中记录
        self.username = username  # 当前用户名
        self.new_person = ''
        self.createWidgets()
        print 'accomplete.....'

    def createWidgets(self):
        self.master.geometry('1200x700')
        ########################################################
        self.left_frame = Tkinter.Frame(self)
        self.left_frame.grid(row = 0,column = 0)
        self.label1 = Tkinter.Label(self.left_frame, text='当前用户:')
        self.label1.grid(row=0, column=0)
        self.label_name = Tkinter.Label(self.left_frame,text = self.username)
        self.label_name.grid(row = 0, column = 1)
        ########################################################
        self.roolabel = Tkinter.Label(self.left_frame,text = '选择房间:')
        self.roolabel.grid(row = 1,column = 0)
        roomlist = ['交友', '科技', '闲扯']
        self.scrollbar = Tkinter.Scrollbar(self.left_frame)
        self.scrollbar.grid(row = 1,column = 2,ipady = 25)
        self.allroom = Tkinter.Listbox(self.left_frame,yscrollcommand = self.scrollbar.set,height = 5)
        self.scrollbar['command'] = self.allroom.yview
        self.start_button = Tkinter.Button(self.left_frame,text = '进入房间',command = self.entry_room)
        self.allroom.grid(row = 1,column = 1,ipady = 10)
        ######################################
        self.start_button = Tkinter.Button(self.left_frame,text = '进入房间',command = self.entry_room)
        self.start_button.grid(row = 2,column = 1,ipady = 10,pady = 10)
        #############################################
        self.create_button = Tkinter.Button(self.left_frame, text='创建房间',command = self.create_room)
        self.create_button.grid(row=3, column=1,ipady = 10,pady = 10)
        ################################################
        self.back_button = Tkinter.Button(self.left_frame, text='退出登录',command = self.back_login)
        self.back_button.grid(row=4, column=1, ipady=10,pady = 10)
        ##############################################
        ##############################################
        ##############################################
        self.right_frame = Tkinter.Frame(self)
        self.right_frame.grid(row = 0,column = 1)
        ##################################################
       
        self.datingtext = Tkinter.Text(self.right_frame)
        self.datingtext.grid(row = 0, column = 0,rowspan = 3)
        self.messscrollbar = Tkinter.Scrollbar(self.right_frame)
        self.messscrollbar.grid(row = 1,column =1,ipady = 160)
        self.messscrollbar.config(command=self.datingtext.yview)
        self.datingtext.config(yscrollcommand = self.messscrollbar.set)
        self.datingtext.edit_modified(True)
        #########################################################
        self.input_str = Tkinter.Entry(self.right_frame)
        self.input_str.bind('<Key-Return>',self.quick_send_mess)
        self.input_str.grid(row=2, column=0, ipadx = 250, ipady = 10)
        ####################################################
        self.send_button = Tkinter.Button(self.right_frame,text = '发送',command = self.send_mess)
        self.send_button.grid(row = 2,column = 1,ipadx = 20,padx = 5)
        ####################################################
        self.all_player = Tkinter.Listbox(self.right_frame)
        self.all_player.bind('<Double-Button-1>',self.create_person_chat)         # 双击事件
        self.all_player.grid(row=1, column=2, sticky=Tkinter.N, ipady=100)
        ####################################
        self.onlinelabel = Tkinter.Label(self.right_frame, text='在线用户:')
        self.onlinelabel.grid(row=0, column=2,sticky = Tkinter.W,pady = 5)

        return

    def entry_room(self):
        if str(self.allroom.curselection()) == '()':
            tkMessageBox.showinfo('提示','未选择房间')
            return
        tmp_room = str(self.allroom.get(self.allroom.curselection()[0]))
        if self.client.room_app.has_key(tmp_room):
            return
        self.client.conn_sock.send_mess('0', '4', str(self.allroom.get(self.allroom.curselection()[0])) )  # 发送进入房间消息
        top = Tkinter.Toplevel(self)
        new_room = Main_Chat_application(master = top,clientp = self.client,room_name = tmp_room)
        self.client.room_app[tmp_room] = new_room   # 新增一个房间引用
        print 'roomnumber now:' + str(len(self.client.room_app))
        print 'user come in:'+  str(self.allroom.get(self.allroom.curselection()[0]))

    def create_room(self):
        top = Tkinter.Toplevel(self)
        New_room_application(master=top,clientp=self.client)
        return
    def send_mess(self):
        if self.input_str.get() == '':
            return
        self.client.conn_sock.send_mess('1','1',self.input_str.get())
        print self.input_str.get()
        print self.input_str.get()
        self.input_str.delete(0,Tkinter.END)
        return

    def quick_send_mess(self,event):
        self.send_mess()

    def create_person_chat(self,event):
        tmp_name = str(self.all_player.get(self.all_player.curselection()[0]))
        if self.client.person_app.has_key(tmp_name):
            return
        if tmp_name == self.username:
            return
        top = Tkinter.Toplevel(self)
        new_person = Main_Person_application(master = top, clientp=self.client,
                                         person_name = tmp_name)
        self.client.person_app[tmp_name] = new_person  # 新增一个私聊对象引用
        print 'private now:' + str(len(self.client.person_app))
        print 'user come in:' + str(self.all_player.get(self.all_player.curselection()[0]))

    def create_new_person(self):  # 消息来时弹出窗口
        per_name = self.new_person
        if self.client.person_app.has_key(per_name):
            return
        top = Tkinter.Toplevel(self)
        new_person = Main_Person_application(master=top, clientp=self.client,
                                             person_name=per_name)
        self.client.person_app[per_name] = new_person  # 新增一个私聊对象引用
        print 'private now:' + str(len(self.client.person_app))
        print 'out private:' + per_name

    def back_login(self):
        print self.username + 'user logout'
        self.quit()
# 房间主界面
class  Main_Chat_application(Tkinter.Frame):

    def __init__(self, master=None,clientp = None,room_name = None):
        Tkinter.Frame.__init__(self, master)
        self.grid(row = 0,column = 0,padx = 30,pady = 30)
        self.master.title('房间名称:' + room_name)
        self.master.geometry('1000x650+450+150')
        self.master.protocol("WM_DELETE_WINDOW", self.back_room) # 捕获窗口关闭事件
        self.client = clientp
        self.room_name = room_name     # 房间名称
        self.createWidgets()

    def createWidgets(self):
        self.label1 = Tkinter.Label(self,text = '消息窗口:')
        self.label1.grid(row = 0, column = 0,sticky = Tkinter.N)
        self.main_text = Tkinter.Text(self)
        self.main_text.grid(row = 0, column = 1,ipadx = 50,ipady = 50)
        #############################################
        self.label2 = Tkinter.Label(self, text='输入框:')
        self.label2.grid(row=1, column=0, sticky=Tkinter.N)
        self.input_text = Tkinter.Entry(self)
        self.input_text.bind('<Key-Return>',self.quick_send_mess)
        self.input_text.bind('<Key-Shift_R>', self.quick_send_ans)
        self.input_text.grid(row = 1, column = 1,ipadx = 300,ipady = 10,sticky =Tkinter.W)
        ################################
        ###################################
        self.sendButton = Tkinter.Button(self,text= '发送/ENTER',command = self.send_mess)
        self.sendButton.grid(row  = 1 ,column = 2,sticky = Tkinter.W,ipadx = 10 ,ipady = 10)

        # self.send_ans_Button = Tkinter.Button(self, text='发送game答案/Shift_R', command=self.send_ans)
        # self.send_ans_Button.grid(row=2, column=2, sticky=Tkinter.W, ipadx=10, ipady=10)

        self.backButton = Tkinter.Button(self,text = '退出房间',command = self.back_room)
        self.backButton.grid(row = 2, column = 1,sticky = Tkinter.W)
        return
    def back_room(self):
        print 'user exit room:' + self.room_name
        self.client.conn_sock.send_mess('0','5',self.room_name)  # 发送退出房间消息
        if self.client.room_app.has_key(self.room_name):
            self.client.room_app.pop(self.room_name)
        print 'roomnumber now:' + str(len(self.client.room_app))
        self.master.destroy()

    def create_person_chat(self,event):
        tmp_name = str(self.all_player.get(self.all_player.curselection()[0]))
        if self.client.person_app.has_key(tmp_name):
            return
        top = Tkinter.Toplevel(self)
        new_person = Main_Person_application(master=top, clientp=self.client,
                                         person_name = tmp_name)
        self.client.person_app[tmp_name] = new_person  # 新增一个私聊对象引用
        print 'private now:' + str(len(self.client.person_app))
        print 'user come in:' + str(self.all_player.get(self.all_player.curselection()[0]))

    def send_mess(self):
        if self.input_text.get() == '':
            return
        self.client.conn_sock.send_mess('1','2',self.room_name + '@@' + self.input_text.get())
        print self.input_text.get()
        self.input_text.delete(0,Tkinter.END)
        return

    def quick_send_mess(self,event):
        self.send_mess()

    def quick_send_ans(self,event):
        self.send_ans()
    # 新建房间界面
class New_room_application(Tkinter.Frame):

    def __init__(self, master=None,clientp=None):
        Tkinter.Frame.__init__(self, master)
        self.grid(row = 0,column = 0,padx = 60,pady = 60)
        self.master.protocol("WM_DELETE_WINDOW", self.close_create)
        self.client = clientp
        self.createWidgets()

    def createWidgets(self):
        self.idLabel = Tkinter.Label(self, text='房间名:')
        self.idLabel.grid(row=0)
        self.id_input = Tkinter.Entry(self)
        self.id_input.bind('<Key-Return>',self.quick_new_room)
        self.id_input.grid(row=0, column=1)
        #############################################
        self.addLabel = Tkinter.Label(self, text='备注:')
        self.addLabel.grid(row=1)
        self.add_input = Tkinter.Entry(self)
        self.add_input.bind('<Key-Return>',self.quick_new_room)
        self.add_input.grid(row=1, column=1)
        self.createButton = Tkinter.Button(self, text='创建', command=self.new_room)
        self.createButton.grid(row=3, column=1, ipadx=20, ipady=4, pady = 5)

    def new_room(self):
        for i in range(self.client.main_app.allroom.size()):
            if self.id_input.get() == self.client.main_app.allroom.get(i):
                tkMessageBox.showinfo('提示', '已存在该名称')
                return
        print 'create new room:' + self.id_input.get()
        self.client.conn_sock.send_mess('0','6',self.id_input.get() + '@@' + self.add_input.get())
        tkMessageBox.showinfo('提示','创建成功')
        self.master.destroy()

    def close_create(self):
        self.master.destroy()

    def quick_new_room(self,event):
        self.new_room()

# 私聊界面
class Main_Person_application(Tkinter.Frame):

    def __init__(self, master=None,clientp = None,person_name = None):
        Tkinter.Frame.__init__(self, master)
        self.grid(row = 0,column = 0,padx = 30,pady = 30)
        self.master.title('对方名称:' + person_name)
        self.master.geometry('880x550+500+150')
        self.master.protocol("WM_DELETE_WINDOW", self.back_chat) # 捕获窗口关闭事件
        self.client = clientp
        self.person_name = person_name     # 对方名称
        self.createWidgets()

    def createWidgets(self):
        self.label1 = Tkinter.Label(self,text = '消息窗口:')
        self.label1.grid(row = 0, column = 0,sticky = Tkinter.N)
        self.main_text = Tkinter.Text(self)
        self.main_text.grid(row = 0, column = 1,ipadx = 20,ipady = 5)
        #############################################
        self.label2 = Tkinter.Label(self, text='输入框:')
        self.label2.grid(row=1, column=0, sticky=Tkinter.N)
        self.input_text = Tkinter.Entry(self)
        self.input_text.bind('<Key-Return>',self.quick_send_mess)
        self.input_text.grid(row = 1, column = 1,ipadx = 200,ipady = 10,sticky =Tkinter.W)
        ################################
        self.sendButton = Tkinter.Button(self,text= '发送',command = self.send_mess)
        self.sendButton.grid(row  = 1 ,column = 2,sticky = Tkinter.W,ipadx = 10 ,ipady = 10)
        self.backButton = Tkinter.Button(self,text = '退出窗口',command = self.back_chat)
        self.backButton.grid(row = 2, column = 1,sticky = Tkinter.W)
        return

    def back_chat(self):
        print 'user exit:' + self.person_name
        if self.client.person_app.has_key(self.person_name):
            self.client.person_app.pop(self.person_name)
        print 'private now:' + str(len(self.client.person_app))
        self.master.destroy()

    def send_mess(self):
        if self.input_text.get() == '':
            return
        self.client.conn_sock.send_mess('1','3',self.person_name + '@@' + self.input_text.get())
        print self.input_text.get()
        self.main_text.insert(Tkinter.END,self.client.main_app.username + ': ' + self.input_text.get()+ '\n')
        self.input_text.delete(0,Tkinter.END)

    def quick_send_mess(self,event):
        self.send_mess()
