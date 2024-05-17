from fastapi import HTTPException
import asyncio
import os
import json
import httpx
from fpdf import FPDF
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import requests
from docx2pdf import convert
import urllib.request
import pypandoc
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
async def download_comments(db_file):
    if os.path.exists(db_file):
        with open(db_file, 'r') as file:
            # Load JSON content
            data = json.load(file)

        # Load comment content
        for i in range(9089, 9301):
            comment_id = f"COLC-2023-0006-{i:04d}"
            print("ID ", comment_id)

            # Fetch comment data
            response = await get_comment(comment_id)

            # Check if the comment id exist
            if response.status_code != 200 : 
                print(f"Skipped! Comment ID {comment_id}  Not Found\n")
                continue

            # Load the comment object to JSON file
            comment_object = response.json()

            # Add the new object to the existing data
            data.append(comment_object)

            # Extract comment content
            has_attachment = 'included'in comment_object
            comment_content = comment_object['data']['attributes']['comment']
            if comment_content is None:
                if comment_object['data']['attributes']['fileFormats'] is not None:
                    attachment_obj = comment_object['data']['attributes']['fileFormats'][0]
                    file_url = attachment_obj['fileUrl']
                    folder_path = create_path(folder_name=comment_id)
                    download_attachment(file_url=file_url, folder_path=folder_path, file_name=comment_id)
                
                elif not 'included'in comment_object:
                    raise ValueError(f"An error occurred: {str(comment_id)} has neither comment nor attachment")
            
            else: # Comments posted as text
                file_path = create_path(folder_name= comment_id, file_name=comment_id+".txt")
                save_to_txt_file(file_path = file_path, data=comment_content)
        
            # Download all attached document(s)
            if(has_attachment): 
                for attachment_obj in comment_object['included']:
                    file_url = attachment_obj['attributes']['fileFormats'][0]['fileUrl']
                    folder_path = create_path(folder_name=comment_id)
                    file_name= attachment_obj['attributes']['title']
                    download_attachment(file_url=file_url, folder_path=folder_path, file_name=file_name)
            
        # Write the updated data back to the JSON file
        with open(db_file, 'w') as file:
            json.dump(data, file, indent=4)
        
    else:
        print(f"Error: Database File not found {db_file}")


def save_to_txt_file(file_path, data):
    with open(file_path, 'w') as file: # File is created if it doesn't exist
        file.write(data)

def extract_file_content(file_url):
    # Download the pdf file
    response = requests.get(file_url)

    # Get comment content
    data = response.content

    return data

def download(file_url, file_path):
    
    data = extract_file_content(file_url)

    with open(file_path, 'wb') as attachment:
        attachment.write(data)

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

def check_pandoc_installation():
    try:
        # Try a simple conversion to check if Pandoc is installed
        pypandoc.convert_text("", 'plain', format='rtf')

    except OSError:
        # Pandoc is not installed, download it
        pypandoc.download_pandoc()

def rtf_document_to_txt(rtf_url, txt_file_path):
    # Extract content
    data_in_bytes = extract_file_content(file_url = rtf_url)

    decoded_data = data_in_bytes.decode('utf-8')
    
    plain_text = pypandoc.convert_text(decoded_data, 'plain', format='rtf')

    # Save data
    save_to_txt_file(file_path=txt_file_path, data=plain_text)
    

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
    if file_format in ['pdf', 'txt', 'xlsx', 'jpg', 'gif', 'png', 'jpeg', 'heif', 'psd', 'raw' , 'heic', 'svg' , 'bmp', 'tif','tiff']:
        file_path = os.path.join(folder_path, f'{file_name}.{file_format}')
        download(file_url=file_url, file_path=file_path)
        
    elif file_format in ['docx', 'docm', 'dotx']:
        file_path = os.path.join(folder_path, f'{file_name}.pdf')
        word_document_to_pdf(word_file_url=file_url, pdf_file_path=file_path)
    
    elif file_format in ['rtf']:
        file_path = os.path.join(folder_path, f'{file_name}.txt')
        rtf_document_to_txt(rtf_url=file_url, txt_file_path=file_path)

    else: # TODO work for 'webp' data extraction
        raise HTTPException(status_code = 400, detail = "Unsupported file format: " + file_url)    

asyncio.run(download_comments(db_file))