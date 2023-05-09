import re
import logging
from queue import PriorityQueue
from urllib import request, parse
from bs4 import BeautifulSoup

html_naming_conventions = {
    'Augustus': 'aug',
    'Aurelius Victor': 'victor',
    'Caesar': 'caes',
    'Cicero': 'cic',
    'Curtius Rufus': 'curtius',
    'Ennius': 'enn',
    'Historia Augusta': 'sha',
    'Horace': 'hor',
    'Livy': 'liv',
    'Pliny Maior': 'pliny1',
    'Pliny Minor': 'pliny',
    'Propertius': 'prop',
    'Sallust': 'sall',
    'Seneca Maior': 'seneca',
    'Seneca Minor': 'sen',
    'Silius Italicus': 'silius',
    'Suetonius': 'suet',
    'Tacitus': 'tac',
    'Terence': 'ter',
    'Tibullus': 'tib',
    'Valerius Flaccus': 'valeriusflaccus',
    'Valerius Maximus': 'valmax',
    'Velleius': 'vell',
    'Vergil': 'verg',
    'Ius Romanum': 'ius',
    'Miscellany': 'misc',
    'Neo-Latin': 'neo'
}

logging.basicConfig(level=logging.DEBUG, filename='output.log', filemode='w')
visitlog = logging.getLogger('visited')

def rank_link(link):
    rank = 0 # the higher the rank, the greater the priority to crawl 

    url = link[0]

    return rank

def is_self_referencing(link): # self referencing links in library are denoted with '#' and always in the innermost directory
    i = len(link) - 1
    while link[i] != '/':
        if link[i] == '#':
            return True
        i -= 1

    return False

def parse_links_sorted(root, html):
    urls = []

    soup = BeautifulSoup(html, 'html.parser')

    for link in soup.find_all('a'):
        href = link.get('href')
        if href and (href == "cred.html" or href =="/index.html" or href == "/classics.html" or href =="index.html" or href == "classics.html"):
            break # short circuit to prevent crawler from reading credits, teaching materials etc. and also from going back into the library's home page
        if href:
            text = link.string
            if not text:
                text = ''
            text = re.sub('\s+', ' ', text).strip()
            urls.append((parse.urljoin(root, link.get('href')), text))
 
    urls.sort(reverse=True, key=rank_link)
    for url in urls:
        yield(url)

def is_http_request(url):
    if len(url) > 8 and url[4] == 's':
        if url[0:8] == "https://":
            return True
    elif len(url) > 7:
        if url[0:7] == "http://":
            return True

def strip_http_request(url):
    if is_http_request(url) and url[4] == 's': # an https request
        return url[8:len(url)]
    elif is_http_request:
        return url[7:len(url)]
    
    return url # already stripped

def strip_www(url):
    if len(url) > 4 and url[0] == "w" and url[1] == "w" and url[2] == "w" and url[3] == ".":
        url = url[4:len(url)]
    
    return url

def get_link_domain(url):
    domain = ""

    stripped_url = strip_www(strip_http_request(url))

    i = 0
    while i < len(stripped_url) and stripped_url[i] != '/':
        domain += stripped_url[i]
        i += 1

    return domain# extra forward slash as per the Library's convention, needed to check if link is in main domain

def crawl(root_domain, authors=[]):
    queue = PriorityQueue()

    if len(authors) != 0: # if the user specified an author, alter root domain to just traverse those authors's works
        for author in authors:
            link_to_traverse = ""

            if author in html_naming_conventions: # for authors with special naming conventions in library
                link_to_traverse += root_domain + "/" + html_naming_conventions[author]
            else:
                link_to_traverse += root_domain + "/" + author.lower() # standard naming convention (e.g., for people with short names)

            if author == "Catullus": # Catullus is only author with shtml formatting
                queue.put(link_to_traverse + ".shtml") 
            else:
                queue.put(link_to_traverse + ".html")
    else:
        queue.put(root_domain) # otherwise, just traverse the whole library

    visited = []

    while not queue.empty():  
        url = queue.get()

        try:
            req = request.urlopen(url)
            html = req.read()
            visited.append(url)
            visitlog.debug(url)
            
            links_added_to_queue = [] # prevents repeat links from being added 
            for link, title in parse_links_sorted(url, html):

              if link not in links_added_to_queue:
                if link not in visited:
                  
                  if not is_self_referencing(link):
                    if get_link_domain(link) == strip_www(strip_http_request(root_domain)): # only crawl TheLatinLibrary itself
                        
                        links_added_to_queue.append(link) 
                        queue.put(link)

        except Exception as e:
            print(e, url)

    return visited

def main():
    authors = ['Cicero']
    crawl("https://www.thelatinlibrary.com", authors) # to test crawler, otherwise, crawl imported by processor

    # NB, html, shtml, ...
    # NB, toLowercase()

if __name__ == '__main__':
    main()