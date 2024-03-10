import xml.etree.ElementTree as ET
import spacy
from collections import Counter
import pandas as pd





# Spécifier le chemin du fichier XML
file_path = '../corpus.xml'

# Charger le fichier XML
tree = ET.parse(file_path)
root = tree.getroot()

# combiner tous les textes des articles en un seul texte
combined_text = " ".join(article.find('contenu').text for article in root.findall('.//article') if article.find('contenu') is not None)

# Charger le modèle de langue française de spaCy
nlp = spacy.load("fr_core_news_sm")

custom_stop_words = list(nlp.Defaults.stop_words) + ['être', 'faire', 'il','falloir','pouvoir','vouloir','-t']
for word in custom_stop_words:
    nlp.vocab[word].is_stop = True


# Définir une fonction pour traiter le texte
def process_text(text):
    doc = nlp(text.lower())
    tokens = []
    for token in doc:
        # Filtrer les stopwords, la ponctuation, les espaces et les nombres
        if not token.is_stop and not token.is_punct and not token.is_space and not token.like_num:
            # lemmatisation
            lemma = token.lemma_
            # Filtrer les mots vides personnalisés
            if lemma not in custom_stop_words:
                tokens.append(lemma)
    return tokens

def get_top_n_words(text, n=30):
    # Traiter le texte
    tokens = process_text(text)
    # Compter la fréquence de chaque mot
    word_freq = Counter(tokens)
    # Récupérer les n mots les plus fréquents
    top_n_words = word_freq.most_common(n)
    return top_n_words


# Récupérer les 30 mots les plus fréquents
top_30_words = get_top_n_words(combined_text, 600)

# Garder les mots et leurs fréquences dans un DataFrame

# Créer un DataFrame à partir des données
df = pd.DataFrame(top_30_words, columns=['Word', 'Frequency'])

# Spécifier le chemin du fichier de sortie
output_file_path = 'top_words_frequency.csv' 

# Enregistrer le DataFrame dans un fichier CSV
df.to_csv(output_file_path, index=False)

print(f"Les 30 mots les plus fréquents ont été enregistrés dans le fichier {output_file_path}.")