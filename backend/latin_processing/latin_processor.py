# the script which the backend calls upon a user GET request
# it processes the user's query and returns pertinent data to stdout (print)
import sys
from nltk.tokenize import word_tokenize

### Weighting considerations:

# prepositional phrases as a singular unit
# query expansion through lemmas
# position of words relative to one another: same clause, sentence, paragraph, section, chapter, book...?
# clearly some sort of inverse term document frequency to water down overused terms
# n-gram model seems strong but dubious due to nonstandardized word ordering

stopwords = word_tokenize("ac adhic an at atque aut autem cur de deinde dum enim et etiam etsi ex haud hic iam igitur interim ita magis modo nam ne nec necque neque nisi non quae quam quare quia quicumque quidem quilibet quis quisnam quisquam quisque quisquis quo quoniam sed si nisi sic sive tam tamen tum ubi uel uero ut")

def remove_stopwords(tokens):
    pruned_sentence = list()
    for word in tokens:
        if word not in stopwords:
            pruned_sentence.append(word)

    return pruned_sentence

def process_global_query(query):
    report = "I. Your text: " + query + "\n"

    # retrieve tokens from query
    tokens = remove_stopwords(word_tokenize(query))

    # pre compute index of terms to documents (book, page level, section, etc.)
    # DRAW IT OUT FOR WRITE UP:
        # TERM INDEXES TO SECTION TO CHAPTER TO WORK TO AUHTOR

    # NB: can crawl common queries (vectors) while offline so answers are quickly found
    # NB: can include "terms to omit", "specify weights",

            # weighted query expansion

    return report

def process_author_query(query, authors_selected):
    report = "I. Selected Authors: " + str(authors_selected) + '\n'
    report += "II. Your text: " + query + '\n'

    # retrieve tokens from query
    tokens = remove_stopwords(word_tokenize(query))

    return report

def main():
    query = (sys.argv[1]).strip()
    authors_selected = (sys.argv[2]).strip()

    ## did user specify specific authors to search?
    if authors_selected != "undefined":
        authors_selected = authors_selected.split(',')
        print(process_author_query(query, authors_selected))
    else:
        print(process_global_query(query)) # print to stdout so that javascript can interpret results

if __name__ == "__main__":
    main()