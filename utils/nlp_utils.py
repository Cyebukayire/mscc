from fastapi import HTTPException
from utils import data_extractor
from models import bart_large, t5
from eyecite import get_citations, clean_text

# Extract author names
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
   
# Extract tech tools
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
    max_length = 2048 # Token limit for each chunk for large comments
    summary = t5.summarize(comment_content, max_length)

    return summary
