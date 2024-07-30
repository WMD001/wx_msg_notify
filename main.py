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
    notify.close()
    stay_backend.stop()
    sys.exit(-1)


def open_mask():
    WxNotify.set_private()


def close_mask():
    WxNotify.set_public()


if __name__ == '__main__':
    stay_backend = StayBackend()

    menu = (
        Menu.SEPARATOR,
        MenuItem('模糊', open_mask, enabled=not WxNotify.mask),
        MenuItem('清楚', close_mask, enabled=WxNotify.mask),

        MenuItem('退出', close_stay)
    )

    stay_backend.set_menu(menu)
    notify = WxNotify()
    backend_stay_thread = Thread(target=stay_backend.run)
    backend_stay_thread.start()
    notify.start()
    logger.debug("启动成功")


