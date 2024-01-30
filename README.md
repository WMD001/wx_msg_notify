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
pyinstaller main.py -i notify.ico -n notify --hidden-import=_cffi_backend -w -y --add-data wcferry:wcferry
```

> 打包后将`wx.ico`和`notify.png`放在打包后的dist下notify目录下

### Feature

- [x] 文本消息
- [x] 图片消息
- [ ] 视频消息
- [ ] 链接消息
- [ ] 文件消息
- [x] 语音消息
- [ ] 表情消息
- [ ] 名片消息
- [ ] 链接消息
- [ ] 小程序消息
- [x] 引用消息
- [ ] 转发消息记录
- [ ] 撤回消息
- [ ] 拍一拍消息
- [ ] 邀请入群消息
- [ ] 好友添加成功消息
- [x] 群消息通知
- [ ] 公众号消息通知
- [ ] 隐私模式
