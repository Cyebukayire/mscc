from transformers import BartForQuestionAnswering, BartTokenizer
import torch


# BART Model using pytorch
def question_answering(question, comment):
    tokenizer = BartTokenizer.from_pretrained('valhalla/bart-large-finetuned-squadv1')
    model = BartForQuestionAnswering.from_pretrained('valhalla/bart-large-finetuned-squadv1')
    
    # Limit large document input
    if len(comment) > 1024:
        raise ValueError("Error: Large Comment Input to BART")

    answers = []

    encoding = tokenizer(question, comment, return_tensors='pt')
    input_ids = encoding['input_ids']
    attention_mask = encoding['attention_mask']

    start_scores, end_scores = model(input_ids, attention_mask=attention_mask, output_attentions=False)[:2]

    all_tokens = tokenizer.convert_ids_to_tokens(input_ids[0])
    answer = ' '.join(all_tokens[torch.argmax(start_scores): torch.argmax(end_scores) + 1])
    answer = tokenizer.convert_tokens_to_ids(answer.split())
    answer = tokenizer.decode(answer)
    answers.append(answer)

    return answers