import itertools
from typing import NamedTuple, List, Dict
from collections import Counter, defaultdict

import numpy as np
from numpy.linalg import norm

class Document(NamedTuple):
    doc_id: int # NB data files index starting from 1
    terms: List[str]
    author: str
    title_of_work: str

    def __repr__(self):
        return (f"doc_id: {self.doc_id}\n" +
            f"  terms: {self.terms}\n" +
            f"  author: {self.author}\n" +
            f"  title: {self.title_of_work}" )

def compute_doc_freqs(docs: List[Document]):
    freq = Counter()
    for doc in docs:
        words = set()
        for sec in doc.sections():
            for word in sec:
                words.add(word)
        for word in words:
            freq[word] += 1
    return freq

def compute_tf(doc: Document):
    vec = defaultdict(float)

    for term in doc.terms:
        vec[term] += 1

    return dict(vec)

def compute_tfidf(doc, doc_freqs, N):
    freq = doc_freqs
    tf = compute_tf(doc)
    
    vec = defaultdict(float)

    # the calculation for IDF(t) was derived from Scikit-Learn which effectively handles edge cases
    for word in doc.terms:
        vec[word] += tf[word] * (np.log2((N + 1) / (freq[word] + 1)) + 1)

    return dict(vec)

def vectorize_doc(doc, doc_freqs, N):
    return compute_tfidf(doc, doc_freqs, N)

def main():
    return

if __name__ == '__main__':
    main()