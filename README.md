### wx_msg_notify

基于 [WeChatFerry](https://github.com/lich0821/WeChatFerry) 实现windows平台的微信消息提醒

适用于微信3.9.2.23，下载地址在 [这里](https://github.com/lich0821/WeChatFerry/releases/latest)；也可以从 [WeChatSetup](https://gitee.com/lch0821/WeChatSetup) 找到。


### 依赖

- [WeChatFerry](https://github.com/lich0821/WeChatFerry)  一个玩微信的工具
- [winotify](https://github.com/versa-syahptr/winotify)  windows平台的消息提醒工具
- [pystray](https://pypi.org/project/pystray/)  程序最小化到系统托盘
- [PyInstaller](https://www.pyinstaller.org/)  打包工具


### 打包

目前使用 `pyinstaller` 进行打包


```shell
# 生成spec文件
pyinstaller main.py -i assets/notify.ico -n notify --hidden-import=_cffi_backend -w -y --add-data assets:assets

# 指定spec文件， 通过脚本复制文件
pyinstaller notify.spec
```

```shell
pyinstaller main.py -i assets/notify.ico -n notify --hidden-import=_cffi_backend -w -y --add-data assets:assets


pyinstaller notify.spec
```



