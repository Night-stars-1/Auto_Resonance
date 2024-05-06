"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-29 12:51:19
LastEditTime: 2024-05-06 23:12:56
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import asyncio
import shutil
import sys
import time
from enum import Enum
from pathlib import Path
from typing import List, TypedDict
from zipfile import ZipFile

from aiohttp import ClientSession
from packaging.version import parse
from tqdm import tqdm

from version import __version__

ROOT_PATH = Path()
TEMP_PATH = ROOT_PATH / "temp"
"""临时路径，用于存放下载的文件"""
HEIYUE_FILE_PATH = TEMP_PATH / "heiyue.zip"
"""更新包路径"""


class AssetsModel(TypedDict):
    browser_download_url: str


class APIResultModel(TypedDict):
    tag_name: str
    """版本标签"""
    assets: List[AssetsModel]
    """资源"""


class UpdateStatus(Enum):
    """更新状态枚举类"""

    Latest = 1
    UPDATE = 2
    FAILURE = 0
    NOSUPPORT = 3


class Updater:
    """应用程序更新器，负责检查、下载、解压和安装最新版本的应用程序。"""

    def __init__(self):
        self.unzip_dir = TEMP_PATH
        self.api_urls = [
            "https://api.github.com/repos/Night-stars-1/Auto_Resonance/releases/latest",
            "https://goda.srap.link/gitapi/https://api.github.com/repos/Night-stars-1/Auto_Resonance/releases/latest",
        ]
        self.mirror_urls = ["", "https://mirror.ghproxy.com/"]

    async def find_fastest_mirror(self, url: str, timeout=5):
        """
        说明:
            测速并找到最快的镜像
        参数:
            :param url 测速地址
            :param timeout 超时时间
        """

        async def fetch_url(session: ClientSession, mirror_url: str):
            start_time = time.time()  # 记录请求开始时间
            try:
                async with session.head(
                    mirror_url,
                    timeout=timeout,
                    allow_redirects=True,
                ) as response:
                    if response.status == 200:
                        speed_time = time.time() - start_time
                        print(mirror_url, speed_time)
                        return mirror_url, speed_time  # 返回URL和响应时间
                    else:
                        return mirror_url, float(
                            "inf"
                        )  # 如果响应状态不是200，返回无限大的时间
            except Exception:
                return mirror_url, float("inf")  # 如果请求失败，返回无限大的响应时间

        async with ClientSession() as session:
            tasks = [
                fetch_url(session, mirror_url + url) for mirror_url in self.mirror_urls
            ]
            results = await asyncio.gather(*tasks)
            # 按响应时间排序并返回最快的结果
            fastest_url, fastest_time = min(results, key=lambda x: x[1])
            print(f"最快的下载地址: {fastest_url} 响应时间: {fastest_time:.2f}s")
            return fastest_url

    async def get_first_valid_response(self):
        async def fetch(session: ClientSession, url):
            try:
                async with session.get(url) as response:
                    data: APIResultModel = await response.json()
                    if data["tag_name"]:  # 检查是否是有效结果
                        return data
            except Exception as e:
                return None
            return None

        async with ClientSession() as session:
            tasks = [asyncio.create_task(fetch(session, url)) for url in self.api_urls]
            while tasks:
                done, pending = await asyncio.wait(
                    tasks, return_when=asyncio.FIRST_COMPLETED
                )

                # 检查已完成的任务是否有有效结果
                for task in done:
                    result = task.result()
                    if result:
                        # 如果找到有效结果，取消所有其他任务
                        for p in pending:
                            p.cancel()
                        return result  # 返回第一个有效的结果

                # 没有有效结果，更新任务列表继续等待
                tasks = list(pending)

            return None  # 所有请求完成但没有有效结果

    async def get_update_status(self):
        """
        说明:
            检查是否是最新版本
        参数:
            :param version 版本号
        """
        if not getattr(sys, "frozen", False):
            return UpdateStatus.NOSUPPORT, ""
        try:
            result = await self.get_first_valid_response()
            if result:
                version = result["tag_name"]
                download_url: str = result["assets"][0]["browser_download_url"]
                self.unzip_dir = TEMP_PATH / f"Auto_Resonance_{version}"
                return (
                    UpdateStatus.Latest
                    if parse(version) <= parse(__version__)
                    else UpdateStatus.UPDATE
                ), download_url
            return UpdateStatus.FAILURE, ""
        except Exception as e:
            print(f"获取更新信息失败: {e}")
            return UpdateStatus.FAILURE, ""

    async def download_file_with_progress(self, fastest_url: str):
        """
        说明:
            下载文件，并显示进度条
        参数:
            :param fastest_url 下载地址
        """
        async with ClientSession() as session:
            async with session.get(fastest_url) as resp:
                if resp.status == 200:
                    # 设置下载进度条
                    total_size = int(resp.headers.get("content-length", 0))
                    with tqdm(
                        total=total_size,
                        unit="B",
                        unit_scale=True,
                        desc=HEIYUE_FILE_PATH.name,
                    ) as progress:
                        with open(HEIYUE_FILE_PATH, "wb") as f:
                            async for data in resp.content.iter_chunked(1024):
                                f.write(data)
                                # 更新进度条
                                progress.update(len(data))
                else:
                    print(f"下载文件失败 - {resp.status}")

    def unzip_with_progress(self, zip_path, extract_path):
        """
        说明:
            解压文件，并显示进度条
        参数:
            :param zip_path 压缩包路径
            :param extract_path 解压路径
        """
        with ZipFile(zip_path, "r") as zip_ref:
            # 获取文件总大小
            total_size = sum((file.file_size for file in zip_ref.infolist()))
            with tqdm(
                total=total_size, unit="B", unit_scale=True, desc="解压中"
            ) as pbar:
                # 循环解压每一个文件
                for file in zip_ref.infolist():
                    # 文件解压缩并指定解压路径
                    zip_ref.extract(member=file, path=extract_path)
                    # 更新进度条
                    pbar.update(file.file_size)

    def get_total_size(self, directory: Path):
        """
        说明:
            计算给定目录下所有文件的总大小
        """
        total_size = sum(
            file.stat().st_size for file in directory.rglob("*") if file.is_file()
        )
        return total_size

    def sync_subdirectories(self, source: Path, destination: Path):
        """
        说明:
            根据来源目录的文件夹删除目标目录的文件夹
        参数:
            :param source 源目录
            :param destination 目标目录
        """

        # 获取source目录下所有的子目录
        source_dirs = [d for d in source.iterdir() if d.is_dir()]

        # 遍历source目录下的子目录
        for source_dir in source_dirs:
            # 构建在destination中相应的目录路径
            dest_dir = destination / source_dir.name
            if dest_dir.exists():
                shutil.rmtree(dest_dir)

    def move_directory_with_progress(self, source: Path, destination: Path):
        """
        说明:
            移动文件夹, 并显示进度条
        参数:
            :param source 源目录
            :param destination 目标目录
        """
        # 计算源目录下所有文件的总大小
        total_size = self.get_total_size(source)

        # 创建进度条
        with tqdm(
            total=total_size, unit="B", unit_scale=True, desc="移动文件中"
        ) as pbar:
            # 遍历源目录中的所有文件和子目录
            for item in source.rglob("*"):
                if item.name == "HeiYue Updater.exe":
                    item = item.replace(item.parent / "HeiYue Updater.exe.new")
                # 创建目标路径
                target = destination / item.relative_to(source)
                target.parent.mkdir(parents=True, exist_ok=True)  # 确保目标目录存在

                if item.is_file():
                    szie = item.stat().st_size
                    # 移动文件并更新进度条
                    shutil.move(item, target)
                    pbar.update(szie)
                elif item.is_dir() and not target.exists():
                    # 创建目标子目录
                    target.mkdir(parents=True, exist_ok=True)

    async def run(self):
        """
        说明:
            运行更新流程
        """
        update_status, download_url = await self.get_update_status()
        if update_status == UpdateStatus.UPDATE:
            fastest_url = await self.find_fastest_mirror(download_url)
            await self.download_file_with_progress(fastest_url)
            self.unzip_with_progress(HEIYUE_FILE_PATH, TEMP_PATH)
            self.sync_subdirectories(self.unzip_dir, ROOT_PATH)
            self.move_directory_with_progress(self.unzip_dir, ROOT_PATH)
        elif update_status == UpdateStatus.FAILURE:
            print("获取更新信息失败")
        else:
            print("已经是最新版了")


def check_temp_dir_and_run():
    """检查临时目录并运行更新程序。"""
    print("开始检查更新")
    if not getattr(sys, "frozen", False):
        print("更新程序只支持打包成exe后运行")
        return UpdateStatus.NOSUPPORT

    if TEMP_PATH.exists():
        shutil.rmtree(TEMP_PATH)
    TEMP_PATH.mkdir(parents=True, exist_ok=True)

    updater = Updater()
    asyncio.run(updater.run())


if __name__ == "__main__":
    check_temp_dir_and_run()
