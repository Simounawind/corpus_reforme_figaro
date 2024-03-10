import os
from collections import defaultdict

def is_duplicate(title):
    words = title.lower().split()
    for i in range(len(words) - 1):
        if words[i] == words[i + 1]:
            return True
    return False

def find_duplicate_files(folder_path):
    titles = defaultdict(list)
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
                first_line = file.readline()
                title = first_line.split('\t')[1]  # 假设标题在第二列
                titles[title.strip().lower()].append(filename)

    duplicate_files = {title: filenames for title, filenames in titles.items() if len(filenames) > 1 or is_duplicate(title)}
    return duplicate_files


folder_path = '/Users/xiaohua/Desktop/毕业/Blcu/毕业论文/corpus/structured_corpus'
duplicate_files = find_duplicate_files(folder_path)
for title, files in duplicate_files.items():
    print(f"Title: '{title}' has duplicates in files: {files}")

