#本脚本用来读取一个csv文件中的a 和 b 列，然后统计 a 列中的每个元素的出现次数，并打印出来前10个出现次数最多的元素
# 同时 统计 b 列中的每个元素的出现次数，并打印出来前10个出现次数最多的元素。

import csv
from collections import Counter

# 读取csv文件
with open('uppppp.csv', 'r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # 跳过标题行
    # 读取a列和b列
    a_column = [row[3] for row in reader]
    file.seek(0)
    next(reader)  # 跳过标题行
    b_column = [row[4] for row in reader]

# 统计a列中每个元素的出现次数
a_counter = Counter(a_column)
print("a列中每个元素的出现次数:")
for word, count in a_counter.most_common(10):
    print(f"{word}: {count}")

# 统计b列中每个元素的出现次数
b_counter = Counter(b_column)
print("\nb列中每个元素的出现次数:")
for word, count in b_counter.most_common(10):
    print(f"{word}: {count}")


# 将完整的结果保存到csv文件中,a 列和 b 列的统计结果分别保存在 2 列中
with open('uppppp.csv', 'r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    rows = list(reader)
    header = rows[0]
    a_column = [row[3] for row in rows[1:]]
    b_column = [row[4] for row in rows[1:]]