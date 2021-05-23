#!/usr/local/bin/python3

import os
import glob
import fileinput
import linecache
from functools import partial

repo_dir = os.getcwd()
source_dir = os.path.join(repo_dir, "source")
all_md_path = os.path.join(repo_dir, "all_v3.0.md",)

count = 0

with open(all_md_path, "w") as all_md:
    write = partial(print, file=all_md, end="")
    os.chdir(source_dir)

    for c_no in sorted(glob.glob("c*")):
        if c_no == "chapters" or c_no == "conf.py":
            continue

        # 读取并记下章节名
        c_name = linecache.getline(os.path.join(source_dir, "chapters", f"{c_no.replace('c', 'p')}.rst"), 2)
        write(f"# {c_name}\n\n", file=all_md)

        # 读取每一节的内容
        all_md_file = sorted(glob.glob(f"{source_dir}/{c_no}/*.md"))
        for line in fileinput.input(all_md_file):
            if "20200804124133" in line or "20200607174235" in line:
                continue

            if fileinput.isfirstline():
                count += 1
                if count%5 == 0:
                    write("![](http://image.iswbm.com/20210523153308.png)", end="\n\n")

            if line.startswith("# "):
                line = line.replace("# ", "## ")
            elif line.startswith("## "):
                line = line.replace("## ", "### ")
            elif line.startswith("### "):
                line = line.replace("### ", "#### ")
            elif "gif" in line:
                line = line.replace("![]", "![该图为GIF,请前往 magic.iswbm.com 浏览]")

            write(line)

