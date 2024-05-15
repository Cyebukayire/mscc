from fastapi import HTTPException
import asyncio
import os
import json
import httpx
from fpdf import FPDF
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
<<<<<<< HEAD
import requests
from docx2pdf import convert
import urllib.request
=======
>>>>>>> origin/main
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
<<<<<<< HEAD


# Create database file path
def create_path(folder_name, file_name=None):
    # Get current directory
    current_directory = os.path.dirname(os.path.realpath(__file__))

    # Construct the path
    folder_path = os.path.join(current_directory, '..', 'database', 'comments', f'{folder_name}')
    
    # Create directory
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    if file_name is None:
        return folder_path
    
    # Create the file
    file_path = os.path.join(folder_path, f'{file_name}')

    return file_path


# Download all comments
=======

# Download the whole dataset
>>>>>>> origin/main
async def download_comments(db_file):
    if os.path.exists(db_file):
        with open(db_file, 'r') as file:
            # Load JSON content
            data = json.load(file)

        # Load comment content
        for i in range(1, 500):
<<<<<<< HEAD
            comment_id = f"COLC-2023-0006-{i:04d}"
            print("ID ", comment_id)

            # Fetch comment data
            response = await get_comment(comment_id)
=======
            comment_id = f"{i:04d}"
            print("ID ", comment_id)

            # Fetch comment data
            response = await get_comment("COLC-2023-0006-"+comment_id)
>>>>>>> origin/main

            # Check if the comment id exist
            if response.status_code != 200 : 
                print(f"Kipped! Comment ID {comment_id}  Not Found\n")
                continue

            # Load the comment object to JSON file
            comment_object = response.json()

            # Add the new object to the existing data
            data.append(comment_object)

<<<<<<< HEAD
            # Extract comment content
            comment_content = comment_object['data']['attributes']['comment']
            if comment_content is None:
                attachment_obj = comment_object['data']['attributes']['fileFormats'][0]
                file_url = attachment_obj['fileUrl']
                folder_path = create_path(folder_name=comment_id)
                download_attachment(file_url=file_url, folder_path=folder_path, file_name=comment_id)
            
            else: # Comments posted as text
                file_path = create_path(folder_name= comment_id, file_name=comment_id+".txt")
                save_to_txt_file(file_path = file_path, data=comment_content)
        
            # Download all attached document(s)
            if('included'in comment_object): 
                for attachment_obj in comment_object['included']:
                    file_url = attachment_obj['attributes']['fileFormats'][0]['fileUrl']
                    folder_path = create_path(folder_name=comment_id)
                    file_name= attachment_obj['attributes']['title']
                    download_attachment(file_url=file_url, folder_path=folder_path, file_name=file_name)
=======
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
>>>>>>> origin/main
            
        # Write the updated data back to the JSON file
        with open(db_file, 'w') as file:
            json.dump(data, file, indent=4)
        
    else:
        print(f"Error: Database File not found {db_file}")

<<<<<<< HEAD

def save_to_txt_file(file_path, data):
    with open(file_path, 'w') as file: # File is created if it doesn't exist
        file.write(data)

def download(file_url, file_path):
    
    # Download the pdf file
    response = requests.get(file_url)

    with open(file_path, 'wb') as attachment:
        attachment.write(response.content)

# Download word document from url
def download_docx_from_url(url, file_path):
    response = requests.get(url)
    with open(file_path, 'wb') as f:
        f.write(response.content)

# Convert word document to pdf to prevent data loss
def convert_docx_to_pdf(docx_file_path, pdf_file_path):
    convert(docx_file_path, pdf_file_path)

# Convert word document to pdf
def word_document_to_pdf(word_file_url, pdf_file_path):
    try:
        # Verify the url
        response = urllib.request.urlopen(word_file_url)
        if response.status == 200:
            # Download the documnet temporarily as the word document file 
            current_directory = os.path.dirname(os.path.realpath(__file__))
            temp_docx_file_path = os.path.join(current_directory, "word_comment.docx") 
            download_docx_from_url(word_file_url, temp_docx_file_path)

            # Convert the downloaded word document to pdf
            convert_docx_to_pdf(temp_docx_file_path, pdf_file_path)

            # Delete temporary word file
            if os.path.exists(temp_docx_file_path):
                os.remove(temp_docx_file_path)
        
        else:
            return HTTPException(status = response.status, detail = "Failed to fetch data from the attached word document")
    
    except Exception as e:
        raise ValueError(f"An error occurred: {str(e)}")
    
def extract_file_format(url):
    # Get last string that comes after /
    file_name = url.split('/')[-1]

    # Extract file extension (split the filename by .)
    file_extension = os.path.splitext(file_name)[1]

    # Get file format
    file_format = file_extension[1:]

    return file_format

# Download comment attachments
def download_attachment(file_url, folder_path, file_name):
    # Get file format
    file_format = extract_file_format(file_url)

    # Download attached document(s)
    if file_format in ['pdf', 'txt', 'xlsx', 'jpg', 'gif', 'png', 'jpeg', 'heif', 'psd', 'raw' , 'heic', 'svg' , 'bmp']:
        file_path = os.path.join(folder_path, f'{file_name}.{file_format}')
        download(file_url=file_url, file_path=file_path)
        
    elif file_format in ['docx', 'docm', 'dotx']:
        file_path = os.path.join(folder_path, f'{file_name}.pdf')
        word_document_to_pdf(word_file_url=file_url, pdf_file_path=file_path)
        
    else: # TODO work for 'tif','tiff', 'webp', data extraction
        raise HTTPException(status_code = 400, detail = "Unsupported file format: " + file_url)    
=======
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
>>>>>>> origin/main

asyncio.run(download_comments(db_file))