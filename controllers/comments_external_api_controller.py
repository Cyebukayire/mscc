from fastapi import HTTPException
from services import comments as comment_service
from utils import data_extractor, temp_store, word_counter
from utils.nlp_utils import get_comment_authors, get_tech_tools

# Retrieve metadata for a single comment
async def get_comment_metadata(comment_id: str):
    response = await comment_service.get_comment_with_url(comment_id)
    
    # Extra metadata
    if response.status_code == 200:
        response_data = response.json()
        comment_data = response_data['data']['attributes']
        comment_title = comment_data['title']
        comment_content = ""

        # Check if the comment has an attachement and extract metadata
        if 'included'in response_data:            
            document_url = []
            document_name = []
            document_size = 0

            for attachment in response_data['included']:
                document_url.append(attachment['attributes']['fileFormats'][0]['fileUrl'])
                document_name.append(attachment['attributes']['title'])
                document_size += attachment['attributes']['fileFormats'][0]['size']

            comment_content = data_extractor.text_extractor(document_url)
            word_count = word_counter.word_counter(comment_content)
            authors = get_comment_authors(comment_title, comment_content)
            tech_tools = get_tech_tools(comment_content)

            # Save extracted metadata
            metadata = {
                "comment_id": comment_id,
                "comment_title": comment_title,
                "document_url": document_url,
                "document_name": document_name, 
                "document_size": document_size,
                "word_count": word_count,
                "authors": authors,
                "tech_tools": tech_tools
            }

            # Store metadata
            temp_store.store_metadata(metadata=metadata, file_name="metadata")

            return metadata
        
        # Handle comment with no attachement
        else:
            comment_content = comment_data['comment']
            authors = get_comment_authors(comment_title, comment_content)
            word_count = word_counter.word_counter(comment_content)
            tech_tools = get_tech_tools(comment_content)
            
            metadata = {
                "comment_id": comment_id,
                "comment_title": comment_title, 
                "file_url": "No attached document",
                "file_name": "Does not apply", 
                "file_size": "Does not apply",
                "word_count": word_count,
                "authors": authors,
                "tech_tools": tech_tools,
            }

            # store metadata
            output_file_name = "metadata"
            temp_store.store_metadata(metadata=metadata, file_name=output_file_name)

            return metadata
        
    else:
        raise HTTPException(status = response.status_code, message = f"failed to fetch comment{comment_id}")
    