import os
import shutil
from typing import Callable, Optional
from zipfile import ZipFile

import requests
from loguru import logger

from core.utils.utils import StrPath


def download_file(
    url: str,
    path: str,
    progress_changed: Optional[Callable[[int], None]] = None,
    update_finished: Optional[Callable[[bool], None]] = None,
):
    """
    说明:
        下载文件，更新进度条
    参数:
        :param url 下载地址
        :param path: 保存的路径
        :param progress_changed: 可选的进度更新回调函数，接收一个整数参数表示下载进度百分比
    """
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        # 设置下载进度条
        total_size = int(response.headers.get("content-length", 0))
        cur_size = 0
        with open(path, "wb") as f:
            for data in response.iter_content(1024):
                f.write(data)
                if progress_changed:
                    cur_size += len(data)
                    # 更新进度条
                    progress_changed(int(cur_size / total_size * 100))
        if update_finished:
            update_finished(True)
    else:
        logger.info(f"下载文件失败 - {path} - {response.status_code}")


def unzip(
    zip_path: StrPath,
    extract_path: StrPath,
    progress_changed: Optional[Callable[[int], None]] = None,
    update_finished: Optional[Callable[[bool], None]] = None,
):
    """
    说明:
        解压文件，更新进度条
    参数:
        :param zip_path 压缩包路径
        :param extract_path 解压路径
    """
    with ZipFile(zip_path, "r") as zip_ref:
        total_size = sum((file.file_size for file in zip_ref.infolist()))
        cur_size = 0

        for file in zip_ref.infolist():
            zip_ref.extract(member=file, path=extract_path)
            if progress_changed:
                cur_size += file.file_size
                # 更新进度条
                progress_changed(int(cur_size / total_size * 100))
    if update_finished:
        update_finished(True)


def move_dir(
    src_dir: StrPath,
    dst_dir: StrPath,
    progress_changed: Optional[Callable[[int], None]] = None,
    update_finished: Optional[Callable[[bool], None]] = None,
):
    """
    说明:
        移动文件, 更新进度条
    参数:
        :param src: 源文件路径
        :param dst: 目标文件路径
    """
    if not os.path.isdir(src_dir):
        raise FileNotFoundError(f"源目录不存在: {src_dir}")
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir, exist_ok=True)

    all_files: list[list[str]] = []
    for root, _, files in os.walk(src_dir):
        for filename in files:
            src_path = os.path.normpath(os.path.join(root, filename))
            all_files.append(
                (
                    src_path,
                    src_path.replace(
                        os.path.normpath(src_dir), os.path.normpath(dst_dir)
                    ),
                )
            )

    total_size = len(all_files)
    if total_size == 0:
        logger.info("没有文件需要移动")
        return
    cur_size = 0

    for src_path, dst_path in all_files:
        try:
            dst_dir = os.path.dirname(dst_path)
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir, exist_ok=True)
            shutil.move(src_path, dst_path)
            if progress_changed:
                cur_size += 1
                # 更新进度条
                progress_changed(int(cur_size / total_size * 100))
        except Exception as e:
            logger.exception(f"移动失败: {src_path}, 错误: {str(e)}")
            if update_finished:
                update_finished(False)
            return
    if update_finished:
        update_finished(True)


def delete_files(
    files: list[StrPath],
    progress_changed: Optional[Callable[[int], None]] = None,
    update_finished: Optional[Callable[[bool], None]] = None,
):
    """
    说明:
        删除目录及其内容, 更新进度条
    参数:
        :param dir_path: 目录路径
    """
    total_size = len(files)
    cur_size = 0
    for file in files:
        if os.path.exists(file):
            try:
                os.remove(file)
                # 更新进度条
                if progress_changed:
                    cur_size += 1
                    progress_changed(int(cur_size / total_size * 100))
            except Exception as e:
                logger.error(f"删除文件失败: {file}, 错误: {str(e)}")
    if update_finished:
        update_finished(True)
