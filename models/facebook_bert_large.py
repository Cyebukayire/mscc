from transformers import pipeline, AutoTokenizer, BartForConditionalGeneration, BartTokenizer
from utils import data_extractor

# Define the model
model_name = "facebook/bart-large-cnn"
model = BartForConditionalGeneration.from_pretrained(model_name)
tokenizer = BartTokenizer.from_pretrained(
    'facebook/bart-large-cnn')

def summarize(comment, max_length = 1024):
    # Create pipeline
    summarizer = pipeline("summarization", model=model_name)

    # Create text chunks
    chunks = data_extractor.create_text_chunks(comment, max_length)

    summary = "" # Stores summary content

    # Summarize and collect all summaries together
    for chunk in chunks:
        summary = summary + " \n " + summarizer(chunk)[0]["summary_text"]

    return summary
