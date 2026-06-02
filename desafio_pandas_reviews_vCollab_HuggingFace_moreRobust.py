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
pd.set_option('display.max_colwidth', 100)  # don't cut off text column of review
print(df_reviews[['reviewText', 'feeling']])

# Save result to CSV
df_reviews.to_csv('reviews_output.csv')

# end of code #
# - - - - - - #
