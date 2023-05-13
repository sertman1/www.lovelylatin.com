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
    title_of_work_tokens: List[str]
    url: str

    def __repr__(self):
        return (f"doc_id: {self.doc_id}\n" +
            f"  terms: {self.terms}\n" +
            f"  author: {self.author}\n" +
            f"  title: {self.title_of_work}\n" +
            f"  url: {self.url}\n")

def compute_doc_freqs(docs: List[Document]):
    freq = Counter()
    for doc in docs:
        for word in doc.terms:
            freq[word] += 1
        for word in doc.title:
            freq[word] += 3 # assign a 3 to 1 weight for title terms
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

    return (dict(vec), doc.doc_id, doc.url)

def vectorize_doc(doc, doc_freqs, N):
    return compute_tfidf(doc, doc_freqs, N)

def main():
    return

if __name__ == '__main__':
    main()