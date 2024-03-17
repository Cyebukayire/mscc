from transformers import pipeline

def summarize(comment):
    model_name = "sshleifer/distilbart-cnn-12-6"# Very large and heavy
    
    # Create pipeline for the model
    summarizer = pipeline("summarization", model=model_name)

    # Summarize the comment
    summary = summarizer(comment)
    
    return summary