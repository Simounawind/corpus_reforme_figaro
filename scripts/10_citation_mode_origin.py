import re
import xml.etree.ElementTree as ET
import csv
import os
import json
from openai import OpenAI



tree = ET.parse('corpus.xml')
root = tree.getroot()
def extract_citations_with_context(text):
    pattern = r'(.{0,100})«(.*?)»(.{0,100})'
    return re.findall(pattern, text)

nested_citation_lists = []

for article in root.findall('article'):
    doc_id = article.get('index')  # Document ID from the index attribute
    content = article.find('contenu').text  # Assuming the citations are in <contenu>
    article_citations = []
    if content:
        for before_citation, citation, after_citation in extract_citations_with_context(content):
            full_citation_text = f"{before_citation}《{citation}》{after_citation}".strip()
            article_citations.append(full_citation_text)  
    nested_citation_lists.append((doc_id, article_citations))





os.environ["OPENAI_API_KEY"] = '************************************'

client = OpenAI()

def gpt_determine_source(text):
    """
    """
    # 构造请求所需的JSON字符串
    texts_json_str = json.dumps(text)

    # 发送请求到OpenAI
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Given the text, identify the source of the citation only based on the content.  The citation is the text in « », and you should check its source before and after the citation to verify the source. If the source is a person or someone, return the name, without saying anything. If it is from a certain person without it's name, just give me the description of the person. You must work hard and not be lazy."},
            {"role": "user", "content": texts_json_str}
        ],
        temperature=0.3
    )

    # 解析响应并提取数据
    data = completion.model_dump_json(indent=2)
    json_data = json.loads(data)

    # 假设输出格式是我们期望的格式，提取和返回源信息
    # 注意：根据实际的API响应结构，这里的路径可能需要调整
    source = json_data.get('choices', [])[0].get('message', {}).get('content', '')
    return source






with open('citation_sources.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Document ID', 'Citation', 'Source'])

    # 遍历每篇文章的引用列表
    for doc_id, citations in nested_citation_lists:
        for citation in citations:
            # 使用GPT判断引用的源泉
            source = gpt_determine_source(citation)
            # 将结果写入CSV文件
            writer.writerow([doc_id, citation, source])


