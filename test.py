import os
import sys

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