from transformers import pipeline, AutoTokenizer, BartForConditionalGeneration, BartTokenizer
from utils import data_extractor

# Define the model
model_name = "facebook/bart-large-cnn"
model = BartForConditionalGeneration.from_pretrained(model_name)
tokenizer = BartTokenizer.from_pretrained(
    'facebook/bart-large-cnn')

def summarize(comment):
    # Create pipeline
    summarizer = pipeline("summarization", model=model_name)

    # Create text chunks
    chunks = data_extractor.create_text_chunks(comment)

    summary = [] # Stores summary

    for chunk in chunks:
        summary.append(summarizer(chunk))

    return summary
