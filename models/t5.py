from transformers import T5ForConditionalGeneration, T5Tokenizer
from utils import data_extractor
# from langchain_core.prompts import PromptTemplate
# # from langchain_community.llms import VertexAI
# from langchain.chains.summarize import load_summarize_chain
# from langchain_google_vertexai import VertexAI

# vertex_llm_text = VertexAI(model_name =  "text-bison@001")

model_name = 'utrobinmv/t5_summary_en_ru_zh_base_2048'
model = T5ForConditionalGeneration.from_pretrained(model_name)
tokenizer = T5Tokenizer.from_pretrained(model_name)

""""
Summarization models
https://huggingface.co/Joemgu/mlong-t5-large-sumstew
https://huggingface.co/utrobinmv/t5_summary_en_ru_zh_base_2048
https://huggingface.co/yhavinga/t5-v1.1-large-dutch-cnn-test
https://huggingface.co/toloka/t5-large-for-text-aggregation
https://huggingface.co/sysresearch101/t5-large-finetuned-xsum-cnn
https://huggingface.co/Samuel-Fipps/t5-efficient-large-nl36_fine_tune_sum_V2
https://huggingface.co/stacked-summaries/flan-t5-large-stacked-samsum-1024
https://huggingface.co/mrm8488/flan-t5-large-finetuned-openai-summarize_from_feedback
https://huggingface.co/basic-go/FRED-T5-large-habr-summarizer

"""
def summarize(comment, max_length):        
    # Create text chunks
    chunks = data_extractor.create_text_chunks(comment, max_length)

    # Generate a brief summary 
    prefix = 'summary: '

    summary = [] # Stores summary content

    # Summarize and collect all summaries together
    for chunk in chunks:
        text = prefix + chunk
        input_ids = tokenizer(text, return_tensors="pt")

        # generate tokens
        generated_tokens = model.generate(**input_ids)
        summary.append(tokenizer.batch_decode(generated_tokens, skip_special_tokens=True))

    return summary

def summarize_briefly(comment, max_length):
    # Create text chunks
    chunks = data_extractor.create_text_chunks(comment, max_length)

    # Generate a brief summary 
    prefix = 'summary brief: '

    summary = [] # Stores summary content

    # Summarize and collect all summaries together
    for chunk in chunks:
        text = prefix + chunk
        input_ids = tokenizer(text, return_tensors="pt")

        # generate tokens
        generated_tokens = model.generate(**input_ids)
        summary.append(tokenizer.batch_decode(generated_tokens, skip_special_tokens=True))

    return summary


# Use refining method for a quality summary
def refined_summary(comment, pages):
    question_prompt_template = f"""
                  Please provide a summary of the following text.
                  TEXT: {comment}
                  SUMMARY:
                  """

    # question_prompt = PromptTemplate(
    #     template=question_prompt_template, input_variables=["text"]
    # )

    # refine_prompt_template = f"""
    #             Write a concise summary of the following text delimited by triple backquotes.
    #             Return your response in bullet points which covers the key points of the text.
    #             ```{comment}```
    #             BULLET POINT SUMMARY:
    #             """

    # refine_prompt = PromptTemplate(
    #     template=refine_prompt_template, input_variables=["text"]
    # )

    # refine_chain = load_summarize_chain(
    #     vertex_llm_text,
    #     chain_type = "refine",
    #     question_prompt = question_prompt,
    #     refine_prompt = refine_prompt,
    #     return_intermediate_steps = True,
    # )

    
    # refine_outputs = refine_chain({"input_documents": pages})


