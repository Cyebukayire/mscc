from fastapi import HTTPException
from services import comments as comment_service
from utils import counter, data_extractor, temp_store
from models import bart_large, distillbert_cased, facebook_bert_large, t5, pegasus_large
from eyecite import get_citations, clean_text

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
            # authors = get_comment_authors(comment_title, comment_content)
            # tech_tools = get_tech_tools(comment_content)
            # cited_case_laws = get_cited_case_laws(comment_content)
            summary = get_summary(comment_content)
            simple_metadata = {
                "comment_id": comment_id,
                "comment_title": comment_title,
                "document_url": document_url,
                "document_name": document_name, 
                "document_size": document_size,
                # "word_count": word_count,
                # "authors": authors,
                # "tech_tools": tech_tools,
                # "cited_case_laws": cited_case_laws,
                "summary": summary
            }

            # Store metadata
            temp_store.store_metadata(simple_metadata)

            return simple_metadata
        
        # If comment has no attachement, extract few metadata (Ex: comment_id = 'COLC-2023-0006-0862')
        else:
            comment_content = comment_data['comment']
            # authors = get_comment_authors(comment_title, comment_content)
            # word_count = counter.word_counter(comment_content)
            # tech_tools = get_tech_tools(comment_content)
            # cited_case_laws= get_cited_case_laws(comment_content)
            summary = get_summary(comment_content)
            
            simple_metadata = {
                "comment_id": comment_id,
                "comment_title": comment_title, 
                "file_url": "No attached document",
                "file_name": "Does not apply", 
                "file_size": "Does not apply",
                # "word_count": word_count,
                # "authors": authors,
                # "tech_tools": tech_tools,
                # "cited_case_laws": cited_case_laws,
                "summary": summary,
            }

            # store metadata
            temp_store.store_metadata(simple_metadata)

            return simple_metadata
        
    else:
        raise HTTPException(status = response.status_code, message = "failed to fetch comment")
    

def get_comment_authors(comment_title, comment_content: str):
    prompt = "Who wrote this comment?"
    comment = comment_title + ' ' + comment_content.replace('\n', ' ')
    comment_size = len(comment)

    # Limit large document input
    first_chunk ="" # The first 1024 tokens of the document
    last_chunk="" # The last tokens of the document
    if comment_size > 1024:
        first_chunk = comment[:1024]
        last_chunk = comment[(comment_size-1024):]

        # Extract authors with BART-LARGE
        authors = bart_large.question_answering(question=prompt, comment=first_chunk)

        # Extract from last chunk if the author was not found in first chunk
        if (len(authors) == 0):
            authors=(bart_large.question_answering(question=prompt, comment=last_chunk))

    else:
        # Extract authors with BART-LARGE
        authors = bart_large.question_answering(question=prompt, comment=comment)

    return authors
   

def get_tech_tools(comment_content: str):
    prompt = "what are the technologies discussed? Extract only their names." # If not, return none
    tech_tools = []

    # Create smaller text chunks
    chunks = data_extractor.create_text_chunks(comment_content)
    for chunk in chunks:
        tools = bart_large.question_answering(question=prompt, comment=chunk)
    
        # TODO Use NER model to accurately extract only names
        for tool in tools:
            if len(tool.split()) > 15:
                tools.remove(tool)

        # Append list of tools to tech_tools
        tech_tools.append(tools)
                
    if len(tech_tools) > 1:
        tech_tools = list(set(tuple(tool) for tool in tech_tools))

        # Remove empty strings from tools
        while ' 'in tools:
            tools.remove(' ')

        while '' in tools:
            tools.remove('')

    return tech_tools


def get_cited_case_laws(comment_content: str):
    # Clean comment, remove any html tags and white spaces for an even formated text
    cleaned_comment = clean_text(comment_content, ['html', 'all_whitespace']) 

    # Extract all citations
    citation_obj = get_citations(cleaned_comment) # Returns an object of detailed information about each citation

    # Collect only case laws from citation_obj
    citations = []
    for citation in citation_obj:
        citations.append(citation.token.data)
    citations = list(set(citations))

    return citations


def get_summary(comment_content: str):
    # Summarize the input comment
    print("\n\nSUMMARIZING...\n\n")
    summary = facebook_bert_large.summarize(comment_content)

    return summary
