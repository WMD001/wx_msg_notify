import os
import sys

from pystray import Menu, MenuItem

from main import StayBackend
from notify.wx_notify import WxNotify
from wcferry import Wcf

from notify.log import logger

# wcf = Wcf(debug=False)
# print(wcf.get_contacts())
# print(wcf.get_friends())
# print(wcf.get_user_info())
# print(wcf.get_self_wxid())
# print(wcf.get_dbs())

# 未实现
# info_by_wxid = wcf.get_info_by_wxid("wxid_wdamwd770lrv22")


exe_path = os.path.dirname(sys.executable)
print(os.getcwd())
print(exe_path)

stay_backend = StayBackend()


def close_stay():
    stay_backend.stop()
    sys.exit(-1)

def on_clicked(icon, item):
    print(item.checked)
    if not item.checked:
        WxNotify.set_private()
        logger.info("已进入隐私模式")
    else:
        WxNotify.set_public()
        logger.info("已退出隐私模式")


menu = (
    Menu.SEPARATOR,
    MenuItem('隐私模式', on_clicked, checked=lambda item: WxNotify.mask),

    MenuItem('退出', close_stay)
)

stay_backend.set_menu(menu)
stay_backend.run()