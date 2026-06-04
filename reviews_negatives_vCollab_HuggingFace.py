## EXERCICIO COM PYTHON AND AI ##
## --------------------------- ##

#  versão para o Google Colab and Hugging Face Pipeline
#  analise das reviews negativas

#  This uses a dedicated sentiment analysis model that's perfect for 
#  Positive/Neutral/Negative classification. 
#  It's much faster than LLMs since it's built specifically for this task.

# 1. carregar o arquivo dado 'reviews.csv' em um dataframe
# 2. a coluna que interessa é a 4a. 'reviewText'
# 3. usa a pipeline pra trazer o "sentimento" de cada feedback (Positivo/Neutro/Negativo)
# 4. adicionar este resultado em uma nova coluna do dataframe


## it needs to install before to use : !pip install transformers torch

import pandas as pd
from transformers import pipeline

MY_CSV = 'reviews.csv'

# Load the CSV file into a DataFrame
df_reviews = pd.read_csv(MY_CSV)

# View the first 5 rows
print(df_reviews.head())

# Load model with specific parameters for sentiment analysis
classifier = pipeline(
    "sentiment-analysis", 
    model="distilbert-base-uncased-finetuned-sst-2-english",  # More robust model
    return_all_scores=False
)

def classify_feedback(text):
    """Classify customer feedback as Positive, Neutral, or Negative
    Using a dedicated sentiment model
    Improved classification with better error handling
    """
    
    if pd.isna(text) or str(text).strip() == "":
        return "Neutral"
    
    # Convert to string and clean
    text = str(text).strip()
    
    try:
        # Get prediction with confidence scores
        result = classifier(text[:512])
        label = result[0]['label']
        score = result[0]['score']
        
        # Map to three categories
        if label == 'POSITIVE':
            # Use confidence threshold to detect Neutral
            if score < 0.6:  # Low confidence = likely neutral
                return "Neutral"
            return "Positive"
        else:  # NEGATIVE
            if score < 0.6:
                return "Neutral"
            return "Negative"
            
    except Exception as e:
        print(f"Error processing '{text[:50]}...': {e}")
        return "Neutral"    

##  end of function: classify_feedback


# Apply to dataframe
df_reviews['feeling'] = df_reviews['reviewText'].apply(classify_feedback)

# View results
print(df_reviews[['reviewText', 'feeling']])


df_reviews_negativas = df_reviews[ df_reviews['feeling']=='Negative' ]
df_reviews_negativas.shape

lst_reviews_negativas = df_reviews_negativas['reviewText']
print(lst_reviews_negativas)

textao_resenhas_negativas = ' ___ '.join(lst_reviews_negativas)


# ------------------------------------------
# categorizando todas as respostas negativas
# ------------------------------------------


# Configure your API key (replace with your actual key)
import os
from google.colab import userdata
os.environ["GOOGLE_API_KEY"] = userdata.get('Gemini_API_key')

from google import genai
client = genai.Client()

# Setting my specific Gemini model
MY_GEMINI_MODEL = "gemini-3-flash-preview"

categorizacao = client.models.generate_content(
    model = MY_GEMINI_MODEL,
    contents = f"""Você é um cientista de dados. Vou te passar várias resenhas negativas de análises
        de um produto, que estão separadas por " ___ ". Então, quero que classifique em 5 distintas
        categorias para estas análises e retorne uma lista ordenada delas.
        
        Segue o conjunto das resenhas negativas na próxima linha:
        {textao_resenhas_negativas}"""
    )
        
print(categorizacao.text)        


# # # salvei este conteudo num arquivo e coloquei na área de "Files"


with open('reviews_negativas_categorizacoes.out', 'r', encoding='utf-8') as arquivo:
    str_categorizacao = arquivo.read()

mini_5_categorias = client.models.generate_content(
    model = MY_GEMINI_MODEL,
    contents = f"""Com base nesta mesma categorizacao, reduza cada um dos 5 agrupamentos
        a 5 termos substantivos (APENAS) que sumarizem a ideia principal:
        {str_categorizacao}"""
    )
        
lst_5_categorias = mini_5_categorias.split(sep=", ")
print(lst_5_categorias)
