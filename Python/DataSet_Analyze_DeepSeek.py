
import string
import pandas as pd
import requests
import time
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

#API DeepSeek
API_URL = 'https://api.deepseek.com/v1/chat/completions'
MODEL = 'deepseek-chat'
API_TOKEN = ''


nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):

    try:

        text = str(text).strip().lower() if pd.notnull(text) else ''


        tokens = word_tokenize(text)


        filtered_tokens = [
            token for token in tokens
            if token not in stop_words
            and token not in string.punctuation
            and token.isalnum()
        ]

        lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]

        return ' '.join(lemmatized_tokens)

    except Exception as e:
        print(f"Erro no pré-processamento: {str(e)}")
        return ''

def analyze_with_deepseek(text, max_retries=3, timeout=20):

    prompt_template = """Analise esta frase e retorne 3 números separados por vírgula:
    1) 1 se contém homofobia, 0 caso contrário
    2) 1 se contém sexismo, 0 caso contrário
    3) 1 se contém racismo, 0 caso contrário

    Frase: {text}
    Resposta (apenas números):"""

    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messages": [{"role": "user", "content": prompt_template.format(text=text)}],
        "model": MODEL,
        "temperature": 0.1,
        "top_p": 0.2,
        "max_tokens": 10
    }

    for attempt in range(max_retries):
        try:
            response = requests.post(API_URL, json=payload, headers=headers, timeout=timeout)
            response.raise_for_status()

            result = response.json()['choices'][0]['message']['content'].strip()
            if ',' in result and len(result.split(',')) == 3:
                return result
            return "x,x,x"  # Padrão seguro para respostas inválidas

        except requests.exceptions.RequestException as e:
            print(f"Tentativa {attempt+1} falhou: {str(e)}")
            time.sleep(2 ** attempt)
        except Exception as e:
            print(f"Erro inesperado: {str(e)}")
            time.sleep(1)

    return "x,x,x"  # Fallback após todas as tentativas

def process_dataset(input_file, output_file):
    try:

        df = pd.read_csv(input_file)


        df['Text'] = df['Text'].fillna('').astype(str)
        print(f"Dataset carregado com {len(df)} registros")


        print("Iniciando pré-processamento...")
        df['Text_Processado'] = df['Text'].apply(preprocess_text)


        print("Iniciando análise via DeepSeek...")
        start_time = time.time()
        resultados = []

        for idx, texto in enumerate(df['Text_Processado']):
            if idx % 10 == 0:
                print(f"Processando registro {idx+1}/{len(df)}")
                time.sleep(1)  # Evitar rate limiting

            resultado = analyze_with_deepseek(texto)
            resultados.append(resultado)

        df[['Homofobia', 'Sexismo', 'Racismo']] = pd.DataFrame(
            [x.split(',') for x in resultados],
            dtype=int
        )

        df.to_csv(output_file, index=False)
        print(f"Processo concluído em {time.time()-start_time:.2f} segundos")
        print(f"Resultados salvos em: {output_file}")

    except Exception as e:
        print(f"Erro crítico no processamento: {str(e)}")

if __name__ == "__main__":


    INPUT_CSV = 'Data/test.csv'
    OUTPUT_CSV = 'Data/Results/DeepSeek/test_result.csv'

    process_dataset(INPUT_CSV, OUTPUT_CSV)
