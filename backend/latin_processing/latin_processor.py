# the script which the backend calls upon a user GET request
# it processes the user's query and returns pertinent data to stdout (print)
import sys
from nltk.tokenize import word_tokenize

### Weighting considerations:

# prepositional phrases as a singular unit

stopwords = word_tokenize("ac adhic an at atque aut autem cur de deinde dum enim et etiam etsi ex haud hic iam igitur interim ita magis modo nam ne nec necque neque nisi non quae quam quare quia quicumque quidem quilibet quis quisnam quisquam quisque quisquis quo quoniam sed si nisi sic sive tam tamen tum ubi uel uero ut")

def remove_stopwords(tokens):
    pruned_sentence = list()
    for word in tokens:
        if word not in stopwords:
            pruned_sentence.append(word)

    return pruned_sentence

def process_query(query):
    report = "Your entry: " + query + "\n"

    # retrieve tokens from query
    tokens = remove_stopwords(word_tokenize(query))

    # ! consider n-gram p

    return report

def main():
    query = sys.argv[1]
    print(process_query(query)) # print to stdout so that javascript can interpret results

if __name__ == "__main__":
    main()