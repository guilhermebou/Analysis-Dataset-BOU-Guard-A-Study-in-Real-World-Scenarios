import string

import pandas as pd

import requests
import google.generativeai as genai

genai.configure(api_key='')
model = genai.GenerativeModel('gemini-pro')

import time
start = time.time()
print (start)

import nltk
#nltk.download('punkt')
#nltk.download('stopwords')
#nltk.download('wordnet')
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

def preprocess(data):
    lemmatizer = WordNetLemmatizer()
    tokens = word_tokenize(data.lower())

    filtered_tokens = []
    for token in tokens:
        if token not in stop_words and token not in string.punctuation:
            filtered_tokens.append(token)


    lemmatized_tokens = []
    for token in filtered_tokens:
        lemmatized_tokens.append(lemmatizer.lemmatize(token))

    processed_data = ' '.join(lemmatized_tokens)
    return processed_data


def analyze_sentiment_with_gemini(data):

    response = model.generate_content(f'"Generate a CSV row with three columns, based on the following sentence, where: the first column should contain the value 1 if the sentence contains any indication of homophobia; the second column should contain the value 1 if the sentence contains any indication of sexism; the third column should contain the value 1 if the sentence contains any indication of racism. (Please only write according to the CSV template. I don t want text, just numbers for the tags and commas to separate them and no spaces as well.)" The sentence is: {data}"')
    print(response.text)

df = pd.read_csv('Data/Test/Datasets_Homo_Portion.csv')


df['Text_Lem'] = df['Text'].apply(preprocess)

n = 0

for line in df['Text_Lem'].astype(str):

    #print(line)
    output=analyze_sentiment_with_gemini(str(line))
    df.loc[df['Text_Lem'] == line, 'Sentiments_analyze'] = output
    df.to_csv('Data/Results/Portion/DataSet_Homo_Result_Extra_Gemini.csv')
    print(n," ",output)
    n +=1

end = time.time()

print (end-start)

