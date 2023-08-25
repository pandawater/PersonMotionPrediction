import os
import string

from pathlib import Path
import subprocess
import shutil

# Set your directory path here
directory_path = r"D:\data_bvh"

source_path = r"D:\data_csv"



for root, dirs, files in os.walk(directory_path):
    #print(root)
    for filename in files:

        #print(filename)
        if filename.endswith(".bvh"):
            bvh_file_path = root+'\\' + filename

            new_root = root.replace("data_bvh", "data_csv")


            print('bvh_file_path   '+bvh_file_path)
            csv_file_path = os.path.join(root, filename)

            if not os.path.exists(new_root):
                os.makedirs(new_root)

            # 构建命令
            command = ["bvh-converter", csv_file_path]
            #
            # # 执行命令
            try:
                subprocess.run(command, check=True)
                print("Conversion completed successfully.")
            except subprocess.CalledProcessError:
                print("Conversion failed.")


            replace_name = filename[:4]+'_worldpos.csv'
            old_file = root+'\\'+replace_name
            print('old_file    '+old_file)

            shutil.move(old_file, new_root)
            print(f"Converted {bvh_file_path} to {csv_file_path}")
