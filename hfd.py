#!/usr/bin/env python3
"""
HuggingFace 下载工具
支持下载模型和数据集，可配置镜像源
"""

import os
import argparse
from pathlib import Path
from typing import Optional


def download_model(
    model_id: str,
    save_dir: Optional[str] = None,
    use_mirror: bool = False,
    token: Optional[str] = None,
    revision: str = "main"
):
    """
    下载 HuggingFace 模型

    Args:
        model_id: 模型ID，如 "bert-base-chinese"
        save_dir: 保存目录，默认为 ./models/{model_name}
        use_mirror: 是否使用镜像源
        token: HuggingFace token（用于私有模型）
        revision: 版本分支，默认 "main"
    """
    try:
        from huggingface_hub import snapshot_download
    except ImportError:
        print("错误: 请先安装 huggingface_hub: pip install huggingface_hub")
        return False

    # 设置镜像源
    if use_mirror:
        os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
        print(f"使用镜像源: https://hf-mirror.com")

    # 设置保存路径
    if save_dir is None:
        save_dir = f"./models/{model_id.replace('/', '_')}"

    save_path = Path(save_dir)
    save_path.mkdir(parents=True, exist_ok=True)

    print(f"开始下载模型: {model_id}")
    print(f"保存路径: {save_path.absolute()}")

    try:
        snapshot_download(
            repo_id=model_id,
            local_dir=save_dir,
            local_dir_use_symlinks=False,
            revision=revision,
            token=token,
            resume_download=True
        )
        print(f"模型下载完成: {save_path.absolute()}")
        return True
    except Exception as e:
        print(f"下载失败: {e}")
        return False


def download_dataset(
    dataset_id: str,
    save_dir: Optional[str] = None,
    use_mirror: bool = False,
    token: Optional[str] = None,
    revision: str = "main"
):
    """
    下载 HuggingFace 数据集

    Args:
        dataset_id: 数据集ID，如 "squad"
        save_dir: 保存目录，默认为 ./datasets/{dataset_name}
        use_mirror: 是否使用镜像源
        token: HuggingFace token（用于私有数据集）
        revision: 版本分支，默认 "main"
    """
    try:
        from huggingface_hub import snapshot_download
    except ImportError:
        print("错误: 请先安装 huggingface_hub: pip install huggingface_hub")
        return False

    # 设置镜像源
    if use_mirror:
        os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
        print(f"使用镜像源: https://hf-mirror.com")

    # 设置保存路径
    if save_dir is None:
        save_dir = f"./datasets/{dataset_id.replace('/', '_')}"

    save_path = Path(save_dir)
    save_path.mkdir(parents=True, exist_ok=True)

    print(f"开始下载数据集: {dataset_id}")
    print(f"保存路径: {save_path.absolute()}")

    try:
        # local_dir_use_symlinks如果是True的话，就会以一种很奇怪的形式保存文件，导致后续使用datasets库加载数据集时找不到文件。创建符号链接？
        snapshot_download(
            repo_id=dataset_id,
            repo_type="dataset",
            local_dir=save_dir,
            local_dir_use_symlinks=False,
            revision=revision,
            token=token,
            resume_download=True
        )
        print(f"数据集下载完成: {save_path.absolute()}")
        return True
    except Exception as e:
        print(f"下载失败: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="HuggingFace 模型和数据集下载工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
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
        """
    )

    parser.add_argument("--model", type=str, help="模型ID，如 bert-base-chinese")
    parser.add_argument("--dataset", type=str, help="数据集ID，如 squad")
    parser.add_argument("--save-dir", type=str, help="保存目录")
    parser.add_argument("--mirror", action="store_true", help="使用镜像源 (hf-mirror.com)")
    parser.add_argument("--token", type=str, help="HuggingFace token（用于私有资源）")
    parser.add_argument("--revision", type=str, default="main", help="版本分支，默认 main")

    args = parser.parse_args()

    # 检查是否指定了模型或数据集
    if not args.model and not args.dataset:
        parser.print_help()
        print("\n错误: 请指定 --model 或 --dataset")
        return

    # 下载模型
    if args.model:
        success = download_model(
            model_id=args.model,
            save_dir=args.save_dir,
            use_mirror=args.mirror,
            token=args.token,
            revision=args.revision
        )
        if not success:
            exit(1)

    # 下载数据集
    if args.dataset:
        success = download_dataset(
            dataset_id=args.dataset,
            save_dir=args.save_dir,
            use_mirror=args.mirror,
            token=args.token,
            revision=args.revision
        )
        if not success:
            exit(1)


if __name__ == "__main__":
    main()
