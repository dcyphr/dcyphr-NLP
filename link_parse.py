import requests


from bs4 import BeautifulSoup

import csv

lst=[]
""" Reading the csv file """
with open('links.csv','r') as file:
  reader=csv.reader(file)
  for row in reader:
    lst.append(row[0])

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
  dicti=[]
  m=['Abstract','Introduction']
  for i in pmc:
    result = requests.get(i)
    src = result.text
    soup = BeautifulSoup(src, 'lxml')

    match = soup.find_all('div',class_="tsec sec")
    for i in range(len(match[:5])):
      
      dicti.append(match[i].text)
      
      
  for i in dicti:

    print(i)
    print('\n')
    print('\n')
  # print(match2)
  # for k in range(len(match)):
  #   print(match2[k].text)
  #   print(match[k].text)

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

    


def get_sim():
  """Gets similar articles """
  sim=soup.find('div',class_='similar-articles') 
  if(sim):
    index3=sim.find('articles')
    sim='Similar Articles|'+sim.text[27:].strip()
    f.write(sim)


def get_ref():
  """ Gets reference to articles """
    
  ref=soup.find('div',class_='references')
  if(ref):
    index3=sim.find('References')
    ref='References|'+ref.text[19:].strip()
    f.write(ref)

def get_cit():
  """ Gets citations """
  cite=soup.find('div',class_='citedby-articles')
  if(cite):
    index3=cite.find('articles')
    cite='Cited By|'+cite.text[42:].strip()
    f.write(cit)

def get_pub():
  """ Gets publications """

  pub=soup.find('div',class_='publication-types keywords-section')
  if(pub!=None):
    index3=pub.find('types')
    pub='Publications|'+pub.text[30:].strip()
    # print(pub)
    f.write(pub)

def get_head():
  heading=soup.find('h1')
  if(heading!=None):
      head=heading.text.strip()
      # print(head)
      f.write(head)


def get_abstract():
  """ Gets the abstracts """
  match=soup.find('div',class_='abstract')
  if(match!=None):
    
    index=match.text.find('Abstract')
    m=match.text[index+8:]
    abstract='Abstract|'+m.strip()
    # print(abstract)
    f.write(abstract)


exception=[]
f = open("file.txt", "x")
for i in lst[1:]:
  try:

    result=requests.get(i)
    src=result.content
    soup= BeautifulSoup(src,'lxml')
    
    
    # else:
    #   abstract=""
    # # print(abstract)


    # print(head)
    # print(abstract)
    # print('\n')
    get_head()
    print('\n')
    get_abstract()
    print('\n')
    get_sim()
    print('\n')
    get_ref()
    print('\n')
    get_cit()
    print('\n')
    get_pub()

  except:
    exception.append(i)
