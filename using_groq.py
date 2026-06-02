#### pip install -q groq

from google.colab import userdata
userdata.get('GROQ_API_KEY')

import os
os.environ["GROQ_API_KEY"] = userdata.get("GROQ_API_KEY")

from groq import Groq
client2 = Groq()

completion = client2.chat.completions.create(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    messages=[
      {
        "role": "user",
        "content": "Como estudar melhor IA: no Google Colab ou locamente no meu desktop?"
      }
    ],
    temperature=0,   
    max_tokens=1024,   ## 0=menos criativo, 1=mais criativo ##
    top_p=1,
    stream=True,
    stop=None
)
for chunk in completion:
    print(chunk.choices[0].delta.content or "", end="")
    
    

