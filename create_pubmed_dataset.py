import requests
import os
from Bio import Entrez

def search(query):
    Entrez.email = 'mc2259@cornell.edu'
    handle = Entrez.esearch(db='pubmed', 
                            sort='relevance', 
                            retmax='20',
                            retmode='xml',
                            term=query)
    results = Entrez.read(handle)
    return results

def fetch_details(id_list):
    ids = ','.join(id_list)
    Entrez.email = 'mc2259@cornell.edu'
    handle = Entrez.efetch(db='pubmed',
                           retmode='xml',
                           id=ids)
    results = Entrez.read(handle)
    return results

def fetch_summaries(id_list):
    ids = ','.join(id_list)
    Entrez.email = 'mc2259@cornell.edu'
    handle = Entrez.esummary(db='pubmed',
                           retmode='xml',
                           id=ids)
    results = Entrez.read(handle)
    return results

import json
results = search('fever') # or any query you like
id_list = results['IdList'] # list of UIDs
papers = fetch_details(id_list)
for i in range(len(papers)):
  print(papers['PubmedArticle'][i]['MedlineCitation']['Article']['Abstract']['AbstractText'][0])
  print('\n')
