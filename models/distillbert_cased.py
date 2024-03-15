from transformers import pipeline

def question_answering(question, comment):
    # Declare the model and task to complete
    model ='distilbert-base-cased-distilled-squad'
    task = "question-answering"

    # Create pipleline for the model
    question_answerer = pipeline(task, model=model)

    # Generate answer
    answer = question_answerer(question = question, context = comment)

    return answer
