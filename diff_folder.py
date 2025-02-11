"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-12-15 21:01:16
LastEditors: Night-stars-1 nujj1042633805@gmail.com
LastEditTime: 2025-02-12 00:57:30
"""

import hashlib
import json
import os
import zipfile

import requests

from version import __version__

TOKEN = os.environ.get("GITHUB_TOKEN")
HEADERS = {
    "Authorization": f"Bearer {TOKEN}"
}

def get_latest_hash():
    """
    获取最新的release的hash文件
    """
    response = requests.get("https://api.github.com/repos/Night-stars-1/Auto_Resonance/releases/latest")
    result: dict = response.json()
    tag_name = result.get("tag_name")
    asset = next((asset for asset in result["assets"] if asset["name"] == "hash.json"), None)
    if asset:
        response = requests.get(asset["browser_download_url"])
        result = response.json()
        return result, tag_name
    else:
        return {}, None


def calculate_file_hash(file_path, hash_algo="sha256"):
    """
    计算文件的哈希值

    :param file_path: 文件路径
    :param hash_algo: 使用的哈希算法（默认：SHA256）
    :return: 文件哈希值
    """
    hash_func = hashlib.new(hash_algo)
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):  # 分块读取文件内容
            hash_func.update(chunk)
    return hash_func.hexdigest()


def get_all_files_with_hash(folder, hash_algo="sha256"):
    """
    获取文件夹中所有文件的路径和哈希值

    :param folder: 文件夹路径
    :param hash_algo: 使用的哈希算法
    :return: 字典 {相对路径: 哈希值}
    """
    file_hashes = {}
    for root, _, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, folder)
            file_hashes[relative_path] = calculate_file_hash(file_path, hash_algo)
    return file_hashes


def compare_folders(target_folder, hash_algo="sha256"):
    """
    比较两个文件夹的文件哈希值

    :param target_folder: 比对目标文件夹路径
    :param hash_algo: 使用的哈希算法
    :return: 差异结果
    """
    source_hashes, tag_name = get_latest_hash()

    target_hashes = get_all_files_with_hash(target_folder, hash_algo)

    # 保存目标文件hash
    with open("hash.json", "w") as f:
        json.dump(target_hashes, f)
    
    source_files = set(source_hashes.keys())
    target_files = set(target_hashes.keys())

    only_in_folder2 = target_files - source_files

    # 找出路径相同但哈希值不同的文件
    common_files = source_files & target_files
    differing_files = set(
        [file for file in common_files if source_hashes[file] != target_hashes[file]]
    )

    return differing_files | only_in_folder2, tag_name


def zip_files(differences, zip_filename, base_folder):
    """
    压缩文件列表到压缩包

    :param differences: 文件列表
    :param zip_filename: 压缩包路径
    :param base_folder: 压缩包中的根目录
    """
    # 创建一个 Zip 文件并添加文件
    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file in differences:
            # 获取文件的绝对路径
            file_path = os.path.join(base_folder, file)

            # 确保文件存在
            if os.path.exists(file_path):
                # 使用相对路径作为文件在 zip 内的路径
                arcname = os.path.relpath(file_path, base_folder)
                zipf.write(file_path, arcname=arcname)
            else:
                print(f"{file_path} 不存在")

if __name__ == "__main__":
    target_folder = "dist/heiyue"

    differences, tag_name = compare_folders(target_folder)
    if tag_name:
        print(f"increment_zip=Auto_Resonance_Update_{tag_name}.zip")
        zip_files(differences, f"Auto_Resonance_Update_{tag_name}.zip", target_folder)
