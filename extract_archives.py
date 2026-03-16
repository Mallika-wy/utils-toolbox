#!/usr/bin/env python3
"""
Batch extract archive files under subfolders of a root path.

Usage examples:
  
# 先预览将要解压的内容（推荐）
python extract_archives.py . --dry-run

# 正式执行：解压当前目录下各子文件夹中的压缩包
python extract_archives.py .

# 包含更深层子目录
python extract_archives.py . --recursive --recursive-in-folder

# 解压到压缩包所在目录（不新建同名目录）并允许覆盖
python extract_archives.py . --inplace --overwrite
"""

from __future__ import annotations

import argparse
import shutil
import sys
import tarfile
import zipfile
from pathlib import Path


ARCHIVE_SUFFIXES = {
    ".zip",
    ".tar",
    ".gz",
    ".tgz",
    ".bz2",
    ".tbz",
    ".tbz2",
    ".xz",
    ".txz",
    ".rar",
    ".7z",
}


def is_supported_archive(path: Path) -> bool:
    if not path.is_file():
        return False
    name = path.name.lower()
    return any(name.endswith(suffix) for suffix in ARCHIVE_SUFFIXES)


def list_subfolders(root: Path, recursive: bool) -> list[Path]:
    if recursive:
        return sorted([p for p in root.rglob("*") if p.is_dir()])
    return sorted([p for p in root.iterdir() if p.is_dir()])


def find_archives(folders: list[Path], recursive_in_folder: bool) -> list[Path]:
    archives: list[Path] = []
    for folder in folders:
        iterator = folder.rglob("*") if recursive_in_folder else folder.iterdir()
        for item in iterator:
            if is_supported_archive(item):
                archives.append(item)
    return sorted(set(archives))


def extract_zip(archive: Path, target: Path) -> None:
    with zipfile.ZipFile(archive, "r") as zf:
        zf.extractall(target)


def extract_tar(archive: Path, target: Path) -> None:
    with tarfile.open(archive, "r:*") as tf:
        tf.extractall(target)


def extract_with_shutil(archive: Path, target: Path) -> bool:
    try:
        shutil.unpack_archive(str(archive), str(target))
        return True
    except (shutil.ReadError, ValueError):
        return False


def extract_archive(archive: Path, target: Path) -> None:
    lower_name = archive.name.lower()

    if lower_name.endswith(".zip"):
        extract_zip(archive, target)
        return

    if any(
        lower_name.endswith(suffix)
        for suffix in (".tar", ".tar.gz", ".tgz", ".tar.bz2", ".tbz", ".tbz2", ".tar.xz", ".txz")
    ):
        extract_tar(archive, target)
        return

    if extract_with_shutil(archive, target):
        return

    raise RuntimeError(
        f"Unsupported archive format or missing dependency: {archive.name}. "
        "For .7z/.rar, install a compatible backend (e.g. py7zr/patool or system tools)."
    )


def resolve_output_dir(archive: Path, inplace: bool) -> Path:
    if inplace:
        return archive.parent
    return archive.parent / archive.stem


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract archive files from each subfolder under a root path."
    )
    parser.add_argument("root", type=Path, help="Root path containing subfolders.")
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Include nested subfolders under root.",
    )
    parser.add_argument(
        "--recursive-in-folder",
        action="store_true",
        help="Search archives recursively inside each matched folder.",
    )
    parser.add_argument(
        "--inplace",
        action="store_true",
        help="Extract directly into the archive's current folder.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing extraction output directories.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned actions without extracting files.",
    )
    parser.add_argument(
        "--delete-archive",
        action="store_true",
        help="Delete archive file after successful extraction.",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    root: Path = args.root.expanduser().resolve()

    if not root.exists():
        print(f"[ERROR] Root path does not exist: {root}")
        return 2
    if not root.is_dir():
        print(f"[ERROR] Root path is not a directory: {root}")
        return 2

    folders = list_subfolders(root, args.recursive)
    if not folders:
        print(f"[INFO] No subfolders found under: {root}")
        return 0

    archives = find_archives(folders, args.recursive_in_folder)
    if not archives:
        print(f"[INFO] No archive files found in subfolders under: {root}")
        return 0

    success_count = 0
    fail_count = 0
    skip_count = 0

    for archive in archives:
        output_dir = resolve_output_dir(archive, args.inplace)
        action = f"{archive} -> {output_dir}"

        if not args.inplace and output_dir.exists():
            if args.overwrite:
                if args.dry_run:
                    print(f"[DRY-RUN] remove existing directory: {output_dir}")
                else:
                    shutil.rmtree(output_dir)
            else:
                print(f"[SKIP] output exists, use --overwrite to replace: {action}")
                skip_count += 1
                continue

        if args.dry_run:
            print(f"[DRY-RUN] extract: {action}")
            success_count += 1
            continue

        try:
            output_dir.mkdir(parents=True, exist_ok=True)
            extract_archive(archive, output_dir)
            if args.delete_archive:
                archive.unlink()
            print(f"[OK] extracted: {action}")
            success_count += 1
        except Exception as exc:  # noqa: BLE001
            print(f"[FAIL] {archive}: {exc}")
            fail_count += 1

    print(
        f"\nDone. success={success_count}, skipped={skip_count}, failed={fail_count}, total={len(archives)}"
    )
    return 1 if fail_count else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
