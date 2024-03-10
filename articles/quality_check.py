import os
from datetime import datetime

def check_date(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')  # 这会自动处理每月天数和闰年
        return True
    except ValueError:
        return False

def check_author(author_str):
    authors = author_str.split(', ')
    for author in authors:
        parts = author.split()
        if not (2 <= len(parts) <= 3):  # 名字由两部分或三部分组成
            return False
    return True

def validate_files(folder_path):
    issues = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            try:
                with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                    date_str = lines[1].split('\t')[1].strip()
                    author_str = lines[2].split('\t')[1].strip()

                    if not check_date(date_str):
                        issues.append((filename, 'Invalid Date'))
                    if not check_author(author_str):
                        issues.append((filename, 'Invalid Author Format'))

            except UnicodeDecodeError:
                issues.append((filename, 'Encoding Issue'))

    return issues

folder_path = '/Users/xiaohua/Desktop/毕业/Blcu/毕业论文/corpus/structured_corpus'
issues = validate_files(folder_path)
for filename, issue in issues:
    print(f"File: {filename}, Issue: {issue}")
