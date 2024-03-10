# extrait les concordances d'un mot dans un fichier XML et les sauvegarde dans un fichier CSV
import xml.etree.ElementTree as ET
import spacy
import pandas as pd
import csv

nlp = spacy.load("fr_core_news_sm")

def extract_contexts(xml_file_path, target_word, window_size=20):
    tree = ET.parse(xml_file_path)
    root = tree.getroot()
    
    contexts = []  
    for contenu in root.findall('.//contenu'):
        text = contenu.text
        if text:
            doc = nlp(text)
            tokens = [token.text for token in doc]  
            for i, word in enumerate(tokens):
                if word.lower() == target_word.lower():
                    start = max(i - window_size, 0)
                    end = min(i + window_size + 1, len(tokens))
                    before = ' '.join(tokens[start:i])
                    after = ' '.join(tokens[i+1:end])
                    contexts.append((before, word, after))
    return contexts

def print_contexts(contexts):
    for i, (before, word, after) in enumerate(contexts[:30], 1):
        print(f"{i}. \nTexte avant: {before}\nMot: {word}\nTexte après: {after}\n")

def save_contexts_to_csv(contexts, csv_file_path):
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Index", "Texte précédent", "Mot", "Texte suivant"])
        for i, context in enumerate(contexts, 1):
            writer.writerow([i] + list(context))

xml_file_path = 'corpus.xml'
csv_file_path = 'concordances_resultats/conc_guerre.csv'

contexts = extract_contexts(xml_file_path, 'guerre')
print_contexts(contexts)
save_contexts_to_csv(contexts, csv_file_path)
