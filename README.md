### 打包问题

使用 `pyinstaller` 进行打包

```shell
pyinstaller main.py -i notify.ico -n notify --hidden-import=_cffi_backend
```

打包后需要将 `wcf.exe` 和 `_cffi_backend.cp39-win_amd64.pyd` 文件手动放在 dist/_internal/wcferry 下，exe文件才可以正常启动
