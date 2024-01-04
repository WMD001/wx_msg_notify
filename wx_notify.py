import os.path
import sys
from queue import Empty
from xml.etree import ElementTree as ET

from wcferry import Wcf, WxMsg
from winotify import Notification


class WxNotify:
    def __init__(self):
        self.wcf = Wcf(debug=False)

    def start(self):
        print('开始监听消息')
        self.wcf.enable_receiving_msg()
        while self.wcf.is_receiving_msg():
            try:
                msg = self.wcf.get_msg()
                self.handle_msg(msg)
            except Empty:
                continue
            except Exception as e:
                print(e)

    def close(self):
        self.wcf.disable_recv_msg()

    def handle_msg(self, msg: WxMsg):
        if msg.from_self():
            return
        sender = msg.sender
        sender_info = self.wcf.get_info_by_wxid(sender)
        sender_name = sender_info['remark'] if sender_info['remark'] != '' else sender_info['name']
        content = self.get_msg_content(msg)
        if msg.from_group():
            if self.enable_room_notify(msg.roomid):
                room_info = self.wcf.get_info_by_wxid(msg.roomid)
                content = f'{sender_name}: {content}'
                sender_name = room_info['name']
            else:
                return

        if sender.startswith('gh'):
            content = f'{sender_name}: {content}'
            sender_name = '公众号消息'
        self.notify(sender_name, content)

    def notify(self, sender, content):
        exe_path = os.path.dirname(sys.executable)
        toast = Notification(app_id="微信消息", title=sender, msg=content, icon=os.path.join(exe_path, "wx.ico"))
        toast.show()

    def enable_room_notify(self, room_id: str):
        room_info = self.wcf.query_sql("MicroMsg.db", f"select * from Contact where UserName = '{room_id}'")[0]
        return room_info['ChatRoomNotify'] == 1

    def get_msg_content(self, msg: WxMsg) -> str:
        msg_type = msg.type
        content = ''
        if msg_type == 1:
            content = msg.content
        elif msg_type == 3:
            content = "[图片]"
        elif msg_type == 34:
            content = "[语音]"
        elif msg_type == 43:
            content = "[视频]"
        elif msg_type == 47:
            content = "[表情]"
        elif msg_type == 49:
            data = ET.fromstring(msg.content)
            content = data[0][0].text

        return content
