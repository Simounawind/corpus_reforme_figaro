import re
from xml.etree import ElementTree as ET

# 读取上传的 XML 文件
file_path = 'corpus.xml'
tree = ET.parse(file_path)
root = tree.getroot()

# 打印出 XML 的结构以便了解
# 查找所有的 article 元素以确定结构
articles = root.findall('.//article')


# 初始化计数器
total_tokens = 0
total_words = 0

# 正则表达式，用于匹配只包含字母的词
word_pattern = re.compile(r'\b[a-zA-ZÀ-ÿ]+\'?[a-zA-ZÀ-ÿ]*\b')

# 更新：Token 定义包括任何分隔的单元，包括标点和数字
token_pattern = re.compile(r'\b[\w\'-]+\b')

for article in articles:
    # 获取文章内容
    content = article.find('contenu').text if article.find('contenu') is not None else ""
    
    # 重新计算 tokens 和 words
    tokens = token_pattern.findall(content)
    words = word_pattern.findall(content)
    
    # 更新总计数
    total_tokens += len(tokens)
    total_words += len(words)
    
print(total_tokens, total_words)

