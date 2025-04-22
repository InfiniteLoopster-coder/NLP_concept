# Word‑level with NLTK
from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt_tab')

text = "Text preprocessing is fun!"
print(word_tokenize(text))
# → ['Text', 'preprocessing', 'is', 'fun', '!']

# Subword‑level with Hugging Face
from transformers import AutoTokenizer
tok = AutoTokenizer.from_pretrained("bert-base-uncased")
print(tok.tokenize("Text preprocessing is fun!"))
# → ['text', 'pre', '##process', '##ing', 'is', 'fun', '!']