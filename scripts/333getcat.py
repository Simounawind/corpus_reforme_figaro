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


def gpt_determine_source(ress, context):
    # 构造请求所需的JSON字符串
    message = f"Citation: {ress}\nContext: {context}"
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a text source classifier. You are given 1. the text 2. the source of the reference in the text. The source needs to be classified into 5 categories: 'Social Institution', 'Media', 'Government and Legislative Bodies', 'People', 'Political Party', and 'Syndicate'. Based on the information and your knowledge, you should tell me what kind of source it is. You can only choose from the choices given, without saying anything else. You must work hard and not be lazy."},
            {"role": "system", "content": "If it's a Name, you should use your knowledge to see if he/she is related to a certain domain, like Emmanuel Macron or Elisabeth Borne and else is certainly to be the 'gouverment' categoriy. If it involves research institutions and think tanks, then classify it as 'Social Institution'; if it involves news outlets, magazines, or online media platforms, then classify it as 'Media'; if the source is from official government documents, legislation, or policy analysis reports, then classify it as 'Government and Legislative Bodies'; if the source is an individual ordinary, like a teacher, a salary, a civilain, classify it as 'People'; if the source is related to a political movement or organization aiming at influencing public policy or government, classify it as 'Political Party'; if the source is from unions or worker organizations focusing on labor rights and interests, classify it as 'Syndicate'."},


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
        writer.writerow(headers + ['categorie'])  # Add new column header for source
        
        for row in data:
            doc_id, citation, context,ress = row
            cat = gpt_determine_source(ress, context)
            updated_row = row + [cat]
            writer.writerow(updated_row)  # 写入每一行更新后的数据

if __name__ == "__main__":
    input_csv_path = 'final_citations.csv'  # Input CSV file path
    output_csv_path = 'uppppp.csv'  # Output CSV file path with sources
    update_csv_with_sources(input_csv_path, output_csv_path)