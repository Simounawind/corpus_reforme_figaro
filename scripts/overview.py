from xml.etree import ElementTree as ET

# 读取上传的 XML 文件
file_path = 'corpus.xml'
tree = ET.parse(file_path)
root = tree.getroot()

# 打印出 XML 的结构以便了解
# 查找所有的 article 元素以确定结构
articles = root.findall('.//article')

# 输出文章数量和第一篇文章的示例结构，包括标签名和部分内容
num_articles = len(articles)
example_structure = {child.tag: child.text[:30] + '...' if child.text else '' for child in articles[0]}

print(num_articles, example_structure)
