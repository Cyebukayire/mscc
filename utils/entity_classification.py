from utils.text_davinci_003 import question_answering

# Method to determine entity with GPT
def determine_entity(comment_title: str):
    prompt =  f"Is the comment ['{comment_title}'] more likely from a person or an entity? Respond with 'person' or 'entity'."
    response = question_answering(prompt=prompt)

    # Extract entity from api response
    entity  = response.message.content

    return entity





