from docx import Document
from io import BytesIO
from PyPDF2 import PdfReader
import magic
from rest_framework.exceptions import ValidationError

# Extract Metadata
class Metadata():
    # Function to count words in a PDF file
    def count_words_in_pdf(self, file_content):
        try:
            pdf_reader = PdfReader(BytesIO(file_content))
            num_words = 0
            for page in pdf_reader.pages:
                num_words += len(page.extract_text().split())
            return num_words
        except Exception as e:
            # Handle any exceptions or errors that may occur during word count
            raise ValidationError(detail={'error': f"Error counting words in PDF file: {e}"})
    
    # Function to count words in a text file
    def count_words_in_text(self, file_content):
        try:
            text_content = file_content.decode('utf-8')  # Decode bytes to text
            return len(text_content.split())  # Count words using spaces as delimiters
        except Exception as e:
            # Handle any exceptions or errors that may occur during word count
            raise ValidationError(detail={'error': f"Error counting words in TXT file: {e}"})
        
    # Function to count words in a DOCX file using python-docx
    def count_words_in_docx(self, file_content):
        try:
            docx_file = BytesIO(file_content)
            doc = Document(docx_file)
            total_words = sum(len(p.text.split()) for p in doc.paragraphs)
            return total_words
        except Exception as e:
            # Handle any exceptions or errors that may occur during word count
            raise ValidationError(detail={'error': f"Error counting words in DOCX file: {e}"})
        
    # Function to handle unsupported file types
    def handle_unsupported_file(self, file_extension):
        error_message = f"Unsupported file type: {file_extension}. Only PDF, DOCX, and TXT are supported."

        # Raise a validation error with the error message
        raise ValidationError(detail={'error': error_message})

    # Function to count words and measure file size
    def counter(self, file, file_name):
        # Find file extension
        file_extension = file_name.split('.')[-1].lower()

        # Determine file type using 'magic' library
        file_mime = magic.from_buffer(file.read(1024), mime=True)
        file.seek(0)

        if file_mime == 'application/pdf' or file_extension == 'pdf':
            pdf_content = file.read()
            word_count = self.count_words_in_pdf(pdf_content)
            file_size = len(pdf_content)
        elif file_extension == 'txt':
            text_content = file.read()
            word_count = self.count_words_in_text(text_content)
            file_size = len(text_content)
        elif file_extension == 'docx':
            docx_content = file.read()
            word_count = self.count_words_in_docx(docx_content)
            file_size = len(docx_content)
        else:
            # Handle unsupported file types
            self.handle_unsupported_file(file_extension)

        return word_count, file_size

    # Function to extract comment id
    def extract_id_from_filename(self, filename):
        name = filename.split('_')
        for id in name:
            if '-' in id and len(id) == 19:
                return id
        raise ValueError("ID not found in the filename")  # Raise exception if ID is not found

    # Extract all metadata
    def extract_all(self, validated_data):
        file = validated_data.get('file')
        file_name = file.name
        word_count, file_size = self.counter(file, file_name)

        # Extract comment id
        try:   
            id = self.extract_id_from_filename(file_name)
            print(id)
        except ValueError as e:
            print(e)

        # Convert file size to Kilobytes
        file_size_kb = file_size / 1024

        # Return the metadata values
        return {
            'id': id,
            'file_name': file_name,
            'title': "none",
            'file_size': file_size_kb,
            'word_count': word_count,
        }
