import requests


from bs4 import BeautifulSoup

import csv

lst=[]
""" Reading the csv file """
with open('links.csv','r') as file:
  reader=csv.reader(file)
  for row in reader:
    lst.append(row[0])

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
  """Gets the headings"""

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
