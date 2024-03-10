# Description: Trouver les co-occurrences les plus fréquentes d'un mot cible dans un corpus
import xml.etree.ElementTree as ET
import re
from collections import Counter

# Charger le fichier XML
tree = ET.parse('neeee_corpus.xml')
root = tree.getroot()

# Créer une liste pour stocker tous les textes
all_texts = []

# Récupérer tous les textes des articles
for contenu in root.findall('.//contenu'):
    text = contenu.text
    if text:
        # Supprimer les balises HTML
        text = re.sub(r'<[^>]+>', '', text)
        all_texts.append(text)

# Définir le mot cible et la taille de la fenêtre
target_word = 'réforme'
window_size = 5
co_occurrences = Counter()

for text in all_texts:
    # Diviser le texte en tokens
    tokens = text.split()
    
    # Parcourir les tokens
    for i, token in enumerate(tokens):
        if token == target_word:
            # Récupérer le contexte
            start = max(0, i - window_size)
            end = min(len(tokens), i + window_size + 1)
            context = tokens[start:i] + tokens[i+1:end]
            
            # Mettre à jour le compteur de co-occurrences
            co_occurrences.update(context)

# Récupérer les 20 co-occurrences les plus fréquentes
most_common_co_occurrences = co_occurrences.most_common(20)

for word, count in most_common_co_occurrences:
    print(f"{word}: {count}")
