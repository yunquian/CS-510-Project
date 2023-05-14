"""


```
import spacy

# Load English tokenizer, tagger, parser and NER
nlp = spacy.load("en_core_web_sm")

# Process whole documents
text = ("When Sebastian Thrun started working on self-driving cars at "
        "Google in 2007, few people outside of the company took him "
        "seriously. “I can tell you very senior CEOs of major American "
        "car companies would shake my hand and turn away because I wasn’t "
        "worth talking to,” said Thrun, in an interview with Recode earlier "
        "this week.")
doc = nlp(text)

# Analyze syntax
print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])

# Find named entities, phrases and concepts
for entity in doc.ents:
    print(entity.text, entity.label_)
```

"""

import heapq
import re

import spacy
import pytextrank


_nlp = spacy.load('en_core_web_sm')

_nlp.add_pipe("textrank")


def extract_frequent_phrases(doc, k=10, lowercase=True):
    if lowercase:
        doc = doc.lower()
    doc = _nlp(doc)
    all_phrases = [
        (phrase.rank, phrase.count, phrase.text)
        for phrase in doc._.phrases
    ]
    if k is None:
        all_phrases = sorted(all_phrases, reverse=True)
    else:
        all_phrases = heapq.nlargest(k, all_phrases)
    return [item[2] for item in all_phrases]

    # for phrase in doc._.phrases:
    #     print(phrase.text)
    #     print(phrase.rank, phrase.count)
    #     print(phrase.chunks)


def remove_non_ascii_chars(text):
    return re.sub('[\u0080-\uFFFF\n]+', ' ', text)




def normalize(model: spacy.language.Language,
              text, lowercase=False, remove_stopwords=False):
    stops = model.Defaults.stop_words
    if lowercase:
        text = text.lower()
    text = model(text)
    lemmatized = list()
    for word in text:
        lemma = word.lemma_.strip()
        if lemma:
            if not remove_stopwords or (
                    remove_stopwords and lemma not in stops):
                lemmatized.append(lemma)
    return " ".join(lemmatized)


def extract_nouns_from_short_text(text, remove_stopwords=True):
    text = remove_non_ascii_chars(text)
    with _nlp.select_pipes(disable=["textrank"]):
        doc = _nlp(text)
    if remove_stopwords:
        stops = _nlp.Defaults.stop_words
        ret = []
        for chunk in doc.noun_chunks:
            noun = []
            for word in chunk:
                lemma = word.lemma_.strip()
                if lemma and lemma not in stops:
                    noun.append(word.text.strip())
            ret.append(' '.join(noun))
    return [chunk.text for chunk in doc.noun_chunks]


def extract_concepts_from_document(text):
    text = remove_non_ascii_chars(text)
    return extract_frequent_phrases(text)
