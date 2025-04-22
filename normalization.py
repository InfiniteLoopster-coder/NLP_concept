# Example with spaCy
import spacy
nlp = spacy.load("en_core_web_sm")
doc = nlp("The striped bats were hanging on their feet for best.")
print([token.lemma_.lower() for token in doc
       if not token.is_stop and token.is_alpha])
# → ['striped', 'bat', 'hang', 'foot', 'best']
