from fastapi import HTTPException
from urllib.parse import urlparse
import urllib.request
from io import BytesIO
from PyPDF2 import PdfReader
from docx import Document
import pandas as pd 

# extract text from an excel document
def extract_text_from_excel(url):
    try:
        response = urllib.request.urlopen(url)
        if response.status == 200:
            excel_data = pd.read_excel(url)
            
            # Convert each sheet to text
            text = ""
            for sheet_name, df in excel_data.items():
                text += f"--- Sheet: {sheet_name} ---\n"
                text += df.to_string(index=False) + "\n\n"

            return text
        
        else:
            return HTTPException(status = response.status, detail = "Failed to fetch data from an attached excel document")
    
    except Exception as e:
        raise ValueError(f"An error occurred: {str(e)}")
    
# extract text from a txt document
def extract_text_from_txt(url):
    try:
        response = urllib.request.urlopen(url)
        if response.status == 200:
            # fetch text from url
            data = response.read()
            text = data.decode('utf-8')
            return text
        
        else:
            return HTTPException(status = response.status, detail = "Failed to fetch data from an attached txt document")
        
    except Exception as e:
        raise ValueError(f"An error occurred: {str(e)}")
    
# extract text from a word document
def extract_text_from_word_document(url):
    try:
        response = urllib.request.urlopen(url)
        if response.status == 200:
            # fetch word document data from url
            data = response.read()
            file = BytesIO(data)

            # read document and extract text
            doc = Document(file)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text

            return text
        
        else:
            return HTTPException(status = response.status, detail = "Failed to fetch data from the attached word document")
        
    except Exception as e:
        raise ValueError(f"An error occurred: {str(e)}")

# extract text from a pdf document
def extract_text_from_pdf(url):
    try:
        # fetch pdf content from the url
        response = urllib.request.urlopen(url)
        if response.status == 200:
            data = response.read() 
            file = BytesIO(data) # create a BytesIO object; it helps to work with a file as if it was on the disk

            # read file
            reader = PdfReader(file)
            pages = len(reader.pages) # Stores number of pages in the file
            text = ""

            # loop through file pages and extract text
            for page in range(pages):
                page_data = reader.pages[page]
                text += page_data.extract_text()
            
            return text
        
        else:
            raise HTTPException(status = response.status, message = "Failed to fetch data from the attached pdf document")

    except Exception as e:
        raise ValueError(f"An error occurred: {str(e)}")

# Extract text from an attachmed document
def extract_text_from_attached_document(file_url):
    text = ""
    # check document format
    if file_url.endswith('.pdf'):
        text = extract_text_from_pdf(file_url)

    elif file_url.endswith('.docx' or '.docm' or '.dotx'):
        text = extract_text_from_word_document(file_url)
        
    elif file_url.endswith('.txt'):
        text = extract_text_from_txt(file_url)
    
    elif file_url.endswith('.xlsx'):
        text = extract_text_from_excel(file_url)

    elif not file_url.endswith('.jpg' or '.jpeg' or '.png'or '.gif' or '.tiff' or '.tif' or '.bmp' or '.webp' or '.svg' or '.heic' or '.heif' or '.raw' or 'psd'):
        raise HTTPException(status_code = 400, detail = "Unsupported file format")
    
    return text

def text_extractor(comment):
    # check if comment has multiple attachments
    if isinstance(comment, list):
        text = ""
        # extract text from all attached documents
        for comment_url in comment: 
            is_url = urlparse(comment_url)
            if all([is_url.scheme, is_url.netloc]):
                text += extract_text_from_attached_document(comment_url)
            else:
                raise ValueError("Error during text extraction: Invalid file url")
            
        return text
    
    elif isinstance(comment, str):
        return comment
    
    else:
        raise ValueError("Error: Invalid comment format")
