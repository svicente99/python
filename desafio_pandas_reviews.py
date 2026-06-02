## DESAFIO COM PYTHON E PANDAS ##
## --------------------------- ##

# 1. carregar o arquivo dado 'reviews.csv' em um dataframe
# 2. a coluna que interessa é a 4a. 'reviewText'
# 3. usar uma LLM para classificar o "sentimento" de cada feedback (Positivo/Neutro/Negativo)
# 4. adicionar este resultado em uma nova coluna do dataframe


## it needs to install before pandas:  pip install pandas

import pandas as pd
import requests
import json

MY_CSV = 'reviews.csv'

# Load the CSV file into a DataFrame
df_reviews = pd.read_csv(MY_CSV)

# View the first 5 rows
print(df_reviews.head())


def classify_feedback(text, model="deepseek-r1:1.5b"):
    """
    Classify customer feedback as Positive, Neutral, or Negative
    """
    prompt = f"""Classify the following customer feedback as exactly one word: Positive, Neutral, or Negative.
    Feedback: "{text}"
    Classification:"""
    
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }
    )
    
    result = response.json()
    classification = result['response'].strip()
    
    # Clean up response to ensure it's one of the three categories
    for category in ["Positive", "Neutral", "Negative"]:
        if category.lower() in classification.lower():
            return category
    return "Neutral"  # Default
    
##  end of function: classify_feedback

# Apply to your dataframe
df_reviews['feeling'] = df_reviews['reviewText'].apply(classify_feedback)

# View results
print(df_reviews[['reviewText', 'feeling']])

