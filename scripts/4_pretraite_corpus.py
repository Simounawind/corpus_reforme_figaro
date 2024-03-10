# Description: C'est un script pour prétraiter un corpus XML en utilisant spaCy pour le traitement du texte.
import xml.etree.ElementTree as ET
import spacy

# Charger le modèle de langue française de spaCy
nlp = spacy.load("fr_core_news_sm")

# Ajouter des mots vides personnalisés
custom_stop_words = list(nlp.Defaults.stop_words) + ['être', 'faire', 'il', 'falloir', 'pouvoir', 'vouloir', '-t']
for word in custom_stop_words:
    nlp.vocab[word].is_stop = True

# Définir une fonction pour traiter le texte
def process_text(text):
    doc = nlp(text.lower())
    tokens = []
    for token in doc:
        if not token.is_stop and not token.is_punct and not token.is_space and not token.like_num:
            lemma = token.lemma_
            if lemma not in custom_stop_words:
                tokens.append(lemma)
    return " ".join(tokens)

#  charger le fichier XML
file_path = 'corpus.xml'  
tree = ET.parse(file_path)
root = tree.getroot()


new_root = ET.Element("root")
for article in root.findall('.//article'):
    new_article = ET.SubElement(new_root, "article")
    for child in article:
        if child.tag != 'contenu':
            new_article.append(child)    
    contenu = article.find('contenu')
    if contenu is not None:
        processed_text = process_text(contenu.text)
        new_contenu = ET.SubElement(new_article, "contenu")
        new_contenu.text = processed_text

new_tree = ET.ElementTree(new_root)
new_file_path = 'pretraite_corpus.xml'
new_tree.write(new_file_path, encoding="utf-8", xml_declaration=True)
