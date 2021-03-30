import os
import re
import linecache
from glob import glob

pwd = os.getcwd()
source_dir = os.path.join(pwd, "source")

def get_chapter_name(file):
    return linecache.getline(file, 2).strip()

def get_title(file):
    first_line = linecache.getline(file, 1)

    if first_line.startswith("#"):
        return first_line.strip()

def get_all_chapter():
    all_chapters_path = []
    os.chdir(source_dir)
    for dir_name in glob("c*"):
        if dir_name == "chapters" or dir_name == "conf.py":
            continue
        all_chapters_path.append(os.path.join(dir_name))

    return all_chapters_path

def generate_mapping(all_chapters_path):
    mapping = dict.fromkeys([os.path.basename(chapter_path) for chapter_path in all_chapters_path])
    for key in mapping.keys():
        chapter_file = os.path.join(pwd, "source", "chapters", key.replace("c", "p") + ".rst")
        mapping[key] = get_chapter_name(chapter_file)

    return mapping

def get_toc_info(all_chapters_path):
    toc = {}
    for dir_name in all_chapters_path:
        chapter_toc = {}
        os.chdir(os.path.join(source_dir, dir_name))

        for file_name in sorted(glob(dir_name + "*.md")):
            section = int(re.findall(r"c\d{2}_(\d{2}).md", file_name)[0])

            md_path = os.path.join("http://pycharm.iswbm.com/zh_CN/latest/", dir_name, file_name.replace("md", "html"))
            title = get_title(file_name)
            if not title:
                continue

            chapter_toc[section] = (title, md_path)

        toc[dir_name] = chapter_toc

    return toc

def print_md_toc(toc_info, mapping):
    for chapter in sorted(toc_info.items(), key=lambda item: item[0]):
        posts = chapter[1]
        chapter_name = mapping[chapter[0]]
        print(f"- **{chapter_name}**")
        for post in sorted(posts.items(), key=lambda item:item[0]):
            # print title only 
            # print(f"{post[1][0]}")
            print("  ", f"* [{post[1][0]}]({post[1][1]})")

def main():
    all_chapter = get_all_chapter()
    mapping = generate_mapping(all_chapter)
    toc_info = get_toc_info(all_chapter)
    print_md_toc(toc_info, mapping)

if __name__ == '__main__':
    main()

