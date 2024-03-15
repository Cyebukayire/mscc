from transformers import AutoTokenizer, BartForConditionalGeneration

def summarizing(comment):
    # Define the model
    model_name = "facebook/bart-large-cnn"
    model = BartForConditionalGeneration.from_pretrained(model_name)

    # Create tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    inputs = tokenizer([(comment[:1024])], max_length=1024, return_tensors="pt")
    summary_ids = model.generate(inputs["input_ids"], num_beams=2, min_length=0, max_length=20)
    summary = tokenizer.batch_decode(summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]

    return summary