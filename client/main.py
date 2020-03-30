# coding:utf-8
from client_gui import *
import Connect_Server
import struct
import time
import Tkinter
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
class client:
    def __init__(self):
        self.conn_sock = Connect_Server.Connect_S(clientp = self)       # 连接服务器的类
        self.gui = Login_application(clientp = self)
        self.text = None
        self.stop_flag = None  # 停止标志
        self.main_app = None  # 客户端大厅主界面引用
        self.room_app = {} # 客户端打开的房间引用字典 key 为房间名称 value 为房间引用
        self.person_app = {} # 客户端打开的私人聊天界面引用字典 key 为对方名称 value 为窗口引用
        self.start_time = None

    def change_gui(self,gui = None):
        self.gui = None
        self.gui = gui

    def show(self):
        self.gui.mainloop()

    def close(self):
        self.gui.quit()
try:
    app = client()
    app.show()
except IOError:
    raise
finally:
    app.conn_sock.close_connection()
    app.close()
#print bin(1222222)
#b =  struct.pack('<I',7888)
#print len(bb)
#print struct.unpack('<I',bb)


