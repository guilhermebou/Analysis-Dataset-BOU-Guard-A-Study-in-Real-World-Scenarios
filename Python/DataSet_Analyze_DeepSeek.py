import string
import pandas as pd
import requests
import time
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from concurrent.futures import ThreadPoolExecutor
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import csv

start_time = time.time()
API_URL = 'https://api.deepseek.com/v1/chat/completions'
MODEL = 'deepseek-chat'
API_TOKEN = ''
MAX_WORKERS = 5
TIMEOUT = 45
MAX_RETRIES = 3

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
stop_words = set(stopwords.words('english'))
punctuation = set(string.punctuation)
lemmatizer = WordNetLemmatizer()

session = requests.Session()
retry = Retry(total=MAX_RETRIES, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
adapter = HTTPAdapter(max_retries=retry)
session.mount('https://', adapter)

def preprocess(data):
    tokens = nltk.word_tokenize(data.lower())
    filtered = [lemmatizer.lemmatize(t) for t in tokens
                if t not in stop_words and t not in punctuation]
    return ' '.join(filtered)

def analyze_with_deepseek(text):
    prompt = ("Generate a CSV row with three columns, based on the following sentence, where: "
        "the first column should contain the value 1 if the sentence contains any indication of homophobia; "
        "the second column should contain the value 1 if the sentence contains any indication of sexism; "
        "the third column should contain the value 1 if the sentence contains any indication of racism. "
        "(Please only write according to the CSV template. I don’t want text, just numbers for the tags "
        "and commas to separate them and no spaces as well.)" " The sentence is: " + text)

    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 1.0,
        "top_p": 1.0
    }

    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        response = session.post(
            API_URL,
            json=payload,
            headers=headers,
            timeout=TIMEOUT
        )
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Error processing '{text[:30]}...': {str(e)[:100]}")

if __name__ == "__main__":
    df = pd.read_csv('Data/Datasets_Homo.csv')
    df['Text_Lem'] = df['Text'].apply(preprocess)

    with open('Data/Results/DeepSeek/DataSet_HOMO_LEM_DeepSeek_2.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerow(['Homophobia', 'Sexism', 'Racism'])

        #processamento paralelo
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            for i, result in enumerate(executor.map(analyze_with_deepseek, df['Text_Lem'])):
                writer.writerow(result.split(','))
                print(f"processando linha {i+1}/{len(df)}: {result}")

    #log
    elapsed = (time.time() - start_time) / 60
    log_entry = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Tempo total: {elapsed:.2f} minutos.\n"

    with open("execution_DataSet_HOMO_LEM_DeepSeek_2_log.txt", "a") as f:
        f.write(log_entry)

    print(f"Processo concluído em {elapsed:.2f} minutos")
