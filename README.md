# Analysis Dataset: BOU-Guard - A Study in Real-World Scenarios

Este repositório contém a análise e o estudo do BOU-Guard, uma ferramenta para detectar discursos ofensivos (racismo, homofobia, sexismo) em cenários reais utilizando comentários de redes sociais como Twitter (X) e Reddit.
Apresentado na [UFU-FACOM | XVIII Workshop de Teses e Dissertações em Ciência da Computação](https://techweek.facom.ufu.br/wtdcc-2024).

## 📋 Objetivo

Investigar a viabilidade e o comportamento de Modelos de Linguagem de Grande Escala (LLMs) na detecção de discursos ofensivos em redes sociais, comparando o desempenho das versões GPT-3.5 e GPT-4.
Este estudo é para promover a ferramenta  [`BOU-Guard | Extension`](https://github.com/guilhermebou/BOU-Guard-Extension), realizando uma comparação de modelos em um estudo de viabilidade.

## 🛠 Estrutura do Repositório

- `data/`  
  Contém os datasets analisados no estudo.  
- `python/`  
  Contém os scripts de análise, pré-processamento de dados e classificação.  
- `results/`  
  Resultados finais organizados em planilhas.  
- `docs/`  
  documentação para fundamentação.

## 🚀 Funcionalidades

- **Pré-processamento de Dados**: Filtragem e organização de grandes volumes de dados de redes sociais.
- **Classificação Automatizada**: Uso de APIs para identificar conteúdos ofensivos em tempo real.
- **Visualização de Dados**: Apresentação dos resultados em relatórios organizados.

## 🧪 Metodologia

1. **Coleta de Dados**: Extração de comentários de redes sociais.
2. **Análise**: Classificação utilizando LLMs (GPT-3.5 e GPT-4).
3. **Comparação de Resultados**: Medição de desempenho, utilizando metricas como Recall, Precision e F1-SCORE.

## 📊 Resultados

Os resultados mostraram uma alta taxa de precisão do GPT-4 em relação ao GPT-3.5, com melhorias na identificação de nuances linguísticas em comentários ofensivos.
### Resultados do BOUGuard - Dataset Result GPT-3.5 (Lemmatization)

| Categoria  | Verdadeiro Positivo (VP) | Falso Positivo (FP) | Falso Negativo (FN) | Precision  | Recall  | F1-Score |
|------------|---------------------------|----------------------|----------------------|------------|---------|----------|
| Homofobia  | 503                       | 0                    | 177                  | 100,00%    | 73,97%  | 85,04%   |
| Sexismo    | 208                       | 0                    | 472                  | 100,00%    | 30,59%  | 46,85%   |
| Racismo    | 387                       | 0                    | 293                  | 100,00%    | 56,91%  | 72,54%   |
| Normal     | 609                       | 0                    | 71                   | 100,00%    | 89,56%  | 94,49%   |

### Resultados do BOUGuard - Dataset Result GPT-3.5 (Sem Lematização)

| Categoria  | Verdadeiro Positivo (VP) | Falso Positivo (FP) | Falso Negativo (FN) | Precision  | Recall  | F1-Score |
|------------|---------------------------|----------------------|----------------------|------------|---------|----------|
| Homofobia  | 497                       | 0                    | 183                  | 100,00%    | 73,09%  | 84,45%   |
| Sexismo    | 273                       | 0                    | 407                  | 100,00%    | 40,15%  | 57,29%   |
| Racismo    | 341                       | 0                    | 339                  | 100,00%    | 50,15%  | 66,80%   |



### Resultados do BOUGuard - Dataset Result GPT-4 (Lemmatization)

| Categoria  | Verdadeiro Positivo (VP) | Falso Positivo (FP) | Falso Negativo (FN) | Precision  | Recall  | F1-Score |
|------------|---------------------------|----------------------|----------------------|------------|---------|----------|
| Homofobia  | 650                       | 0                    | 30                   | 100,00%    | 95,59%  | 97,74%   |
| Sexismo    | 470                       | 0                    | 210                  | 100,00%    | 69,12%  | 81,74%   |
| Racismo    | 390                       | 0                    | 290                  | 100,00%    | 57,35%  | 72,90%   |
| Normal     | 622                       | 0                    | 58                   | 100,00%    | 91,47%  | 95,55%   |




Analisando os resultados mais minuciosamente, foram encontrados alguns ruídos nos datasets de sexismo e racismo. Neles, não estavam presentes 100% dos comentários correspondentes às suas respectivas labels. Por isso, foi realizada uma segunda análise manual, apresentada no arquivo[`manual_analysis_comments_racist_sexist.xlsx`](https://github.com/guilhermebou/Analysis-Dataset-BOU-Guard-A-Study-in-Real-World-Scenarios/blob/main/Data/Results/manual_analysis_comments_racist_sexist.xlsx)

### Resultados da Análise Manual de Comentários Racismo e Sexismo

| Categoria            | Verdadeiro Positivo (VP)  | Falso Positivo (FP)  | Falso Negativo (FN)  | Acurácia | Precisão | Recall | F1-Score |
|----------------------|---------------------------|----------------------|-------------------|----------|----------|--------|----------|
| Sexismo (GPT-4.0)    | 456                       | 52                   | 38                 | 91,67%   | 92,31%   | 89,76% | 91,02%   |
| Sexismo (GPT-3.5)    | 184                       | 24                   | 272                | 40,35%   | 62,64%   | 95,00% | 75,50%   |
| Racismo (GPT-4.0)    | 368                       | 22                   | 82                 | 81,78%   | 95,34%   | 84,59% | 89,64%   |
| Racismo (GPT-3.5)    | 313                       | 74                   | 137                | 69,56%   | 85,88%   | 76,66% | 81,01%   |
