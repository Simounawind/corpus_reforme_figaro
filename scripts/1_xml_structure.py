import os
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString
from datetime import datetime
import re

def parse_document(file_path):
    """
    解析单个文档，返回一个包含文档信息的字典。
    该字典中的内容（contenu）将去除换行符，成为一个长字符串。
    """
    doc = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        doc['titre'] = lines[0].split(maxsplit=1)[1].strip() if len(lines) > 0 else ""
        doc['ddp'] = lines[1].split(maxsplit=1)[1].strip() if len(lines) > 1 else ""
        doc['auteur'] = lines[2].split(maxsplit=1)[1].strip() if len(lines) > 2 else ""
        doc['contenu'] = ""
       # 去除内容中的换行符，并将内容合并为一个长字符串
        contenu = ' '.join(line.strip() for line in lines[3:]).split(maxsplit=1)[1].strip() if len(lines) > 3 else ""
        doc['contenu'] = re.sub(r'\s+', ' ', contenu)

    return doc

def create_document_element(doc, index):
    """
    根据文档内容和索引创建XML元素。
    """
    document = ET.Element("article", index=str(index))
    for key, value in doc.items():
        child = ET.Element(key)
        child.text = value
        document.append(child)
    return document

def docs_to_xml(folder_path):
    """
    遍历指定文件夹内的所有txt文件，将它们转换为XML格式，并保存到一个文件中。
    文档将根据发布日期排序。
    """
    documents = []
    
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            file_path = os.path.join(folder_path, file_name)
            doc = parse_document(file_path)
            documents.append(doc)
    
    # 按照日期排序文档
    documents.sort(key=lambda x: datetime.strptime(x['ddp'], "%Y-%m-%d"))
    
    root = ET.Element("corpus")
    for index, doc in enumerate(documents, start=1):
        document_element = create_document_element(doc, index)
        root.append(document_element)
    
    tree = ET.ElementTree(root)
    xml_str = ET.tostring(tree.getroot(), 'utf-8')
    pretty_xml_as_string = parseString(xml_str).toprettyxml(indent="    ")
    
    with open("news_documents.xml", "w", encoding="utf-8") as f:
        f.write(pretty_xml_as_string)


folder_path = "structured_corpus"
docs_to_xml(folder_path)
