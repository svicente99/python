## DESAFIO COM PYTHON E PANDAS ##
## --------------------------- ##

#  versão para o Google Colab and Hugging Face Pipeline

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

def classify_feedback(text):
    """Classify customer feedback as Positive, Neutral, or Negative
    Using a dedicated sentiment model
    """
    try:
        result = classifier(text[:512])  # Truncate to model's max length
        # Map the model's labels to your categories
        label = result[0]['label'].upper()
        # The model returns LABEL_0 (Negative), LABEL_1 (Neutral), LABEL_2 (Positive)
        if 'POSITIVE' in label or 'LABEL_2' in label:
            return 'Positive'
        elif 'NEGATIVE' in label or 'LABEL_0' in label:
            return 'Negative'
        else:
            return 'Neutral'
    except:
        return 'Neutral'    
##  end of function: classify_feedback


# Apply to dataframe
df_reviews['feeling'] = df_reviews['reviewText'].apply(classify_feedback)

# View results
print(df_reviews[['reviewText', 'feeling']])

