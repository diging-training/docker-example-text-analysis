import pytesseract
from PIL import Image
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
import os

os.environ['JAVAHOME'] = '/usr/bin/java'

# call tesseract and OCR image
ocr_text = pytesseract.image_to_string(Image.open('testimage.png'))

st = StanfordNERTagger(r'/stanford-ner/stanford-ner-2020-11-17/classifiers/english.all.3class.distsim.crf.ser.gz',
                       r'/stanford-ner/stanford-ner-2020-11-17/stanford-ner.jar',
                       encoding='utf-8')

# tokenize and tag text
tokenized_text = word_tokenize(ocr_text)
found_tokens = st.tag(tokenized_text)

print("Attempting to classify:")
print(ocr_text)
print("======================")

prev_token = []
prev_token_type = None
# iterate over all tags
for token in found_tokens:
    # we are looking for compound words here 
    # (is there already a tag right before this one with the same type?)
    if prev_token:
        # if the current tag is 0, print what we found before
        if token[1] == 'O':
            print('{} ({})'.format(' '.join([t[0] for t in prev_token]), prev_token[0][1]))
            prev_token = []
            prev_token_type = None
            continue
        # if there is a new tag type, print the previous one
        elif prev_token_type != token[1]:
            print('{} ({})'.format(' '.join([t[0] for t in prev_token]), prev_token[0][1]))
            prev_token = [token]
            prev_token_type = token[1]
            continue
    
    # in all other cases, if the term was tagged store it
    if token[1] != 'O':
        prev_token.append(token)
        prev_token_type = token[1]

