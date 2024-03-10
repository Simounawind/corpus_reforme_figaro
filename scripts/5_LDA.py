import xml.etree.ElementTree as ET
import spacy
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from collections import Counter


file_path = 'corpus.xml'

tree = ET.parse(file_path)
root = tree.getroot()
nlp = spacy.load("fr_core_news_md")
texts = []  

for article in root.findall('.//article') :
    contenu = article.find('contenu')
    if contenu is not None:
        doc = nlp(contenu.text)
        nouns = [token.text for token in doc if token.pos_ == 'NOUN']
        texts.append(' '.join(nouns))

vectorizer = CountVectorizer(max_df=0.95, min_df=2)
dtm = vectorizer.fit_transform(texts) 

lda = LatentDirichletAllocation(n_components=5, random_state=0)
lda.fit(dtm)

for index, topic in enumerate(lda.components_):
    print(f"Top words for topic #{index}")
    print([vectorizer.get_feature_names_out()[i] for i in topic.argsort()[-20:]])
    print("\n")



    # ainsi, c'est une script qui utilise la méthode de LDA pour trouver les thèmes dans un corpus XML.