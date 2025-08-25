import string

import pandas as pd

import requests
url = 'https://api.openai.com/v1/chat/completions'
model = 'gpt-4'
#model='gpt-4o-mini-2024-07-18'

token = ''

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

start_time = time.time()


def preprocess(data):
    lemmatizer = WordNetLemmatizer()
    tokens = word_tokenize(data.lower())
    filtered_tokens = [token for token in tokens if token not in stop_words and token not in string.punctuation]
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]
    return ' '.join(lemmatized_tokens)

def analyze_sentiment_with_gpt(data, max_retries=3, timeout=10):
    prompt = [
        {'role': 'user', 'content': f'"Generate a CSV row with three columns, based on the following sentence, where: the first column should contain the value 1 if the sentence contains any indication of homophobia; the second column should contain the value 1 if the sentence contains any indication of sexism; the third column should contain the value 1 if the sentence contains any indication of racism. (Please only write according to the CSV template. I don t want text, just numbers for the tags and commas to separate them and no spaces as well.)" The sentence is:{data}'}
    ]

    for attempt in range(max_retries):
        try:
            response = requests.post(
                url,
                headers={'Authorization': f'Bearer {token}'},
                json={
                    'model': model,
                    'messages': prompt
                },
                timeout=timeout
            )
            response.raise_for_status()  # HTTPError 4xx/5xx
            data = response.json()
            return data['choices'][0]['message']['content']
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
            else:
                return "Error"

df = pd.read_csv('Data/Datasets_Normal.csv')

#stop_words = set(stopwords.words('english'))
#df['Text_Lem'] = df['Text'].apply(preprocess)


print(start)

results = []
for n, line in enumerate(df['Text']):
    output = analyze_sentiment_with_gpt(line)
    results.append(output)
    print(n, " ", output)

df['Sentiments_analyze'] = results
df.to_csv('Data/Results/GPT4.0/DataSet_NORMAL_BRUTO_Result_GPT4.csv', index=False)

end = time.time()
print(end - start)

# log
elapsed = (time.time() - start_time) / 60
log_entry = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Tempo total: {elapsed:.2f} minutos.\n"

with open("execution_GPT4_NORMAL_BRUTO_log.txt", "a") as f:
    f.write(log_entry)

print(f"Processo concluído em {elapsed:.2f} minutos")
