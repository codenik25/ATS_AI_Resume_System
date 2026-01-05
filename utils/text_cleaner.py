import re
import spacy

nlp = spacy.load("en_core_web_sm")

def clean_text(text):
    # Lowercase
    text = text.lower()

    # Remove email & phone
    text = re.sub(r'\S+@\S+', ' ', text)
    text = re.sub(r'\d{10}', ' ', text)

    # Remove special characters
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)

    # NLP processing
    doc = nlp(text)

    tokens = []
    for token in doc:
        if not token.is_stop and not token.is_punct:
            tokens.append(token.lemma_)

    return " ".join(tokens)
