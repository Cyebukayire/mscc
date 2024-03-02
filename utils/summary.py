from openai import OpenAI
from config.config import settings
from utils.data_extractor import text_extractor

# create openai client
openapi_api_key = settings.OPENAI_API_KEY
client = OpenAI(api_key=openapi_api_key)

async def extract_authors(comment):
    text = text_extractor(comment)

    # Prompt for author extraction
    prompt = f"Summarize the following document?\n \"{text}\""
    response = client.completions.create(model="text-davinci-003", prompt=prompt, max_tokens=100)

    # extract authors
    authors = response.choices[0].text

    return authors
