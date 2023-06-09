# the script which the backend calls upon a user GET request
# it processes the user's query and returns pertinent data to stdout (print)

import sys
from nltk.tokenize import word_tokenize
from typing import Dict, List
from collections import Counter
from numpy.linalg import norm

## auxilary scripts to help runtime processing
from latin_crawler import crawl
from vector_model import vectorize_doc, Document
from process_unimorph import process_unimorph_file

inflected_form_to_base_form = process_unimorph_file()

def compute_doc_freqs(docs: List[Document]):
    freq = Counter()
    for doc in docs:
        for word in doc.terms:
            freq[word] += 1
        for word in doc.title_of_work_tokens:
            freq[word] += 3 # assign a 3 to 1 weight for title terms
    return freq

def dictdot(x: Dict[str, float], y: Dict[str, float]):
    '''
    Computes the dot product of vectors x and y, represented as sparse dictionaries.
    '''
    keys = list(x.keys()) if len(x) < len(y) else list(y.keys())
    return sum(x.get(key, 0) * y.get(key, 0) for key in keys)

def cosine_sim(x, y):
    '''
    Computes the cosine similarity between two sparse term vectors represented as dictionaries.
    '''
    num = dictdot(x, y)
    if num == 0:
        return 0
    return num / (norm(list(x.values())) * norm(list(y.values())))

def compute_similarities(query_vec, doc_vecs):
    similarities = []

    for doc in doc_vecs:
        sim = cosine_sim(query_vec[0], doc[0])
        if sim != 0:
            similarities.append((sim, doc[1]))

    similarities = sorted(similarities, reverse=True)

    #i = 0
    #while i < len(similarities):
        #if i != 0:
            #inverted_file[((similarities[i])[1])].score = "(" + str( (similarities[i][0]) / similarities[0][0] ) + ") "

    return similarities

stopwords = word_tokenize("ac adhic an at atque aut autem cum cur de deinde dum enim et etiam etsi ex haud hic hoc iam igitur interim ita itaque magis modo nam ne nec necque neque nisi non quae quam quare quia quicumque quidem quilibet quis quisnam quisquam quisque quisquis quo quoniam sed si nisi sic sive tam tamen tum ubi uel vel uero vero ut . , ; : [ ] < > ?")

def remove_stopwords(tokens):
    pruned_sentence = list()
    for word in tokens:
        if word not in stopwords and not word.isnumeric():
            pruned_sentence.append(word)

    return pruned_sentence

def add_base_form_to_tokens(tokens):
    expanded_tokens = []
    for token in tokens:
        expanded_tokens.append(token)
        if token in inflected_form_to_base_form:
            expanded_tokens.append(inflected_form_to_base_form[token])

    return expanded_tokens
    

inverted_file = {}
def process_extracted_docs(extracted_texts):
    docs = []

    i = 0 # documents to be indexed by i
    for author in extracted_texts.keys():
        for title_of_work in extracted_texts[author]:
            works_text = ((extracted_texts[author])[title_of_work])[0]
            works_text = remove_stopwords(word_tokenize(works_text.lower()))
            works_text = add_base_form_to_tokens(works_text)
            works_url = ((extracted_texts[author])[title_of_work])[1]
            title_of_work_tokens = word_tokenize(title_of_work.lower())
            doc = Document(i, works_text, author, title_of_work, title_of_work_tokens, works_url, "")
            docs.append(doc)
            inverted_file[i] = doc
            i += 1
    
    return docs, i + 1 # the latter tells us the value of N: number of documents (+1 for index offset of i = 0)

def process_query(query):
    tokens = remove_stopwords(word_tokenize(query))
    query_doc = Document(-1, tokens, "user", "query", [], "/", "") # special field values -1, "user" "query" "/" distinguish the doc as the query
    return query_doc

def process(query, authors_selected):
    report = ""
    extracted_texts = crawl("https://www.thelatinlibrary.com", authors_selected)

    query_doc = process_query(query.lower())
    text_docs, N = process_extracted_docs(extracted_texts)
    
    doc_freqs = compute_doc_freqs(text_docs)

    # vectors are dictionary (term matrix) to doc_id pairs
    query_vec = vectorize_doc(query_doc, doc_freqs, N)
    doc_vecs = []
    for doc in text_docs:
        doc_vecs.append(vectorize_doc(doc, doc_freqs, N))

    ranked_results = compute_similarities(query_vec, doc_vecs)

    i = 1
    for result in ranked_results:
        report += (inverted_file[result[1]]).score + (inverted_file[result[1]]).title_of_work +  (inverted_file[result[1]]).url + "\n"
        i += 1

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