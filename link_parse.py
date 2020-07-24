import requests
from bs4 import BeautifulSoup
def lancet(lancetlink):
  """Takes a lancet link and returns a dictionary"""
  dicti={}
  result=requests.get(lancetlink)
  src=result.text
  soup=BeautifulSoup(src,'lxml')
  head=soup.find_all('h3')[:5]
  para=soup.find_all('div',class_='section-paragraph')[:5]

  for i in range(len(head)):
    dicti[(head[i].text)]=(para[i].text)
  return dicti

def cell_extract(link):
  """Returns a list of extract from cell articles """
  dicti={}
  
 
  result=requests.get(link)
  src=result.content
  soup= BeautifulSoup(src,'lxml')
  match1=soup.find_all(class_='sectionTitle')
  match=soup.find_all('div',class_='section-paragraph')
  # match=soup.find_all('section')
  if(match1==[]):
    dicti['Abstract:']=(match[0].text)
    

  else:
    dicti={}
    for j in range(len(match1)):
      dicti[(match1[j].text)]=(match[j].text)


  
  return dicti



def ncbi_pubmed_extract(link):
  """ Gets the ncbi abstracts"""
  dicti={}
  result=requests.get(link)
  src=result.content
  soup= BeautifulSoup(src,'lxml')
  match=soup.find_all('div',class_='abstract-content selected')
  for j in match:
    dicti['Abstract']=(j.text.strip())

  return dicti
      
      
def nejm_extract(link):
  """Extracts njem articles """
  dicti={}
  result = requests.get(link)
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

  return dicti

      
def pmc_extract(link):
  dicti={}
  result = requests.get(link)
  src = result.text
  soup = BeautifulSoup(src, 'lxml')
  match = soup.find_all('div',class_="tsec sec")
  match2=soup.find_all('h2',class_='head no_bottom_margin')
  for j in range(len(match2)):
    key=len(match2[j].text)  
    dicti[(match2[j].text)]=(match[j].text[key:])
  for i in match2:
    print(i.text)

  return dicti

def scimag(link):
  dicti={}
  result=requests.get(link)
  src = result.text
  soup=BeautifulSoup(src, 'lxml')


  match = soup.find_all('div',class_='section abstract')
  intro=  soup.find_all('div',class_='section introduction')
  match2 = soup.find_all('div',class_='section discussion')
  match3 = soup.find_all('div',class_='section conclusions')

  abstract=""
  intro=""
  discussion=""
  conclusions=""

  for j in match:
    abstract+=abstract+j.text
  for k in match2:
    discussion+=k.text
  for m in intro:
    intro+= m.text

  for f in match3:
    conclusions+=(f.text)
  if(abstract):
    dicti['Abstract']=abstract
  
  if(intro):
    dicti['Introduction']=intro

  if(discussion):
    dicti['Discussion']=discussion

  if(conclusions):
    dicti['Conclusion']=conclusions
  return dicti
  
  

    


    
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

def scrape_nature(naturelink):
  dicti={}
  result=requests.get(naturelink)
  src = result.text
  soup=BeautifulSoup(src, 'lxml')
  match2 = soup.find_all('h2',class_='c-article-section__title')
  match = soup.find_all('div',class_='c-article-section')
  for i in range(min(len(match2),len(match))):
    key=(match2[i].text)
    l=len(key)
    dicti[key]=(match[i].text[l:])
    
  return dicti














