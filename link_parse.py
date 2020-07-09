import requests
from bs4 import BeautifulSoup

lst=['https://www.ncbi.nlm.nih.gov/pubmed/8303295',
     'https://www.ncbi.nlm.nih.gov/pubmed/16590258',
     'https://www.ncbi.nlm.nih.gov/pubmed/13054692',
     'https://www.ncbi.nlm.nih.gov/pubmed/1701568',
     'https://www.ncbi.nlm.nih.gov/pubmed/8004676',
     'https://www.ncbi.nlm.nih.gov/pubmed/?term=Wolves%2C+Moose%2C+and+Tree+Rings+on+Isle+Royale.',
'https://www.ncbi.nlm.nih.gov/pubmed/?term=Lateral+Transfer+of+Genes+from+Fungi+Underlies+Carotenoid+Production+in+Aphids.',
'https://www.ncbi.nlm.nih.gov/pubmed/?term=Contingency+and+Determinism+in+Replicated+Adaptive+Radiations+of+Island+Lizards.',
'https://www.ncbi.nlm.nih.gov/pubmed/2704419',
'https://www.ncbi.nlm.nih.gov/pubmed/9794762',
'https://www.ncbi.nlm.nih.gov/pubmed/?term=An+Expressed+Fgf4+Retrogene+Is+Associated+with+Breed-Defining+Chondrodysplasia+in+Domestic+Dogs.',
'https://www.cell.com/fulltext/0092-8674(86)90665-3',
'https://www.nejm.org/doi/full/10.1056/NEJM200002243420801',
'https://science.sciencemag.org/content/318/5853/1108',
'https://science.sciencemag.org/content/309/5734/630',
# 'https://academic.oup.com/jtm/advance-article/doi/10.1093/jtm/taaa037/5808003',
# 'https://www.ajronline.org/doi/full/10.2214/AJR.20.22961',
'https://www.eurosurveillance.org/content/10.2807/1560-7917.ES.2020.25.11.2000258',
'https://www.nature.com/articles/s41579-018-0118-9'
     ]

for i in lst:

  result=requests.get(i)
  src=result.content
  soup= BeautifulSoup(src,'lxml')
  match=soup.find('div',class_='abstract')
  if(match!=None):
    index=match.text.find('Abstract')
    m=match.text[index+9:]

    abstract='Abstract|'+m.strip()
  else:
    abstract=""
  # print(abstract)
  heading=soup.find('h1')
  head=heading.text.strip()
  print(head)
  print(abstract)
  print('\n')
