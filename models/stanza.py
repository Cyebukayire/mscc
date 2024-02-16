import stanza

# initialize stanza pipeline
pipeline = stanza.Pipeline(lang='en', processors= 'tokenize, lemma')

# Stanza sentence tokenizer
def sentense_tokenizer(comment_content):
    return [sentence.text for sentence in comment_content.sentences]
