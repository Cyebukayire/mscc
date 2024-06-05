from bs4 import BeautifulSoup
import html

# Method to clean text
def clean_text(text):
    # Validate text
    if text is None:
        return None
    elif len(text) < 4:
        return text
    
    # Parse HTML and remove tags
    soup = BeautifulSoup(text, "html.parser")
    text_without_tags = soup.get_text()
    
    # Unescape HTML entities
    cleaned_text = html.unescape(text_without_tags)
    
    # Normalize newlines and strip leading/trailing whitespace
    cleaned_text = '\n'.join(line.strip() for line in cleaned_text.splitlines() if line.strip())
    
    return cleaned_text
