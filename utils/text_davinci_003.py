from openai import OpenAI
from config.config import settings

client = OpenAI()

# model = "text-davinci-003"
model = "gpt-3.5-turbo"

# Question answering method
def question_answering(prompt: str, max_tokens = 16, temperature = 1):
    completion = client.chat.completions.create(
        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ],
        model = model,
        max_tokens = max_tokens,
        temperature = temperature
    )

    return completion.choices[0]