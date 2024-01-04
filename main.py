import sys

from pystray import Icon, Menu, MenuItem
from PIL import Image
from threading import Thread

from wx_notify import WxNotify


class StayBackend:

    def __init__(self):
        self.icon = None
        self.menu = None
        self.image = Image.open("notify.png")

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


if __name__ == '__main__':
    stay_backend = StayBackend()
    stay_backend.set_menu((Menu.SEPARATOR, MenuItem('退出', close_stay)))
    notify = WxNotify()
    backend_stay_thread = Thread(target=stay_backend.run)
    backend_stay_thread.start()
    notify.start()


