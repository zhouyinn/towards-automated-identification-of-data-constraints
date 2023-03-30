import spacy
from spacy.language import Language


@Language.component("merge_punct")
def merge_punct(doc):
    spans = []
    for word in doc[:-1]:
        if word.is_punct or not word.nbor(1).is_punct:
            continue
        start = word.i
        end = word.i + 1
        while end < len(doc) and doc[end].is_punct:
            end += 1
        span = doc[start:end]
        spans.append((span, word.tag_, word.lemma_, word.ent_type_))
    with doc.retokenize() as retokenizer:
        for span, tag, lemma, ent_type in spans:
            attrs = {"tag": tag, "lemma": lemma, "ent_type": ent_type}
            retokenizer.merge(span, attrs=attrs)
    return doc


@Language.component("lower_lemmas")
def lower_case_lemmas(doc) :
    for token in doc :
        token.lemma_ = token.lemma_.lower()
    return doc

_app_nlp = spacy.load("en_core_web_sm")
_app_nlp.add_pipe("merge_noun_chunks")
_app_nlp.add_pipe("merge_entities")
_app_nlp.add_pipe("merge_subtokens")
_app_nlp.add_pipe("lower_lemmas")

_no_en_nlp = spacy.load("en_core_web_sm")
_no_en_nlp.add_pipe("merge_noun_chunks")
_no_en_nlp.add_pipe("merge_subtokens")
_no_en_nlp.add_pipe("lower_lemmas")

_no_su_nlp = spacy.load("en_core_web_sm")
_no_su_nlp.add_pipe("merge_noun_chunks")
_no_su_nlp.add_pipe("merge_entities")
_no_su_nlp.add_pipe("lower_lemmas")

_no_nc_nlp = spacy.load("en_core_web_sm")
_no_nc_nlp.add_pipe("merge_entities")
_no_nc_nlp.add_pipe("merge_subtokens")
_no_nc_nlp.add_pipe("lower_lemmas")

_clean_nlp = spacy.load("en_core_web_sm")
_clean_nlp.remove_pipe('ner')
_clean_nlp.add_pipe("lower_lemmas")

nlps = {
    'all': _app_nlp,
    'no_en': _no_en_nlp,
    'no_su': _no_su_nlp,
    'no_nc': _no_nc_nlp,
    'clean': _clean_nlp,
    'custom': spacy.load("en_core_web_sm")
}
