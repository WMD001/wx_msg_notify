import sys

from pystray import Icon, Menu, MenuItem
from PIL import Image
from threading import Thread

from notify.wx_notify import WxNotify
from notify.log import logger


class StayBackend:

    def __init__(self):
        self.icon = None
        self.menu = None
        self.image = Image.open("assets/notify.png")

    def set_menu(self, menu):
        self.menu = menu
        self.icon = Icon("name", self.image, "WxNotify", self.menu)

    def run(self):
        self.icon.run()

    def stop(self):
        self.icon.stop()


def close_stay():
    try:
        notify.close()
        stay_backend.stop()
        sys.exit(0)
    except Exception as e:
        logger.error(e)
        sys.exit(1)


def check_mask(icon, item):
    if not item.checked:
        WxNotify.set_private()
        logger.info("已进入隐私模式")
    else:
        WxNotify.set_public()
        logger.info("已退出隐私模式")


if __name__ == '__main__':
    stay_backend = StayBackend()

    menu = (
        Menu.SEPARATOR,
        MenuItem('隐私模式', check_mask, checked=lambda item: WxNotify.mask),
        MenuItem('退出', close_stay)
    )

    stay_backend.set_menu(menu)
    notify = WxNotify()
    backend_stay_thread = Thread(target=stay_backend.run)
    backend_stay_thread.start()
    notify.start()
    logger.debug("启动成功")


