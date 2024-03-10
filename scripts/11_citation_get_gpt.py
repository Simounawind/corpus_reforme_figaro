import csv
import os
import json
from openai import OpenAI

# 加载CSV文件
def load_csv(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader, None)  # Skip header row
        data = [row for row in reader]
    return headers, data

# 设置OpenAI API密钥环境变量
os.environ["OPENAI_API_KEY"] = 'sk-xxxxxx'

client = OpenAI()


def gpt_determine_source(citation, context):
    # 构造请求所需的JSON字符串
    message = f"Citation: {citation}\nContext: {context}"
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Given the text, identify the source of the reference in the text. Below, I will provide specific citation along with their surrounding text (context) where the reference is embedded. Based on the provided citation and its context, I need you to help me identify the correct source of the reference. This may include the name of a person, an institution, or a description of the subject matter referenced. The citation is the text in «», and you should check its source before and after the citation to verify the source. Whether the source is a person or a group or someone, return the name without saying anything.  You must work hard and not be lazy."},
            {"role": "system", "content": '''Citation: "[Specific citation here]"
Context: "[The surrounding text where the citation is found]"
Example Citation: "d’aller jusqu’à l’âge légal. Pour eux, la durée de cotisation acquise doit primer sur l’âge légal."
Example Context: "Dès lors, pour LR, «à cette heure, le compte n’y est pas» encore, fait valoir Éric Ciotti. «Je serai très attentif à la question de l’emploi des seniors et des carrières hachées sur l’âge légal.»"'''},

            {"role": "user", "content": message}
        ],
        temperature=0.4
    )
    try:
        # 尝试直接访问content属性
        source = completion.choices[0].message.content
    except AttributeError:
        # 如果上述方法失败，尝试其他可能的属性访问方法
        source = "Error: Unable to extract source information."

    return source.strip()

# 修改后的更新CSV文件函数
def update_csv_with_sources(input_file_path, output_file_path):
    headers, data = load_csv(input_file_path)
    
    with open(output_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers + ['Source'])  # Add new column header for source
        
        for row in data:
            doc_id, citation, context = row
            source = gpt_determine_source(citation, context)
            updated_row = row + [source]
            writer.writerow(updated_row)  # 写入每一行更新后的数据

if __name__ == "__main__":
    input_csv_path = 'citations.csv'  # Input CSV file path
    output_csv_path = 'updated_citations.csv'  # Output CSV file path with sources
    update_csv_with_sources(input_csv_path, output_csv_path)