# 搜索目录下是否有符合条件的POC文件，如果有则生成pocFiles.md文件

import os

ignoreDirs = ["assets", "gitbook"]
ignoreFiles = ["sort.sh", "sortfile.py"]
# exts For pocs
exts = [".py", ".jar", ".zip", ".sh", ".php", ".war", ".java", ".jsp", ".tar", ".gz", ".xz", ".rar", ".nse"]

for root, dirs, files in os.walk("./docs"):
    for dir in dirs:
        if dir in ignoreDirs:
            dirs.remove(dir)
    for file in files:
        if file in ignoreFiles:
            files.remove(file)
    with open(os.path.join(root, "pocFiles.md"), "w") as f:
        for file in files:
            if os.path.splitext(file)[1] in exts:
                path = os.path.join(root.split("./docs")[-1], file)
                line = f"[{file}]({path})\n"
                print(line.strip())
                f.write(line)
                # with open("pocFiles.md", "a") as f:
                #     f.write(os.path.join(root, file) + "\n")

# delete empty pocFiles.md
for root, dirs, files in os.walk("./docs"):
    for file in files:
        if file == "pocFiles.md" and os.path.getsize(os.path.join(root, file)) == 0:
                os.remove(os.path.join(root, file))