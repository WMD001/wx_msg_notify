import os.path
import sys
from queue import Empty
from threading import Thread
from xml.etree import ElementTree as ET

from wcferry import Wcf, WxMsg
from winotify import Notification

from notify.log import logger


def get_msg_content(msg: WxMsg) -> str:
    """
    获取消息内容
    {
        0: '朋友圈消息', 1: '文字', 3: '图片', 34: '语音', 37: '好友确认', 40: 'POSSIBLEFRIEND_MSG', 42: '名片', 43: '视频',
        47: '石头剪刀布 | 表情图片', 48: '位置', 49: '共享实时位置、文件、转账、链接', 50: 'VOIPMSG',
        51: '微信初始化', 52: 'VOIPNOTIFY', 53: 'VOIPINVITE', 62: '小视频', 66: '微信红包', 9999: 'SYSNOTICE', 1
        0000: '红包、系统消息', 10002: '撤回消息', 1048625: '搜狗表情', 16777265: '链接', 436207665: '微信红包',
        536936497: '红包封面', 754974769: '视频号视频', 771751985: '视频号名片', 822083633: '引用消息', 922746929: '拍一拍',
        973078577: '视频号直播', 974127153: '商品链接', 975175729: '视频号直播', 1040187441: '音乐链接', 1090519089: '文件'
    }
    :param msg: WxMsg
    :return: 内容，显示文本或者消息类别
    """
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


def notify(sender, content, app_id='微信消息'):
    """
    发送通知到 windows 通知中心
    :param app_id: 消息标题
    :param sender: 发送人
    :param content: 消息内容
    :return:
    """
    toast = Notification(app_id=app_id, title=sender, msg=content, icon=os.path.join(os.getcwd(), "assets/wx.ico"))
    toast.show()


class WxNotify:
    mask = False

    def __init__(self):
        self.wcf = Wcf(debug=False)
        # 初始化联系人
        self.contacts = {}
        self.init_contacts()
        logger.info("联系人初始化完成")

    def init_contacts(self):
        """
        初始化联系人
        self.contacts: {
            wxid: {
                    wxid, code, name, remark, country, province, city, gender
                }
        }
        :return:
        """
        self.wcf.get_contacts()
        for contact in self.wcf.contacts:
            self.contacts[contact['wxid']] = contact

    def start(self) -> None:
        """
        入口方法
        :return: void
        """
        receiving_msg = self.wcf.enable_receiving_msg()
        logger.info("开启消息监听：" + str(receiving_msg))

        def process_msg(wcf: Wcf):
            while wcf.is_receiving_msg():
                try:
                    msg = wcf.get_msg()
                    self.handle_msg(msg)
                except Empty:
                    continue
                except Exception as e:
                    logger.error(e)

        Thread(target=process_msg, name="GetMessage", args=(self.wcf,), daemon=True).start()
        logger.info('开始监听消息')

    def close(self):
        """
        停止接收消息
        :return:
        """
        self.wcf.disable_recv_msg()

    def handle_msg(self, msg: WxMsg):
        """
        处理接收到的消息
        :param msg: WxMsg
        :return:
        """

        # 忽略自己发送的消息
        if msg.from_self():
            return

        if WxNotify.mask:
            notify("", "收到一条微信消息")
            return

        # 获取发送人
        sender = msg.sender
        sender_name = self.get_sender_name(sender)

        # 是否允许发送通知
        # if not self.enable_notify(sender):
        #     return

        # 获取发送内容
        content = get_msg_content(msg)

        if msg.from_group():
            # 发送消息提醒
            notify(sender_name, content, "微信群组消息")
        elif sender.startswith('gh'):
            # 公众号消息
            notify(sender_name, content, "微信公众号消息")
        else:
            # 个人消息
            notify(sender_name, content)

    def get_sender_name(self, wxid):
        """
        获取发送人名称 / 群组名称 / 公众号名称
        :param wxid: wxid
        :return: remark > name
        """
        sender_info = self.contacts.get(wxid)
        if sender_info:
            if sender_info['remark']:
                return sender_info['remark']
            elif sender_info['name']:
                return sender_info['name']

    def enable_notify(self, username: str):
        """
        是否免打扰
        :param username: username
        :return: True 免打扰 / False 正常
        """
        contact_info = self.wcf.query_sql("MicroMsg.db", f"select * from Contact where UserName = '{username}'")[0]
        return contact_info['ChatRoomNotify'] == 1

    @staticmethod
    def set_private():
        WxNotify.mask = True

    @staticmethod
    def set_public():
        WxNotify.mask = False
