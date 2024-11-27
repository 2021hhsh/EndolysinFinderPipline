import os
import shutil

# 指定源目录和目标目录
source_dir = '.'
target_dir = './肺炎_na'
dest_dir = './1164_fna'
txt_file = '1164.txt'

# 读取指定的txt文件中的所有行
with open(os.path.join(source_dir, txt_file), 'r') as f:
    lines = f.readlines()

# 在目标目录中查找是否有同名文件
for line in lines:
    target_file = os.path.join(target_dir, line.strip())
    if os.path.exists(target_file):
        # 将目标文件复制到指定目录下
        shutil.copy(target_file, os.path.join(dest_dir, line.strip()))
