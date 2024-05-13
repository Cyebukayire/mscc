import asyncio
import os
import json
import httpx
from fpdf import FPDF
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
# from services.comments import get_comment 

# Initialize database file
db_file = "/Users/peace/Developer/Machine Learning/Research/mscc/database/database.json"

# Get a comment from Regulations.gov API 
async def get_comment(comment_id):
    regulations_api_key = "fUhDOvth3SkvSvVWLym8oJfQHc5CKbHqv92gPanf"
    async with httpx.AsyncClient() as client:
        comment_api = f"https://api.regulations.gov/v4/documents/{comment_id}?include=attachments&api_key={regulations_api_key}"
        response = await client.get(comment_api)
        return response

# Download the whole dataset
async def download_comments(db_file):
    if os.path.exists(db_file):
        with open(db_file, 'r') as file:
            # Load JSON content
            data = json.load(file)

        # Load comment content
        for i in range(1, 500):
            comment_id = f"{i:04d}"
            print("ID ", comment_id)

            # Fetch comment data
            response = await get_comment("COLC-2023-0006-"+comment_id)

            # Check if the comment id exist
            if response.status_code != 200 : 
                print(f"Kipped! Comment ID {comment_id}  Not Found\n")
                continue

            # Load the comment object to JSON file
            comment_object = response.json()

            # Add the new object to the existing data
            data.append(comment_object)

            # Extract comment content in a pdf file
            if not ('included'in comment_object): # Comment with no attachment
                print(f"Comment {comment_id} has No attachment!")
                # print("\n\n",comment_object,"\n\n\n")
                comment_content = comment_object['data']['attributes']['comment']

                # Store the comment in a pdf 
                if comment_content is None:
                    comment_document = comment_object['data']['attributes']['fileFormats'][0]

                    print("COMMENT MISSED!")
                    # Check for other attached documents (Some documents are not marked as attachments in the API)
                    if comment_document['format'] == 'pdf':
                        print(f"{comment_id} has a pdf document attached instead!")
                    else:
                        print(f"{comment_id} has a {comment_document['format']} document attached instead")

                else:
                    create_pdf(comment_content=comment_content, comment_id = "COLC-2023-0006-"+comment_id)
            
            else: # Comment with attachment(s)
                print(f"{comment_id} has attachment!")
                # download_attachment()
            
        # Write the updated data back to the JSON file
        with open(db_file, 'w') as file:
            json.dump(data, file, indent=4)
        
    else:
        print(f"Error: Database File not found {db_file}")

# Create pdf file
def create_pdf(comment_content, comment_id, file_name = None):
    # Validate comment content
    if not comment_content.strip():
        print("Error: No content provided. Pdf file not created!")
        return
    
    # Create pdf document
    current_directory = os.path.dirname(os.path.realpath(__file__))

    # Construct the path to "../database/comments" directory
    comments_directory = os.path.join(current_directory, '..', 'database', 'comments', f'{comment_id}')
    
    # Create directory
    if not os.path.exists(comments_directory):
        os.makedirs(comments_directory)
    
    # Create temporary txt document to store the comment
    txt_file_path = os.path.join(comments_directory, f'comment.txt')
    save_to_text_file(txt_file_path, comment_content)

def save_to_text_file(file_path, data):
    with open(file_path, 'x') as file: # File is created if it doesn't exist
        file.write(data)

# # Fetch comment content
# def download_comment(file_url, comment_id):
#     # check document format
#     if file_url.endswith('.pdf'):
#         download_pdf(file_url, comment_id)
        
#     elif file_url.endswith('.docx' or '.docm' or '.dotx'):
#         word_document_to_pdf(file_url)
        
#     elif file_url.endswith('.txt'):
#         txt_to_pdf(file_url)
    
#     elif file_url.endswith('.xlsx'):
#         excel_to_pdf(file_url)

#     elif not file_url.endswith('.jpg' or '.jpeg' or '.png'or '.gif' or '.tiff' or '.tif' or '.bmp' or '.webp' or '.svg' or '.heic' or '.heif' or '.raw' or 'psd'):
#         raise HTTPException(status_code = 400, detail = "Unsupported file format")    

# def download_pdf(file_url, comment_id):
#     current_directory = os.path.dirname(os.path.realpath(__file__))
    
#     # Construct the path to the "../database/comments" directory
#     comments_directory = os.path.join(current_directory, '..', 'database', 'comments', f'{comment_id}')
#     if not os.path.exists(comments_directory):
#         os.makedirs(comments_directory)

#     # docx_filename = os.path.join(comments_directory, f"{id}")
#     pdf_filename = os.path.join(comments_directory, f"{id}")

#     print(f"Downloaded {comment_id} Successfully!")

asyncio.run(download_comments(db_file))