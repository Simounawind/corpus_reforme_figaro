# c'est une script qui extrait les concordances d'un mot dans un fichier XML et les sauvegarde dans un fichier CSV.
import xml.etree.ElementTree as ET
import spacy
from collections import Counter
import csv

nlp = spacy.load("fr_core_news_sm")
def extract_cooccurrences_with_context(xml_file_path, target_word, window_size=5):
    tree = ET.parse(xml_file_path)
    root = tree.getroot()
    
    occurrences_with_context = []  
    for contenu in root.findall('.//contenu'):
        text = contenu.text
        if text:
            doc = nlp(text)
            tokens = [token.text for token in doc] 
            for i, word in enumerate(tokens):
                if word.lower() == target_word.lower():
                    start = max(i - window_size, 0)
                    end = min(i + window_size + 1, len(tokens))
                    before_context = tokens[start:i]
                    after_context = tokens[i+1:end]
                    occurrences_with_context.append((
                        " ".join(before_context),
                        word,
                        " ".join(after_context)
                    ))
    
    return occurrences_with_context

def save_cooccurrences_context_to_csv(occurrences_with_context, csv_file_path):
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["mots avant", "mon central", "mots après"])
        for before_context, word, after_context in occurrences_with_context:
            writer.writerow([before_context, word, after_context])


xml_file_path = 'cleaned_corpus.xml'
csv_file_path = 'cooccurrences_forre.csv'

occurrences_with_context = extract_cooccurrences_with_context(xml_file_path, 'réforme')
save_cooccurrences_context_to_csv(occurrences_with_context, csv_file_path)



