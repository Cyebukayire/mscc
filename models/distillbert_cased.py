from transformers import pipeline

def question_answering(question, text):
    model ='distilbert-base-cased-distilled-squad'
    """TODO Models to try
    distilbert-base-cased-distilled-squad //tried
    
    """
    task = "question-answering"
    question_answerer = pipeline(task, model=model)
    # QA_input = {question, text}
    answer = question_answerer(question = question, context = text)

    return answer

