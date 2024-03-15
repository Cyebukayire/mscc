from transformers import pipeline

def summarizing(comment):
    model_name = "sshleifer/distilbart-cnn-12-6"
    
    # Create the pipeline for the model
    summarizer = pipeline("summarization", model=model_name)

    # Summarize the comment
    summary = summarizer(comment)
    
    return summary