from fastapi import HTTPException
from services import comments as comment_service
from utils import counter, data_extractor, temp_store, case_law_citation_patterns
from config.config import settings
# import json
# import stanza
# import torch
from models import bart_large, distillbert_cased
from eyecite import get_citations, clean_text, resolve_citations, annotate_citations
from eyecite.tokenizers import HyperscanTokenizer

import re

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
            # word_count = counter.word_counter(comment_content)
            word_count = 0
            # word_count = 0
            authors = get_comment_authors(comment_title, comment_content)
            # authors = ""
            # tech_tools = get_tech_tools(comment_content)
            tech_tools = []
            # cited_case_laws = get_cited_case_laws(comment_content)
            cited_case_laws = []
            simple_metadata = {
                "comment_id": comment_id,
                "comment_title": comment_title,
                "document_url": document_url,
                "document_name": document_name, 
                "document_size": document_size,
                "word_count": word_count,
                "authors": authors,
                "tech_tools": tech_tools,
                "cited_case_laws": cited_case_laws
            }

            # Store metadata
            temp_store.store_metadata(simple_metadata)

            # data = {
            #     "comment_id": comment_id,
            #     "comment_title": comment_title,
            #     "document_url": document_url,
            #     "document_name": document_name, 
            #     "document_title":"",
            #     "document_size": document_size,
            #     "word_count": word_count,
            #     "authors": authors,
            #     "document_content": comment_content
            # }
            # with open('/Users/peace/Developer/Machine Learning/Research/mscc/utils/text.json', 'w') as file:
            #     json.dump(data, file, indent=4)

            return simple_metadata
        
        # If comment has no attachement, extract few metadata (Ex: comment_id = 'COLC-2023-0006-0862')
        else:
            comment_content = comment_data['comment']
            authors = get_comment_authors(comment_title, comment_content)
            # authors=""
            # word_count = counter.word_counter(comment_content)
            word_count = 0
            # tech_tools = get_tech_tools(comment_content)
            tech_tools=[]
            # cited_case_laws= get_cited_case_laws(comment_content)
            cited_case_laws = []
            simple_metadata = {
                "comment_id": comment_id,
                "comment_title": comment_title, 
                "file_url": "No attached document",
                "file_name": "Does not apply", 
                "file_size": "Does not apply",
                "word_count": word_count,
                "authors": authors,
                "tech_tools": tech_tools,
                "cited_case_laws": cited_case_laws
            }

            # store metadata
            temp_store.store_metadata(simple_metadata)

            return simple_metadata
        
    else:
        raise HTTPException(status = response.status_code, message = "failed to fetch comment")
    

def get_comment_authors(comment_title, comment_content: str):
    question = "Who wrote this comment?"
    comment = comment_title + ' ' + comment_content.replace('\n', ' ')
    comment_size = len(comment)

    # Limit large document input
    first_chunk ="" # The first 1024 tokens of the document
    last_chunk="" # The last tokens of the document
    if comment_size > 1024:
        first_chunk = comment[:1024]
        last_chunk = comment[(comment_size-1024):]

        # Extract authors with BART-LARGE
        authors = bart_large.question_answering(question=question, text=first_chunk)

        # Extract from last chunk if the author was not found in first chunk
        if (len(authors) == 0):
            authors=(bart_large.question_answering(question=question, text=last_chunk))

        print("\n\n\n\n\n AUTHORS:\n", authors, "\n\n\n\n")
        # authors = list(set(authors))
        print("\n\n\nFIRST CHUNK\n", first_chunk, "\n\n\n",last_chunk, " \n\n\n\n")

    else:
        # Extract authors with BART-LARGE
        authors = bart_large.question_answering(question=question, text=comment)

        
    return authors