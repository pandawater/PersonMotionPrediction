import os
import shutil

def rename_and_move_files(source_directory, target_directory, old_str, new_str):
    directory_path = target_directory + '\\' + new_string
    file_count = 0

    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    #caculate
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            file_count += 1

    for filename in os.listdir(source_directory):
        if old_str in filename:
            new_filename = str(file_count).zfill(4)+'.fbx'
            file_count += 1
            source_path = os.path.join(source_directory, filename)
            target_path = os.path.join(directory_path, new_filename)
            shutil.move(source_path, target_path)
            print(f"Renamed and moved {source_directory}{filename} to {target_path}")

# 使用示例
source_directory_path = ""  # 替换为源目录的路径
target_directory_path = ""  # 替换为目标目录的路径
old_string = "comfort"                     # 要替换的旧字符串
new_string = "comfort1"                                # 新的字符串

rename_and_move_files(source_directory_path, target_directory_path, old_string, new_string)

