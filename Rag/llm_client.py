from config import API_KEY, BASE_URL
from openai import OpenAI

client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)