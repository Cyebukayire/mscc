from fastapi import HTTPException
from services import comments as comment_service
from utils import data_extractor, temp_store, word_counter
from utils.nlp_utils import get_comment_authors, get_tech_tools, get_cited_case_laws
import re, os, PyPDF2, glob
import json

# Retrieve metadata of a single comment
async def get_all_metadata():
        result = []
        # Loop through all comment objects in chunks
        for i in range(228, 228):
            # Format comment id
            comment_id = f"COLC-2023-0006-{i:04d}"

            # Fetch comment object
            response = comment_service.get_comment(comment_id=comment_id)

            # Store non-stored comment
            if response.status == 404:
                print(f"\n\nCOMMENT OBJECT MISSING: {comment_id}\n\n")
                # Initialize database file
                db_file = "/Users/peace/Developer/Machine Learning/Research/mscc/database/database.json"
                if os.path.exists(db_file):
                    with open(db_file, 'r') as file:
                        # Load JSON content
                        data = json.load(file)
                    
                    # Fetch comment data
                    response_obj = await comment_service.get_comment_with_url(comment_id)

                    # Check if the comment id exist
                    if response_obj.status_code != 200 : 
                        print(f"Skipped! Comment ID {comment_id}  Not Found\n")
                        return f"404, Request to access the comment {comment_id} failed."

                    # Load the comment object to JSON file
                    comment_object = response_obj.json()

                    # Add the new object to the existing data
                    data.append(comment_object)

                    # Write the updated data back to the JSON file
                    with open(db_file, 'w') as file:
                        json.dump(data, file, indent=4)

                    print(f"\n\nCOMMENT OBJECT ADDED: {comment_id}\n\n")
                else:
                    raise ValueError(f"Can't save the comment object: {comment_id} json db file not found")
            
            elif response.status != 200:
                raise Exception(response.status, response.message)

            # Extract simple metadata first
            comment_content = fetch_comment_content_from_db(comment_id)
            comment_title, comment_size = get_simple_metadata(comment_object=response.data, comment_content=comment_content)

            # Extract advanced metadata
            # authors = get_comment_authors(comment_title=comment_title, comment_content=comment_content)
            # tech_tools = get_tech_tools(comment_content=comment_content)
            # cited_case_laws = get_cited_case_laws(comment_content=comment_content)

            # Temporarily store metadata in excel file
            metadata = {
                "comment_id": comment_id,
                "comment_title": comment_title,
                "comment_size": comment_size,
                # "authors": authors,
                # "tech_tools": tech_tools,
                # "cited_case_laws": cited_case_laws
            }
            print("\n\nMETADATA\n\n", metadata, "\n\n")
            result.append(metadata)

            # Store metadata
            temp_store.store_metadata(metadata=metadata, file_name="all_metadata")
            
        return result

# Get comment size
def get_comment_size(comment_content: str):
    # Count words with regex for more accurate word matching
    # words = re.findall(r'\b\w+\b', comment_content)
    words = comment_content.split()
    word_count = len(words)

    # Return word count
    return word_count
         

# Extract all simple metadata
def get_simple_metadata(comment_object: object, comment_content: str):
    # Get metadata
    comment_data = comment_object['data']['attributes']
    comment_title = comment_data['title']
    comment_size = get_comment_size(comment_content=comment_content)

    # Return metadata
    return comment_title, comment_size


# Fetch comment content from database
def fetch_comment_content_from_db(comment_id: str):
    database_path = os.path.join('/Users/peace/Developer/Machine Learning/Research/mscc/database/comments', f'{comment_id}')

    # Verify that the directory exists
    if not os.path.isdir(database_path):
        raise Exception(f"Directory does not exist: {database_path}")

    comment = ""
    
    # Iterate through files in the folder
    for comment_path in glob.glob(os.path.join(database_path, '*')):
        # Check if it's a text file
        if comment_path.endswith('.txt'):
            with open(comment_path, 'r', encoding='utf-8') as file:
                comment += (file.read())

        # Check if it's a PDF file
        elif comment_path.endswith('.pdf'):
            with open(comment_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                data = ''
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    data += page.extract_text()

                comment += data

    return comment
