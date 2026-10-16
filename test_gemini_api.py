from openai import OpenAI
import os
# Inizializza il client OpenAI puntando all'endpoint di Google Gemini
key = os.environ["LLM_API_KEY"]
model= os.environ["LLM_MODEL"]
url = os.environ["LLM_BASE_URL"]
client = OpenAI(
    api_key=key,
    base_url=url
)

response = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": "Sei un assistente di cucina."},
        {"role": "user", "content": "Spiegami come funziona l'IA in breve quando è un insegnante di cucina."}
    ]
)

print(response.choices[0].message.content)
