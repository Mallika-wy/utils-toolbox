# 在服务器上使用clash

## 1. 下载clash

```bash
git clone https://github.com/Mallika-wy/Clash-for-linux.git
cd Clash-for-linux
chmod +x clash-linux-amd64-v1.10.0
```

## 2. 运行clash

```bash
./clash-linux-amd64-v1.10.0 -d . -f config.yaml
```

## 3. 使用clash

每次启动一个窗口，输入以下命令：

```bash
export HTTP_PROXY="http://127.0.0.1:7890"
export HTTPS_PROXY="http://127.0.0.1:7890"
```

具体端口号可以在`config.yaml`中查看，默认为7890。
