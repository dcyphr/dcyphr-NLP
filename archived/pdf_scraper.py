import requests
from crossref.restful import Works
import xml.etree.ElementTree as ElementTree
from bs4 import BeautifulSoup
import re

def get_pmid(doi):
    works = Works()
    output = works.doi(doi)
    if output == None:
        return "Not available"
    return output

def get_titles(pmid):
    base_url = "https://www.ncbi.nlm.nih.gov/pmc/oai/oai.cgi?verb=GetRecord&identifier=oai:pubmedcentral.nih.gov:{}&metadataPrefix=pmc"

    r = requests.get(url=base_url.format(7264580))
    root = ElementTree.fromstring(r.content)

    for child in root.iter("{https://jats.nlm.nih.gov/ns/archiving/1.2/}sec"):
        if 'sec-type' in child.keys():
            for title in child.findall('{https://jats.nlm.nih.gov/ns/archiving/1.2/}title'):
                print(title.text)

def scrape_html(link="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7264580/"):
    r = requests.get(url=link)
    soup = BeautifulSoup(r.content, 'html.parser')
    to_remove = soup.find_all(["a", "em", "span"]) 
    for element in to_remove:
        element.extract()
    new_text = re.sub(r', ,', '', str(soup.find_all('p', {'id' : re.compile('^')})))
    new_text = re.sub(r'<[^>]*>', '', new_text)[1:-1]
    return new_text

print(scrape_html())

