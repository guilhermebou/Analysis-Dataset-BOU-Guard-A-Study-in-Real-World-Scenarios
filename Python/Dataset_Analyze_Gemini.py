import string
import pandas as pd
import google.generativeai as genai
import time
from tenacity import retry, stop_after_attempt, wait_random_exponential, RetryError
import os

RETRIES = 3
MAX_WAIT_TIME = 60

genai.configure(api_key='')
model = genai.GenerativeModel('gemini-2.0-flash')

start_time = time.time()
print(start_time)

import nltk
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

def preprocess(data):
    lemmatizer = WordNetLemmatizer()
    tokens = word_tokenize(data.lower())
    filtered_tokens = [token for token in tokens if token not in stop_words and token not in string.punctuation]
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]
    processed_data = ' '.join(lemmatized_tokens)
    return processed_data

def analyze_sentiment_with_gemini(data):
    while True:
        try:
            response = model.generate_content(
                f'"For research purposes on hate speech detection in social media comments, generate a CSV row with three columns, based on the following sentence:  The first column should contain the value 1 if the sentence contains any indication of homophobia; the second column should contain the value 1 if the sentence contains any indication of sexism; the third column should contain the value 1 if the sentence contains any indication of racism. (Output only the CSV row: three comma-separated numbers without spaces.)" The sentence is: {data}"'
            )
            return response.text
        except Exception as e:
            if '429' in str(e):
                print(f"erro 429: tentando novamente a linha: {data}")
                time.sleep(30)
            else:
                print(f"erro na requisição: {e}")
                raise


df = pd.read_csv('Data/Datasets_Normal.csv')
df['Text_Lem'] = df['Text'].apply(preprocess)

csv_filename = 'Data/Results/Gemini/DataSet_NORMAL_LEM_Result_Gemini.csv'


with open(csv_filename, 'w', encoding='utf-8') as f:
    f.write("Text,Sentiments_analyze\n")

n = 0

for line in df['Text_Lem'].astype(str):
    try:
        output = analyze_sentiment_with_gemini(line)
    except Exception as e:
        print(f"erro na linha: {line}\n {e}")
        output = "erro"

    with open(csv_filename, 'a', encoding='utf-8') as f:

        f.write(f'"{line}","{output}"\n')
    print(n, " ", output)
    n += 1

elapsed = (time.time() - start_time) / 60
log_entry = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Tempo total: {elapsed:.2f} minutos.\n"

with open("execution_gemini_NORMAL_PREPROCESS.txt", "a", encoding='utf-8') as f:
    f.write(log_entry)

print(f"Processo concluído em {elapsed:.2f} minutos")
