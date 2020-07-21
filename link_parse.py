import requests
from bs4 import BeautifulSoup


cell=['https://www.cell.com/fulltext/0092-8674(86)90665-3','https://www.cell.com/immunity/fulltext/S1074-7613(20)30170-9']
nejm=['https://www.nejm.org/doi/full/10.1056/NEJM200002243420801','http://www.nejm.org/doi/10.1056/NEJMc2004973','https://www.nejm.org/doi/full/10.1056/NEJMc2011400',
      
 'https://www.nejm.org/doi/full/10.1056/NEJMoa2016638' ]


ncbi=['https://www.ncbi.nlm.nih.gov/pubmed/8303295',
      'https://www.ncbi.nlm.nih.gov/pubmed/16590258',
'https://www.ncbi.nlm.nih.gov/pubmed/13054692',
'https://www.ncbi.nlm.nih.gov/pubmed/1701568',
'https://www.ncbi.nlm.nih.gov/pubmed/8004676',
'https://www.ncbi.nlm.nih.gov/pubmed/?term=Wolves%2C+Moose%2C+and+Tree+Rings+on+Isle+Royale.',
'https://www.ncbi.nlm.nih.gov/pubmed/?term=Lateral+Transfer+of+Genes+from+Fungi+Underlies+Carotenoid+Production+in+Aphids.',
'https://www.ncbi.nlm.nih.gov/pubmed/?term=Contingency+and+Determinism+in+Replicated+Adaptive+Radiations+of+Island+Lizards.',
'https://www.ncbi.nlm.nih.gov/pubmed/2704419',
'https://www.ncbi.nlm.nih.gov/pubmed/9794762',
      
      
      
      
      
      
      
      'https://www.ncbi.nlm.nih.gov/pubmed/8303295','https://www.ncbi.nlm.nih.gov/pubmed/16590258','https://www.ncbi.nlm.nih.gov/pubmed/13054692',
      'https://www.ncbi.nlm.nih.gov/pubmed/1701568','https://www.ncbi.nlm.nih.gov/pubmed/8004676','https://pubmed.ncbi.nlm.nih.gov/32275812/',
      'https://pubmed.ncbi.nlm.nih.gov/32081636/','https://www.ncbi.nlm.nih.gov/pubmed/?term=Wolves%2C+Moose%2C+and+Tree+Rings+on+Isle+Royale',
      'https://www.ncbi.nlm.nih.gov/pubmed/?term=Lateral+Transfer+of+Genes+from+Fungi+Underlies+Carotenoid+Production+in+Aphids.'
      
      
      
      ]  
pmc=['https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5052149/','https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3797217/pdf/nihms482109.pdf',
     'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7048352/pdf/OAMJMS-7-3733.pdf',
     'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5588700/pdf/nihms867337.pdf',
     'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7162776/',
     'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2546865/',
     'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5467610/',
     'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3056401/',
     'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6109018/pdf/11606_2018_Article_4462.pdf',
     'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6509028/pdf/191e505.pdf',
     'https://www.ncbi.nlm.nih.gov/pmc/articles/pmid/25849572/',
     'https://www.ncbi.nlm.nih.gov/pmc/articles/pmid/22401530/',
     'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7219423/pdf/main.pdf',
     'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5201116/',
     'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5447185/pdf/SaudiMedJ-38-344.pdf',
     
     
     
     
     ]



def cell_extract():
  """Returns a list of extract from cell articles """
  dicti={}
  listi=[]
  for i in cell:
    result=requests.get(i)
    src=result.content
    soup= BeautifulSoup(src,'lxml')
    match1=soup.find_all(class_='sectionTitle')
    match=soup.find_all('div',class_='section-paragraph')
    # match=soup.find_all('section')
    if(match1==[]):

      dicti['Abstract:']=(match[0].text)
      listi.append(dicti)

    else:
      dicti={}
      for j in range(len(match1)):
        
        dicti[(match1[j].text)]=(match[j].text)
      listi.append(dicti)

  
  return listi

def ncbi_pubmed_extract():
  """ Gets the abstracts """
  listi=[]
  for i in ncbi:
    dicti={}
    result=requests.get(i)
    src=result.content
    soup= BeautifulSoup(src,'lxml')
    match=soup.find_all('div',class_='abstract-content selected')
    for j in match:
      dicti['Abstract']=(j.text.strip())
    listi.append(dicti)
  return listi
      

def njem_extract():
  """Extracts njem articles """
  listi=[]
  for i in nejm:
    dicti={}
    result = requests.get(i)
    src = result.text
    soup = BeautifulSoup(src, 'lxml')
    match=soup.find_all('section',class_='o-article-body__section')
    for i in match[:5]:
      k=len((i.text.split()[0]))
      dicti[(i.text.split()[0])]=i.text[k+1:].strip()
    
      if 'Abstract' not in dicti.keys():
        match2=soup.find_all('p',class_='f-body')
        dicti={}
        s=""
        for i in match2:
          s+=i.text
        dicti['Abstract']=s
    listi.append(dicti)
  return listi


def pmc_extract():
  listi=[]
  m=['Abstract','Introduction']
  for i in pmc:
    dicti={}
    result = requests.get(i)
    src = result.text
    soup = BeautifulSoup(src, 'lxml')

    match = soup.find_all('div',class_="tsec sec")
    match2=soup.find_all('h2',class_='head no_bottom_margin')
    for j in range(len(match[:4])):
      key=len(match2[j].text)
      
      dicti[(match2[j].text)]=(match[j].text[key:])
    listi.append(dicti)
      
      
  
  return listi

def scimag():
  for i in sci_direct:
    result=requests.get(i)
    src = result.text
    soup=BeautifulSoup(src, 'lxml')


    match = soup.find_all('div',class_='section abstract')
    match2 = soup.find_all('div',class_='section discussion')
    match3 = soup.find_all('div',class_='section conclusions')
   
    for j in match:
      print(j.text)
    for k in match2:
      print(k.text)

    for f in match3:
      print(f.text)

    
def medrxiv():
  """Takes in a list of medrxiv links and retruns a list of dictionaries"""
  for j in medrxiva:
    result=requests.get(j)
    src = result.text
    soup=BeautifulSoup(src, 'lxml')


    match = soup.find_all('div',class_='section abstract')
    
    for i in match:
      print(i.text)
      print('\n')


def scrape_nature():
  listi=[]
  for j in nature:
    dicti={}
    result=requests.get(j)
    src = result.text
    soup=BeautifulSoup(src, 'lxml')
    match2 = soup.find_all('h2',class_='c-article-section__title')
    match = soup.find_all('div',class_='c-article-section')
    
    for i in range(len(match2)):
      key=(match2[i].text)
      l=len(key)
      dicti[key]=(match[i].text[l:])
    listi.append(dicti)
  return listi



