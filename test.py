import os
import sys

from pystray import Menu, MenuItem

from main import StayBackend
from notify.wx_notify import WxNotify
from wcferry import Wcf

from notify.log import logger

import struct


def parse_extra_buf(extra_buf):
    offset = 0
    parsed_data = {}

    try:
        while offset < len(extra_buf):
            # Read the tag (1 byte)
            tag = struct.unpack_from('<B', extra_buf, offset)[0]
            offset += 1

            # Read the length (1 byte)
            length = struct.unpack_from('<B', extra_buf, offset)[0]
            offset += 1

            # Read the value (length bytes)
            value = extra_buf[offset:offset + length]
            offset += length

            parsed_data[tag] = value

    except Exception as e:
        print(f"Error parsing extra_buf: {e}")

    return parsed_data

wcf = Wcf(debug=False)
# print(wcf.get_contacts())
# print(wcf.get_friends())
# print(wcf.get_user_info())
# print(wcf.get_self_wxid())
# print(wcf.get_dbs())
# print(wcf.get_tables(db='MicroMsg.db'))
# print(wcf.query_sql(db='MicroMsg.db', sql='select UserName, NickName, ChatRoomNotify from Contact where UserName = "45273110636@chatroom"'))
# info = wcf.query_sql(db='MicroMsg.db', sql='select * from Contact where UserName = "wxid_ggtdzbh7t0il12"')
# print(info)
# print(parse_extra_buf(info[0]['ExtraBuf']))
print(wcf.query_sql(db='MicroMsg.db', sql='select UserName, Remark, NickName, Type from Contact where UserName = "wxid_07otohc81r9n21"'))
# print(wcf.query_sql(db='MicroMsg.db', sql='select UserName, Remark, NickName, Type from Contact group by Type'))
# print(wcf.query_sql(db='MicroMsg.db', sql='select UserName, Remark, NickName, Type from Contact order by Type'))
# print(wcf.query_sql(db='MicroMsg.db', sql='select UserName, NickName, ChatRoomNotify from Contact where ChatRoomNotify=1'))
# print(wcf.query_sql(db='MicroMsg.db', sql='select UserName, NickName, ChatRoomNotify from Contact where ChatRoomNotify=0'))
print(wcf.query_sql(db='MicroMsg.db', sql='select UserName, NickName, ChatRoomNotify from Contact where Type=515'))
# print(wcf.query_sql(db='MicroMsg.db', sql='select * from ChatRoom limit 1'))
# print(wcf.query_sql(db='MicroMsg.db', sql='select * from ChatRoomInfo limit 1'))

# 未实现
# info_by_wxid = wcf.get_info_by_wxid("wxid_wdamwd770lrv22")
#
#
# exe_path = os.path.dirname(sys.executable)
# print(os.getcwd())
# print(exe_path)
#
# stay_backend = StayBackend()
#
#
# def close_stay():
#     stay_backend.stop()
#     sys.exit(-1)
#
# def on_clicked(icon, item):
#     print(item.checked)
#     if not item.checked:
#         WxNotify.set_private()
#         logger.info("已进入隐私模式")
#     else:
#         WxNotify.set_public()
#         logger.info("已退出隐私模式")
#
#
# menu = (
#     Menu.SEPARATOR,
#     MenuItem('隐私模式', on_clicked, checked=lambda item: WxNotify.mask),
#
#     MenuItem('退出', close_stay)
# )
#
# stay_backend.set_menu(menu)
# stay_backend.run()