import requests
import pandas as pd
import os
import re
from elasticsearch import helpers, Elasticsearch
import csv


# Download the dataset to the working directory
url = "http://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz"
filename = url.split("/")[-1]

with open(filename, "wb") as f:
    r = requests.get(url)
    f.write(r.content)

# import the txt files in the "unsup" folder into python and then concatenate into a dataframe
df = pd.DataFrame()
path = "C:/Users/englerttw/PycharmProjects/textMiningProject/aclImdb/train/unsup/"
for file in os.listdir(path):
    with open(os.path.join(path, file),'r', encoding='utf-8') as infile:
        txt = infile.read()
    df = df.append([txt], ignore_index=True)
df.columns = ['review']

# clean up all the random garbage in the dataframe; like html code 
def preprocessor(text):
    text = re.sub('<[^>]*>', '', text)
    emoticons = re.findall('(?::|;|=)(?:-)?(?:\)|\(|D|P)', text)
    text = re.sub('[\W]+', ' ', text.lower()) +\
        ' '.join(emoticons).replace('-', '')
    return text

df['review'] = df['review'].apply(preprocessor)

# Save the assembled data to a csv file to the current working directory
df.to_csv('./unlabeled_movie_data.csv', index=False, encoding='utf-8')


# Apply TextBlob classifier to the DataFrame
for index, row in df.iterrows():
    temp = TextBlob(row['review'])
    df.loc[index,'sentscore'] = temp.sentiment.polarity
	
# Add a new column to the DataFrame that bins the sentiment score
# We can always scale our definition of positive, negative and neutral up and down	
for index, row in df.iterrows():
    if df.loc[index,'sentscore'] >= 0.1:
        df.loc[index,'best_guess'] = 'positive'
    elif df.loc[index,'sentscore'] <= -0.1:
        df.loc[index,'best_guess'] = 'negative'
    else:
        df.loc[index,'best_guess'] = 'neutral'

# For simplicity, write the DataFrame to a CSV. The CSV will be used to import data into Elastic Search
df.to_csv('./analyzed_unlabeled_movie_data.csv', index=False, encoding='utf-8')

# Make sure Elastic Search is running in your Windows Services
es = Elasticsearch()

# Bulk load the analyzed_unlabeled_movie_data into Elastic Search
with open('analyzed_unlabeled_movie_data.csv', encoding="utf8") as f:
    reader = csv.DictReader(f)
    helpers.bulk(es, reader, index='movies', doc_type='reviews')












