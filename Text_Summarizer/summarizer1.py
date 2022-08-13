from sklearn.feature_extraction.text import TfidfVectorizer
from spacy.lang.en import English
import numpy as np

nlp = English()
nlp.add_pipe('sentencizer')



def summarizer(text, tokenizer=nlp, max_sent_in_summary=3):
    
    doc = nlp(text.replace("\n", ""))
    sentences = [sent.text.strip() for sent in doc.sents]
    
    sentence_organizer = {k:v for v,k in enumerate(sentences)}
    
    vectorizer = TfidfVectorizer(min_df=2,  max_features=None, 
                                        strip_accents='unicode', 
                                        analyzer='word',
                                        token_pattern=r'\w{1,}',
                                        ngram_range=(1, 3), 
                                        use_idf=1,smooth_idf=1,
                                        sublinear_tf=1,
                                        stop_words = 'english')
    
    vectorizer.fit(sentences)
    vectors = vectorizer.transform(sentences)
    scores = np.array(vectors.sum(axis=1)).ravel()
    N = max_sent_in_summary
    top_n_sentences = [sentences[ind] for ind in np.argsort(scores, axis=0)[::-1][:N]]
    
    top_n = [(sentence,sentence_organizer[sentence]) for sentence in top_n_sentences]
   
    top_n = sorted(top_n, key = lambda x: x[1])
    ordered_scored_sentences = [element[0] for element in top_n]
   
    summary = " ".join(ordered_scored_sentences)
    return summary

