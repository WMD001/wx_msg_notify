from wcferry import Wcf, WxMsg
from queue import Empty
import xml.etree.ElementTree as et
from winotify import Notification
from pystray import Icon, Menu, MenuItem
from PIL import Image
from threading import Thread

image = Image.open("notify.png")


def notify(sender, content):
    toast = Notification(app_id="微信消息", title=sender, msg=content, icon=r"D:\software\Tencent\WeChat\8.ico")
    toast.show()


def handle_msg(wcf: Wcf, msg: WxMsg):
    sender = msg.sender
    sender_info = wcf.get_info_by_wxid(sender)
    name = sender_info['remark'] if sender_info['remark'] != '' else sender_info['name']
    content = ""

    if msg.from_self():
        return
    elif msg.from_group():
        pass
    else:
        msg_type = msg.type
        if msg_type == 3:
            content = "[图片]"
        elif msg_type == 1:
            content = msg.content
        elif msg_type == 49:
            data = et.fromstring(msg.content)
            content = data[0][0].text

        notify(name, content)


def handle_start():
    wcf = Wcf(debug=False)
    wcf.enable_receiving_msg()
    while wcf.is_receiving_msg():
        try:
            msg = wcf.get_msg()
            handle_msg(wcf, msg)
        except Empty:
            continue
        except Exception as e:
            print(e)


def quit_exe(icon: Icon):
    icon.stop()


menu = (Menu.SEPARATOR, MenuItem('退出', quit_exe))


icon = Icon("name", image, "WxNotify", menu)


if __name__ == '__main__':
    Thread(target=icon.run, daemon=False).start()
    Thread(target=handle_start, daemon=True).start()


