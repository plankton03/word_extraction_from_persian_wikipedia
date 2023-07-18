import requests
import bz2
import xml.etree.ElementTree as ET
import re

def download_xml_bz2(url):
    response = requests.get(url)
    with open('fawiki-latest-pages-articles.xml.bz2', 'wb') as f:
        f.write(response.content)

def extract_text_from_xml_bz2(xml_bz2_path):
    with bz2.open(xml_bz2_path, 'rt', encoding='utf-8') as xml_file:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        extracted_text = []

        def extract_text_recursive(element):
            if element.text:
                extracted_text.append(element.text.strip())
            for child in element:
                extract_text_recursive(child)

        extract_text_recursive(root)

        return '\n'.join(extracted_text)

def count_words(text):
    words = re.findall(r'\b\w+\b', text)
    return len(words)

if __name__ == "__main__":
    # test url
    url = 'https://dumps.wikimedia.org/fawiki/20230701/fawiki-20230701-flow.xml.bz2'
    
    # wanted url
    # url = 'https://dumps.wikimedia.org/fawiki/latest/fawiki-latest-pages-articles.xml.bz2'

    download_xml_bz2(url)

    xml_bz2_path = 'fawiki.xml.bz2'

    extracted_text = extract_text_from_xml_bz2(xml_bz2_path)

    word_count = count_words(extracted_text)
    print("Number of words in the dataset:", word_count)
