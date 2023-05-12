# the script which the backend calls upon a user GET request
# it processes the user's query and returns pertinent data to stdout (print)
import sys
from nltk.tokenize import word_tokenize
from typing import NamedTuple, List
from collections import Counter

## auxilary scripts to help runtime processing
from latin_crawler import crawl
from vector_model import vectorize_doc, Document

def compute_doc_freqs(docs: List[Document]):
    freq = Counter()
    for doc in docs:
        words = set()
        for term in doc.terms:
            words.add(term)
        for word in words:
            freq[word] += 1
    return freq

stopwords = word_tokenize("ac adhic an at atque aut autem cum cur de deinde dum enim et etiam etsi ex haud hic hoc iam igitur interim ita itaque magis modo nam ne nec necque neque nisi non quae quam quare quia quicumque quidem quilibet quis quisnam quisquam quisque quisquis quo quoniam sed si nisi sic sive tam tamen tum ubi uel vel uero vero ut")

def remove_stopwords(tokens):
    pruned_sentence = list()
    for word in tokens:
        if word not in stopwords:
            pruned_sentence.append(word)

    return pruned_sentence

def process_extracted_docs(extracted_texts):
    docs = []

    i = 0 # documents to be indexed by i
    for author in extracted_texts.keys():
        for title_of_work in extracted_texts[author]:
            works_text = (extracted_texts[author])[title_of_work]
            works_text = remove_stopwords(word_tokenize(works_text))
            doc = Document(i, works_text, author, title_of_work)
            docs.append(doc)
    
    return docs, i + 1 # the latter tells us the value of N: number of documents (+1 for index offset of i = 0)

def process_query(query):
    tokens = remove_stopwords(word_tokenize(query))
    query_doc = Document(-1, tokens, "user", "query") # special field values -1, "user" and "query" distinguish the doc as the query
    return query_doc

def process(query, authors_selected):
    report = ""
    extracted_texts = crawl("https://www.thelatinlibrary.com", authors_selected)

    query_doc = process_query(query)
    text_docs, N = process_extracted_docs(extracted_texts)
    
    doc_freqs = compute_doc_freqs(text_docs)

    query_vec = vectorize_doc(query_doc, doc_freqs, N)
    doc_vecs = []
    for doc in text_docs:
        doc_vecs.append(vectorize_doc(doc, doc_freqs, N))

    return report

def main():
    # Handle arguments provided from javascript backend:
    query = (sys.argv[1]).strip()
    if sys.argv[2] == "undefined":
        # no authors selected by user --> backend must process them all
        authors_selected = ['Ammianus', 'Apuleius', 'Augustus', 'Aurelius Victor', 'Caesar', 'Cato', 'Catullus', 'Cicero', 'Claudian', 'Curtius Rufus', 'Ennius', 'Eutropius', 'Florus', 'Frontinus', 'Gellius', 'Historia Augusta', 'Horace', 'Justin', 'Juvenal', 'Livy', 'Lucan', 'Lucretius', 'Martial', 'Nepos', 'Ovid', 'Persius', 'Petronius', 'Phaedrus', 'Plautus', 'Pliny Maior', 'Pliny Minor', 'Propertius', 'Quintilian', 'Sallust', 'Seneca Maior', 'Seneca Minor', 'Silius Italicus', 'Statius', 'Suetonius', 'Sulpicia', 'Tacitus', 'Terence', 'Tibullus', 'Valerius Flaccus', 'Valerius Maximus', 'Varro', 'Velleius', 'Vergil', 'Vitruvius']
    else:
        authors_selected = (sys.argv[2]).strip().split(',')

    # calculate result for client
    print(process(query, authors_selected)) # print to stdout so that javascript can interpret results

if __name__ == "__main__":
    main()