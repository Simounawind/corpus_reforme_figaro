from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from xml.etree import ElementTree as ET
import spacy

# 加载 spaCy 的法语模型
nlp = spacy.load("fr_core_news_sm")
# 获取 spaCy 法语停用词列表
stop_words_fr = list(nlp.Defaults.stop_words)
# 添加额外的停用词，如 qu 和 ans 和 texte和lr和 retraite
stop_words_fr.append('qu')
stop_words_fr.append('ans')
stop_words_fr.append('texte')
stop_words_fr.append('lr')
stop_words_fr.append('retraite')

# 重新加载 XML 文件并提取所有文章的内容
file_path = 'corpus.xml'
tree = ET.parse(file_path)
root = tree.getroot()

# 提取所有文章的内容
texts = [article.find('contenu').text for article in root.findall('.//article') if article.find('contenu') is not None]

# 创建 TF-IDF 模型，使用 spaCy 提供的法语停用词
vectorizer = TfidfVectorizer(stop_words=stop_words_fr)
X = vectorizer.fit_transform(texts)

# 计算每个词的平均 TF-IDF 分数
mean_tfidf_scores = np.mean(X, axis=0).A1

# 获取特征名字（即词汇）
features = np.array(vectorizer.get_feature_names_out())

# 对 TF-IDF 分数进行排序并获取前5个关键词
sorted_indices = np.argsort(mean_tfidf_scores)[::-1]
top_keywords = features[sorted_indices[:10]]

print(top_keywords)
