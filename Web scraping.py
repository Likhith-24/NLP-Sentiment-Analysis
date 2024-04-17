#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import requests
import bs4 as bfs
import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import string
from textblob import TextBlob
import csv
import numpy as np


# In[2]:


df = pd.read_excel('Input.xlsx',index_col=0)
df


# In[3]:


li = [url for url in df['URL']]
li


# In[4]:


articletext = []
for url in li:
    articletext.append(requests.get(url,headers={"User-Agent": "XY"}))


# In[5]:


for i in range(len(articletext)):
    articletext[i] = bfs.BeautifulSoup(articletext[i].content,'html.parser')


# In[6]:


articles = []
for text in articletext:
    articles.append(articletext[i].find(attrs= {"class":"td-post-content"}).text)


# In[7]:


for i in range(len(articles)):
  articles[i]= articles[i].replace('\n','')


# In[8]:


stop_words = list(set(stopwords.words('english')))


# In[9]:


articles


# In[10]:


sentences = []
for article in articles:
  sentences.append(len(sent_tokenize(article)))


# In[11]:


cleaned_text = ['']*len(articles)
for i in range(len(articles)):
  for w in stop_words:
    cleaned_text[i] = articles[i].replace(' '+ w +' ',' ').replace('?','').replace('.','').replace(',','').replace('!','')


# In[12]:


words = []
for article in articles:
  words.append(len(word_tokenize(article)))


# In[13]:


words_cleaned = []
for article in cleaned_text:
  words_cleaned.append(len(word_tokenize(article)))


# In[14]:


with open('positive-words.txt','r') as file:
    for line in file:
        for word in line.split():
            print(word)


# In[15]:


positive_words = open('positive-words.txt','r') 


# In[16]:


negative_words = open('negative-words.txt','r') 


# In[17]:


positive_score = [0]*len(articles)
for i in range(len(articles)):
  for word in positive_words:
    for letter in cleaned_text[i].lower().split(' '):
      if letter==word:
        positive_score[i]+=1


# In[18]:


negative_score = [0]*len(articles)
for i in range(len(articles)):
  for word in negative_words:
    for letter in cleaned_text[i].upper().split(' '):
      if letter==word:
        negative_score[i]+=1


# In[19]:


words_cleaned = np.array(words_cleaned)
sentences = np.array(sentences)


# In[20]:


df['POSITIVE SCORE'] = positive_score
df['NEGATIVE SCORE'] = negative_score


# In[21]:


df['POLARITY SCORE'] = (df['POSITIVE SCORE']-df['NEGATIVE SCORE'])/ ((df['POSITIVE SCORE'] +df['NEGATIVE SCORE']) + 0.000001)


# In[22]:


df['AVG SENTENCE LENGTH'] = np.array(words)/np.array(sentences)


# In[23]:


complex_words = []
syllable_counts = []


# In[24]:


for article in articles:
  syllable_count=0
  d=article.split()
  ans=0
  for word in d:
    count=0
    for i in range(len(word)):
      if(word[i]=='a' or word[i]=='e' or word[i] =='i' or word[i] == 'o' or word[i] == 'u'):
           count+=1
#            print(words[i])
      if(i==len(word)-2 and (word[i]=='e' and word[i+1]=='d')):
        count-=1;
      if(i==len(word)-2 and (word[i]=='e' and word[i]=='s')):
        count-=1;
    syllable_count+=count    
    if(count>2):
        ans+=1
  syllable_counts.append(syllable_count)
  complex_words.append(ans)    


# In[25]:


df['PERCENTAGE OF COMPLEX WORDS'] = np.array(complex_words)/np.array(words)


# In[26]:


df['FOG INDEX'] = 0.4 * (df['AVG SENTENCE LENGTH'] + df['PERCENTAGE OF COMPLEX WORDS'])


# In[27]:


df['AVG NUMBER OF WORDS PER SENTENCES'] = df['AVG SENTENCE LENGTH']


# In[28]:


df['COMPLEX WORD COUNT'] = complex_words


# In[29]:


df['WORD COUNT'] = words


# In[30]:


df['SYLLABLE PER WORD'] = np.array(syllable_counts)/np.array(words)


# In[31]:


total_characters = []
for article in articles:
  characters = 0
  for word in article.split():
    characters+=len(word)
  total_characters.append(characters)


# In[32]:


personal_nouns = []
personal_noun =['I', 'we','my', 'ours','and' 'us','My','We','Ours','Us','And'] 
for article in articles:
  ans=0
  for word in article:
    if word in personal_noun:
      ans+=1
  personal_nouns.append(ans)


# In[33]:


df['PERSONAL PRONOUN'] = personal_nouns


# In[34]:


df['AVG WORD LENGTH'] = np.array(total_characters)/np.array(words)


# In[35]:


df


# In[36]:


articles


# In[38]:


df = df.to_excel('Output.xlsx')


# In[ ]:




