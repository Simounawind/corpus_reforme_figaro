import xml.etree.ElementTree as ET
import re
import csv

def extract_citations(text):
    """
    Extraire les citations d'un texte.
    """
    pattern = r'«(.*?)»'
    return re.findall(pattern, text)

def main(xml_file_path, csv_file_path):
    """
    Extraire les citations de chaque article dans le fichier XML et les écrire dans un fichier CSV.
    """
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    # Créer une liste pour stocker les citations
    citations = []

    # Parcourir tous les articles
    for article in root.findall('article'):
        doc_id = article.get('index')  # Récupérer l'ID du document
        content = article.find('contenu').text  # Récupérer le contenu de l'article
        if content:
            for citation in extract_citations(content):
                citations.append([doc_id, citation])

    # Écrire les citations dans un fichier CSV
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Document ID', 'Citation Text'])
        for citation in citations:
            writer.writerow(citation)

if __name__ == "__main__":
    xml_file_path = 'corpus.xml'
    csv_file_path = 'citation_searched.csv'
    main(xml_file_path, csv_file_path)



