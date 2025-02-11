"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-12-15 21:01:16
LastEditors: Night-stars-1 nujj1042633805@gmail.com
LastEditTime: 2025-02-11 19:06:07
"""

import hashlib
import os


def calculate_file_hash(file_path, hash_algo="sha256"):
    """
    计算文件的哈希值。
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
    获取文件夹中所有文件的路径和哈希值。
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


def compare_folders(folder1, folder2, hash_algo="sha256"):
    """
    比较两个文件夹的文件哈希值。
    :param folder1: 第一个文件夹路径
    :param folder2: 第二个文件夹路径
    :param hash_algo: 使用的哈希算法
    :return: 差异结果
    """
    hashes1 = get_all_files_with_hash(folder1, hash_algo)
    hashes2 = get_all_files_with_hash(folder2, hash_algo)

    folder1_files = set(hashes1.keys())
    folder2_files = set(hashes2.keys())

    # 找出仅在各自文件夹中的文件
    only_in_folder1 = folder1_files - folder2_files
    only_in_folder2 = folder2_files - folder1_files

    # 找出路径相同但哈希值不同的文件
    common_files = folder1_files & folder2_files
    differing_files = [file for file in common_files if hashes1[file] != hashes2[file]]

    # 找出路径相同且内容相同的文件
    identical_files = [file for file in common_files if hashes1[file] == hashes2[file]]

    return {
        "only_in_folder1": only_in_folder1,
        "only_in_folder2": only_in_folder2,
        "differing_files": differing_files,
        "identical_files": identical_files,
    }


# 使用示例
if __name__ == "__main__":
    folder1 = "dist/HeiYue"  # 替换为第一个文件夹路径
    folder2 = "dist/HeiYue2"  # 替换为第二个文件夹路径

    differences = compare_folders(folder1, folder2)

    print("仅在文件夹1中的文件:")
    for file in differences["only_in_folder1"]:
        print(file)

    print("\n仅在文件夹2中的文件:")
    for file in differences["only_in_folder2"]:
        print(file)

    print("\n路径相同但内容不同的文件:")
    for file in differences["differing_files"]:
        print(file)

    print("\n路径相同且内容相同的文件:")
    for file in differences["identical_files"]:
        print(file)
