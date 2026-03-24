from huggingface_hub import HfApi, upload_large_folder

# 初始化API（自动读取你输入的Token）
api = HfApi()

# 上传大文件夹（核心：自动分块上传，断点续传）
upload_large_folder(
    repo_id="",  # 如 "zhangsan/ocean-swinlstm"
    folder_path="./data/",  # 要上传的本地文件夹
    repo_type="dataset",
    ignore_patterns=[".git", "*.log", "venv/"],  # 忽略无关文件（减少上传体积）
)