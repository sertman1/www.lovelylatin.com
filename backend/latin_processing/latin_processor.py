# the script which the backend calls upon a user GET request
# it processes the user's query and returns pertinent data to stdout (print)
import sys
from nltk.tokenize import word_tokenize

## auxilary scripts to help runtime processing
from latin_crawler import crawl

### Weighting considerations:

# prepositional phrases as a singular unit
# query expansion through lemmas
# position of words relative to one another: same clause, sentence, paragraph, section, chapter, book...?
# clearly some sort of inverse term document frequency to water down overused terms
# n-gram model seems strong but dubious due to nonstandardized word ordering

stopwords = word_tokenize("ac adhic an at atque aut autem cum cur de deinde dum enim et etiam etsi ex haud hic hoc iam igitur interim ita itaque magis modo nam ne nec necque neque nisi non quae quam quare quia quicumque quidem quilibet quis quisnam quisquam quisque quisquis quo quoniam sed si nisi sic sive tam tamen tum ubi uel uero ut")

def remove_stopwords(tokens):
    pruned_sentence = list()
    for word in tokens:
        if word not in stopwords:
            pruned_sentence.append(word)

    return pruned_sentence

def process_extracted_texts(extracted_texts):
    for author in extracted_texts.keys():
        print(author)
    return  


###### GENERAL NOTES / CONSIDERATIONS FOR FUTURE IMPLEMENTATIONS
    # pre compute index of terms to documents (book, page level, section, etc.)
    # DRAW IT OUT FOR WRITE UP:
        # TERM INDEXES TO SECTION TO CHAPTER TO WORK TO AUHTOR

    # NB: can crawl common queries (vectors) while offline so answers are quickly found
    # NB: can include "terms to omit", "specify weights",

    # weighted query expansion
def process_query(query, authors_selected):
    report = ""

    # get appropriate text from library given authors selected 
    extracted_texts = crawl("https://www.thelatinlibrary.com", authors_selected)
    process_extracted_texts(extracted_texts)

    # process query
    tokens = remove_stopwords(word_tokenize(query))

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
    print(process_query(query, authors_selected)) # print to stdout so that javascript can interpret results

if __name__ == "__main__":
    main()