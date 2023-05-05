# the script which the backend calls upon a user GET request
# it processes the user's query and returns pertinent data to stdout (print)
import sys

def process_text(query):
    report = query + " :\n"

    return report

def main():
    query = sys.argv[1]
    print(process_text(query)) # print to stdout so that javascript can interpret results

if __name__ == "__main__":
    main()