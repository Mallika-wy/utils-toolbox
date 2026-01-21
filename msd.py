#!/usr/bin/env python3
"""
ModelScope 下载工具
支持下载模型和数据集，适合在无法访问 HuggingFace 的环境使用
"""

import os
import argparse
from pathlib import Path
from typing import Optional


def download_model(
    model_id: str,
    save_dir: Optional[str] = None,
    revision: str = "master"
):
    """
    下载 ModelScope 模型

    Args:
        model_id: 模型ID，如 "qwen/Qwen-VL-Chat"
        save_dir: 保存目录，默认为 ./models/{model_name}
        revision: 版本分支，默认 "master"
    """
    try:
        from modelscope.hub.snapshot_download import snapshot_download
    except ImportError:
        print("错误: 请先安装 modelscope: pip install modelscope")
        return False

    # 设置保存路径
    if save_dir is None:
        save_dir = f"./models/{model_id.replace('/', '_')}"

    save_path = Path(save_dir)
    save_path.mkdir(parents=True, exist_ok=True)

    print(f"开始下载模型: {model_id}")
    print(f"保存路径: {save_path.absolute()}")

    try:
        model_dir = snapshot_download(
            model_id=model_id,
            cache_dir=save_dir,
            revision=revision
        )
        print(f"模型下载完成: {model_dir}")
        return True
    except Exception as e:
        print(f"下载失败: {e}")
        return False


def download_dataset(
    dataset_id: str,
    save_dir: Optional[str] = None,
    subset_name: str = "default",
    split: str = "train"
):
    """
    下载 ModelScope 数据集

    Args:
        dataset_id: 数据集ID，如 "clue/afqmc"
        save_dir: 保存目录，默认为 ./datasets/{dataset_name}
        subset_name: 子集名称，默认 "default"
        split: 数据集分割，默认 "train"
    """
    try:
        from modelscope.msdatasets import MsDataset
    except ImportError:
        print("错误: 请先安装 modelscope: pip install modelscope")
        return False

    # 设置保存路径
    if save_dir is None:
        save_dir = f"./datasets/{dataset_id.replace('/', '_')}"

    save_path = Path(save_dir)
    save_path.mkdir(parents=True, exist_ok=True)

    print(f"开始下载数据集: {dataset_id}")
    print(f"子集: {subset_name}, 分割: {split}")
    print(f"保存路径: {save_path.absolute()}")

    try:
        dataset = MsDataset.load(
            dataset_id,
            subset_name=subset_name,
            split=split,
            cache_dir=save_dir
        )
        print(f"数据集下载完成: {save_path.absolute()}")
        print(f"数据集大小: {len(dataset)} 条")
        return True
    except Exception as e:
        print(f"下载失败: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="ModelScope 模型和数据集下载工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 下载模型
  python msd.py --model qwen/Qwen-VL-Chat

  # 下载 Qwen3-VL-4B-Instruct
  python msd.py --model qwen/Qwen3-VL-4B-Instruct

  # 下载数据集
  python msd.py --dataset clue/afqmc

  # 指定保存路径
  python msd.py --model qwen/Qwen-VL-Chat --save-dir ./my_models/qwen

  # 下载数据集并指定子集和分割
  python msd.py --dataset clue/afqmc --subset default --split train

  # 指定模型版本
  python msd.py --model qwen/Qwen-VL-Chat --revision v1.0
        """
    )

    parser.add_argument("--model", type=str, help="模型ID，如 qwen/Qwen-VL-Chat")
    parser.add_argument("--dataset", type=str, help="数据集ID，如 clue/afqmc")
    parser.add_argument("--save-dir", type=str, help="保存目录")
    parser.add_argument("--revision", type=str, default="master", help="模型版本分支，默认 master")
    parser.add_argument("--subset", type=str, default="default", help="数据集子集名称，默认 default")
    parser.add_argument("--split", type=str, default="train", help="数据集分割，默认 train")

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
            revision=args.revision
        )
        if not success:
            exit(1)

    # 下载数据集
    if args.dataset:
        success = download_dataset(
            dataset_id=args.dataset,
            save_dir=args.save_dir,
            subset_name=args.subset,
            split=args.split
        )
        if not success:
            exit(1)


if __name__ == "__main__":
    main()
