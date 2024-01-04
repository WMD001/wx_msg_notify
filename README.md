### wx_msg_notify

基于 [WeChatFerry](https://github.com/lich0821/WeChatFerry) 实现windows平台的微信消息提醒

适用于微信3.9.2.23，下载地址在 [这里](https://github.com/lich0821/WeChatFerry/releases/latest)；也可以从 [WeChatSetup](https://gitee.com/lch0821/WeChatSetup) 找到。



### 打包

目前使用 `pyinstaller` 进行打包

```shell
pyinstaller main.py -i notify.ico -n notify --hidden-import=_cffi_backend -w -y --add-data wcferry:wcferry
```

> 打包后将`wx.ico`和`notify.png`放在打包后的dist下notify目录下

