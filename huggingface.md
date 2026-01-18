# huggingface 模型或者数据集下载

## 下载方法1：使用hfd.py脚本下载
1. 保证你的conda环境中有huggingface-hub
2. 运行如下命令即可下载：
```shell
# 下载模型
python hfd.py --model bert-base-chinese

# 下载数据集
python hfd.py --dataset squad

# 使用镜像源下载
python hfd.py --model bert-base-chinese --mirror

# 指定保存路径
python hfd.py --model gpt2 --save-dir ./my_models/gpt2

# 使用 token 下载私有模型
python hfd.py --model private/model --token hf_xxxxx
```

## 下载方法2：使用huggingface-cli命令行工具下载
1. 保证你的conda环境中有huggingface-hub
2. 使用如下命令进行下载
```shell
# 1. 下载模型到指定目录
huggingface-cli download meta-llama/Llama-2-7b-hf --local-dir ./llama2-7b

# 2. 只下载配置文件
huggingface-cli download meta-llama/Llama-2-7b-hf --include "*.json" --local-dir ./configs

# 3. 使用镜像加速下载
export HF_ENDPOINT=https://hf-mirror.com
huggingface-cli download bert-base-uncased --local-dir ./bert

# 4. 下载并保存到自定义缓存位置
export HF_HOME=/data/huggingface_cache
huggingface-cli download gpt2 --local-dir /data/models/gpt2
```

## 什么都不行怎么办
本地下载，SCP传输
1. scp -P 端口 本地路径 name@IP:服务器下载位置路径
2. 注意请本地压缩之后再传输