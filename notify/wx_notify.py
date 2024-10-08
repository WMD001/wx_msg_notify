import os.path
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
        msg_data = ET.fromstring(msg.content)
        for child in msg_data:
            if child.tag == 'appmsg':
                msg_title = None
                msg_des = None
                msg_type = None
                for c in child:
                    if c.tag == 'type':
                        msg_type = c.text
                    if c.tag == 'title':
                        msg_title = c.text
                    if c.tag == 'des':
                        msg_des = c.text
                if msg_type == '2000':
                    # 转账
                    return msg_des
                if msg_type == '19':
                    # 聊天记录
                    return '[{}]'.format(msg_title)
                if msg_type == '17':
                    return '发起了位置共享'
                if msg_type == '6':
                    # 文件
                    return '[文件]' + msg_title
                if msg_type == '5':
                    # 链接
                    return '[链接]' + msg_title
                if msg_type == '57':
                    # 引用消息
                    return msg_title
                return msg_title
    elif msg_type == 10000:
        return msg.content
    else:
        return msg.content

    return content


def notify(sender, content, app_id='WeChat_Notify'):
    """
    发送通知到 windows 通知中心
    :param app_id: 消息标题
    :param sender: 发送人
    :param content: 消息内容
    :return:
    """
    logger.info("发送[{}]通知: {}, 来自: {}".format(app_id, content, sender))
    if WxNotify.mask:
        content = "发来一条微信消息"
    toast = Notification(app_id=app_id, title=sender, msg=r"{}".format(content),
                         icon=os.path.join(os.getcwd(), "assets/wx.ico"))
    toast.show()


class WxNotify:
    mask = False
    enable_gh = False

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
        contacts = self.wcf.query_sql("MicroMsg.db",
                                      "select UserName as wxid, Alias as code, Remark as remark, NickName as name from Contact")
        for contact in contacts:
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
        notify("", "Wx_Notify 已启动")

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

        # 获取发送人
        sender = msg.sender

        sender_name = self.get_sender_name(sender)
        if sender_name is None:
            # 如果联系人中没有发送人，重新加载联系人列表
            self.init_contacts()
            sender_name = self.get_sender_name(sender)

        # 获取发送内容
        content = get_msg_content(msg)

        if msg.from_group():
            # 免打扰
            if not self.enable_room_notify(msg.roomid):
                logger.info("群组已免打扰[{}]".format(msg.roomid))
                return
            content = f"{sender_name}: {content}"
            room_name = self.get_sender_name(msg.roomid)
            # 发送消息提醒
            notify(room_name, content)
        elif sender.startswith('gh'):
            if not WxNotify.enable_gh:
                logger.info("公众号已免打扰[{}]".format(sender))
                return
            # 公众号消息
            notify(sender_name, content)
        else:
            if not self.enable_person_notify(sender):
                logger.info("好友已免打扰[{}]".format(sender))
                return
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

    def enable_room_notify(self, roomid: str):
        """
        是否免打扰
        :param roomid: roomid
        :return: True 免打扰 / False 正常
        """
        contact_info = self.wcf.query_sql("MicroMsg.db", f"select * from Contact where UserName = '{roomid}'")[0]
        return contact_info['ChatRoomNotify'] == 1

    def enable_person_notify(self, username: str):
        """
        是否免打扰
        :param username: username
        :return: True 免打扰 / False 正常
        """
        contact_info = self.wcf.query_sql("MicroMsg.db", f"select * from Contact where UserName = '{username}'")[0]
        return contact_info['Type'] != 515

    @staticmethod
    def set_private():
        WxNotify.mask = True

    @staticmethod
    def set_public():
        WxNotify.mask = False
