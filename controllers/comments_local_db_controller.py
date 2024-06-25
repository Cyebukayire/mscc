from services import comments as comment_service
from utils import temp_store, clean_data, entity_classification
from utils.nlp_utils import get_comment_authors, get_tech_tools, get_cited_case_laws
import os, PyPDF2, glob
import json
from config.config import settings
import pandas as pd
import ast
from collections import Counter

# Define output file path
output_file = f"{settings.OUTPUT_PATH}updated_all_metadata.xlsx"

async def get_all_metadata():
        # Loop through all comment objects
        for i in range(1, 10375):
            # Skip withdrawn comments
            if i == 1676 or i == 2951 or i == 9088:
                continue
            
            # Format comment id
            comment_id = f"COLC-2023-0006-{i:04d}"

            # Fetch comment object
            response = comment_service.get_comment(comment_id=comment_id)

            response_status = response.status
            response_message = response.message
            response_data = response.data

            # Store a missing comment object in db
            if response_status == 404:
                # Initialize database file
                db_file = f"{settings.LOCAL_DB_PATH}database.json"
                if os.path.exists(db_file):
                    with open(db_file, 'r') as file:
                        # Load JSON content
                        data = json.load(file)
                    
                    # Fetch comment data
                    response_obj = await comment_service.get_comment_with_url(comment_id)

                    # Check if the comment id exist
                    if response_obj.status_code != 200 : 
                        return f"404, Request to access the comment {comment_id} failed."

                    # Load the comment object to JSON file
                    response_data = response_obj.json()

                    # Add the new object to the existing data
                    data.append(response_data)

                    # Write the updated data back to the JSON file
                    with open(db_file, 'w') as file:
                        json.dump(data, file, indent=4)

                else:
                    raise ValueError(f"Can't save the comment object: {comment_id} json db file not found")
            
            elif response_status != 200:
                raise Exception(response_status, response_message)

            # Extract simple metadata first
            comment_content = clean_data.clean_text(fetch_comment_content_from_db(comment_id))
            comment_title, attachment_title, comment_size = get_simple_metadata(comment_object=response_data, comment_content=comment_content)

            # Merge comment title with attachment title(s)
            merged_titles = comment_title +'. '+ ', '.join(attachment_title)
            clean_merged_titles = clean_data.clean_text(merged_titles)

            # Extract advanced metadata
            authors = get_comment_authors(title=clean_merged_titles, comment_content=comment_content)
            tech_tools = get_tech_tools(comment_content=comment_content)
            cited_case_laws = get_cited_case_laws(comment_content=comment_content)

            # Temporarily store metadata in excel file
            metadata = {
                "comment_id": comment_id,
                "comment_title": comment_title,
                "comment_size": comment_size,
                "attachment_title": attachment_title,
                "authors": authors,
                "tech_tools": tech_tools,
                "cited_case_laws": cited_case_laws
            }

            # Store metadata
            temp_store.store_metadata(metadata=metadata, file_name="all_metadata")
            
        return "Metadata Extracted Successfully!"
        # return metadata

# Get comment size
def get_comment_size(comment_content: str):
    words = comment_content.split()
    word_count = len(words)

    # Return word count
    return word_count
         

# Extract all simple metadata
def get_simple_metadata(comment_object: object, comment_content: str):
    # Get metadata
    comment_data = comment_object['data']['attributes']
    comment_size = get_comment_size(comment_content=comment_content)
    comment_title = comment_data['title']
    attachment_title = []

    # Add data from title of attached document(s)
    has_attachment = 'included'in comment_object
    if has_attachment:
        # Collect titles from multiple attached documents if any
        for attachment in comment_object["included"]:
            attachment_title.append(attachment['attributes']['title'])

    # Return metadata
    return comment_title, attachment_title, comment_size


# Fetch comment content from database
def fetch_comment_content_from_db(comment_id: str):
    database_path = os.path.join(f'{settings.LOCAL_DB_PATH}comments', f'{comment_id}')

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

# Method to update comment entity
def update_comment_entity():
    # Load the data from file
    df = pd.read_excel(output_file)

    # Create 'entity column'
    df['entity'] =  df['comment_title'].apply(entity_classification.determine_entity)

    # Save updates
    try:
        df.to_excel(output_file, index = False)
        
        if os.path.isfile(output_file):
            return "Entity updated successfully!"
        
        else:
            return "Error: Changes were not saved successfully!"

    except Exception as e:
        return e
    
# Method to get all cited case laws
def get_cited_case_laws():
    # Collect all citations
    df = pd.read_excel(output_file, sheet_name=0)

    # Get all cited case laws
    citations = df["cited_case_laws"]

    # Convert citations from string to a python list
    citation_list = pd.DataFrame(citations)['cited_case_laws'].apply(ast.literal_eval)

    # Combine all lists
    all_cited_case_laws = sum(citation_list, [])

    return all_cited_case_laws