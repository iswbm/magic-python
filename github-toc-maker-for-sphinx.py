import os
import re
from glob import glob

pwd = os.getcwd()
all_chapters_path = glob(pwd + "/source/c0*")


def get_chapter_name(file):
    with open(file) as f:
        f.readline()
        chapter_name = f.readline().strip()

    return chapter_name

def get_title(file):
    with open(file) as f:
        first_line = f.readline()

    if first_line.startswith("#"):
        return first_line[1:].strip()

def generate_mapping():
    mapping = dict.fromkeys([os.path.basename(chapter_path) for chapter_path in all_chapters_path])
    for key in mapping.keys():
        chapter_file = os.path.join(pwd, "source", "chapters", key.replace("c", "p") + ".rst")
        mapping[key] = get_chapter_name(chapter_file)

    return mapping

def get_toc_info():
    toc = {}
    for dir_path in all_chapters_path:
        dir_name = os.path.basename(dir_path)

        chapter_toc = {}
        files = glob(dir_path + "/*.md")

        for file in files:
            file_name = os.path.basename(file)
            section = int(re.findall(r"c\d{2}_(\d{2}).md", file_name)[0])

            md_path = os.path.join("./source/", dir_name, file_name)
            title = get_title(file)
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
            print("  ", f"* [{post[1][0]}]({post[1][1]})")

def main():
    mapping = generate_mapping()
    toc_info = get_toc_info()
    print_md_toc(toc_info, mapping)

if __name__ == '__main__':
    main()