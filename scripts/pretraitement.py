import spacy
from spacy.tokens import Span
from xml.etree import ElementTree as ET

# 加载法语模型
nlp = spacy.load("fr_core_news_md")

import xml.etree.ElementTree as ET
import re

# 加载并解析XML文件
tree = ET.parse('/mnt/data/corpus.xml')
root = tree.getroot()

# 遍历XML文件，找到所有的'contenu'标签
for contenu in root.findall('.//contenu'):
    text = contenu.text
    
    # 预处理步骤
    # 示例：去除HTML标签
    text = re.sub(r'<[^>]+>', '', text)
    
    # 示例：替换特殊字符
    text = text.replace('&nbsp;', ' ').replace('&amp;', '&')
    
    # 示例：去除额外的空格
    text = re.sub(r'\s+', ' ', text).strip()
    
    # 处理后的文本
    print(text)

# 注意：这里只是打印处理后的文本，实际应用中你可能需要将它们保存到文件或进行进一步的处理。
