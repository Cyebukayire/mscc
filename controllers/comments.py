from fastapi import HTTPException
from services import comments as comment_service
from utils import counter, data_extractor, temp_store
from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification
from config.config import settings
import json

# Retrieve metadata of a single comment
async def get_comment_metadata(comment_id: str):
    response = await comment_service.get_comment(comment_id)
    response_data = response.json()

    # Extra metadata
    if response.status_code == 200:
        comment_data = response_data['data']['attributes']
        comment_title = comment_data['title']
        comment_content = ""

        # Check if the comment has an attachement and extract all simple metadata (EX: comment_id = 'COLC-2023-0006-0036')
        if 'included'in response_data:            
            document_url = []
            document_name = []
            document_size = 0

            for attachment in response_data['included']:
                document_url.append(attachment['attributes']['fileFormats'][0]['fileUrl'])
                document_name.append(attachment['attributes']['title'])
                document_size += attachment['attributes']['fileFormats'][0]['size']

            comment_content = data_extractor.text_extractor(document_url)
            word_count = counter.word_counter(comment_content)
            authors = get_comment_authors(comment_title, comment_content)
            simple_metadata = {
                "comment_id": comment_id,
                "comment_title": comment_title,
                "document_url": document_url,
                "document_name": document_name, 
                "document_size": document_size,
                "word_count": word_count,
                "authors": authors
            }

            # Store metadata
            temp_store.store_metadata(simple_metadata)


            data = {
                "comment_id": comment_id,
                "comment_title": comment_title,
                "document_url": document_url,
                "document_name": document_name, 
                "document_title":"",
                "document_size": document_size,
                "word_count": word_count,
                "authors": authors,
                "document_content": comment_content
            }
            with open('/Users/peace/Developer/Machine Learning/Research/mscc/utils/text.json', 'w') as file:
                json.dump(data, file, indent=4)

            return simple_metadata
        
        # If comment has no attachement, extract few metadata (Ex: comment_id = 'COLC-2023-0006-0862')
        else:
            comment_content = comment_data['comment']
            authors = get_comment_authors(comment_title, comment_content)
            word_count = counter.word_counter(comment_content)
            simple_metadata = {
                "comment_id": comment_id,
                "comment_title": comment_title, 
                "file_url": "No attached document",
                "file_name": "Does not apply", 
                "file_size": "Does not apply",
                "word_count": word_count,
                "authors": authors
            }
            # store metadata
            temp_store.store_metadata(simple_metadata)

            return simple_metadata
        
    else:
        raise HTTPException(status = response.status_code, message = "failed to fetch comment")



def get_comment_authors(comment_title, comment_content: str):
    # create smaller chunks of text from the comment
    #segments = [comment_content[i : i + segment_size] for i in range(0, len(comment_content), segment_size)]

    # initialize nlp pipleline
    '''
    When it comes to extracting citations from text, Named Entity Recognition (NER) models can be quite effective. Here are several models from Hugging Face's model hub that you might consider trying for author name extraction:
    0. GPT 3.5
    1. BERT-based Models: dslim/bert-base-NER: 
    2. RoBERTa-based Models: allenai/longformer-base-4096: 
    3. DistilBERT-based Models: distilbert-base-uncased
    4. ALBERT-based Models: albert-large-v2
    '''
    tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
    model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")

    nlp_pipeline = pipeline("ner", model="dslim/bert-base-NER", grouped_entities=True)
    # nlp_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, grouped_entities=True)
    # send an author extraction request to huggingface transformers
    prompt = f"What are the authors of this document below? \n Document title: {comment_title} \n \"{comment_content}\"."
    # prompt = f"Identify full names of authors of this comment: \"{comment_content}\""
    response = nlp_pipeline(prompt)
    print(response)
    
    # extract authors 
    result = [entity['word'] for entity in response if entity['entity_group'] == 'PER']
    print(result)
    authors = list(set(result))

    return authors

    # import spacy

    # # Load the English language model
    # nlp = spacy.load("en_core_web_sm")

    # # Your text containing author names
    # text = "title: " + comment_title + "\n" + comment_content
    # # text = comment_content 
    # # Process the text with spaCy
    # doc = nlp(text)

    # # Extract entities that are people (PERSON entity type)
    # newauthors = [entity.text for entity in doc.ents if entity.label_ == "PERSON"]

    # print("Authors found:", newauthors)
    # return authors
