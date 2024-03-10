import xml.etree.ElementTree as ET

# 加载XML文件
tree = ET.parse('corpus_metaphore.xml')
root = tree.getroot()

# 计算<sisd>标签的数量
guerre_count = len(root.findall('.//guerre'))

voyage_count = len(root.findall('.//voyage'))
maladie_count = len(root.findall('.//maladie'))
jeu_count = len(root.findall('.//jeu'))
catas_count = len(root.findall('.//catas'))

print(f"Number of <guerre_count> tags: {guerre_count}")
print(f"Number of <voyage_count> tags: {voyage_count}")
print(f"Number of <maladie_count> tags: {maladie_count}")
print(f"Number of <jeu_count> tags: {jeu_count}") 
print(f"Number of <catas_count> tags: {catas_count}")

# c'est une script qui compte le nombre de balises <sisd> dans un fichier XML.