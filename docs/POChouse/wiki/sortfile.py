# 将README.md改名为父文件夹名.md
import os
import shutil
import re

def sortfile(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file == 'README.md':
                # print(root)
                # print(os.path.basename(root))
                # print(os.path.join(root, os.path.basename(root)+'.md'))
                shutil.move(os.path.join(root, file), os.path.join(root, os.path.basename(root)+'.md'))

sortfile('POChouse')