from fastapi import HTTPException
from urllib.parse import urlparse
import urllib.request
from io import BytesIO
from PyPDF2 import PdfReader
from docx import Document

# count words in a word document
def count_words_in_txt(url):
    try:
        response = urllib.request.urlopen(url)
        if response.status == 200:
            # fetch text from url
            data = response.read()
            text = data.decode('utf-8')

            # count words in the text
            words = text.split()
            word_count = len(words)

            return word_count
        
        else:
            return HTTPException(status = response.status, detail = "Failed to fetch data from the attached word document")
        
    except Exception as e:
        raise ValueError(f"An error occurred: {str(e)}")
    
# count words in a word document
def count_words_in_word_document(url):
    try:
        response = urllib.request.urlopen(url)
        if response.status == 200:
            # fetch word document data from url
            data = response.read()
            file = BytesIO(data)

            # read document and count words
            doc = Document(file)
            word_count = 0
            for paragraph in doc.paragraphs:
                text = paragraph.text.split()
                word_count += len(text)

            return word_count
        
        else:
            return HTTPException(status = response.status, detail = "Failed to fetch data from the attached word document")
        
    except Exception as e:
        raise ValueError(f"An error occurred: {str(e)}")

# count words in a pdf document
def count_words_in_pdf(url):
    try:
        # fetch pdf content from the url
        response = urllib.request.urlopen(url)
        if response.status == 200:
            data = response.read() 
            file = BytesIO(data) # create a BytesIO object; it helps to work with a file as if it was on the disk

            # read file
            reader = PdfReader(file)
            pages = len(reader.pages) # Stores number of pages in the file
            word_count = 0

            # loop through file pages and count words
            for page in range(pages):
                page_data = reader.pages[page]
                text = page_data.extract_text()
                words = text.split()
                word_count += len(words)
            
            return word_count
        
        else:
            raise HTTPException(status = response.status, message = "Failed to fetch data from the attached pdf document")

    except Exception as e:
        raise ValueError(f"An error occurred: {str(e)}")

# Count total number of words in a comment
def count_words_in_attached_document(file_url):
    # count words in an attached document
    if file_url.endswith('.pdf'):
        word_count = count_words_in_pdf(file_url)

    elif file_url.endswith('.docx' or '.docm' or '.dotx'):
        word_count = count_words_in_word_document(file_url)
        
    elif file_url.endswith('.txt'):
        word_count = count_words_in_txt(file_url)

    else:
        raise HTTPException(status_code = 400, detail = "Unsupported file format")
    
    return word_count

def word_counter(comment):
    # check if comment has multiple attachments
    if isinstance(comment, list):
        word_count = 0
        
        # count total of words in all attached documents
        for single_comment in comment: 
            word_count += count_words_in_attached_document(single_comment)
        return word_count
    
    else:
        # check if the comment is a string
        is_url = urlparse(comment)

        # count words in a string if the comment has no attachment
        if not all([is_url.scheme, is_url.netloc]): 
            words = comment.split()
            word_count = len(words)
            return word_count
            
        else:
            return count_words_in_attached_document(comment)
