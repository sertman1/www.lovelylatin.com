import re
import logging
from queue import PriorityQueue
from urllib import request, parse
from bs4 import BeautifulSoup
import csv

extracted_works = {} # maps authors to (work, title) pairs and to be returned to main processing script for vector modeling
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
# list of bad links on the library NOT TO TRAVERSE (english/teaching materials)
bad_links = ["ll1/", "ll2/", "caes/", "catullus/", "satire/", "sallust/", "livius/", 
             "cic/", "virgil/", "historians/", "imperialism/syllabus.html", "law/",
             "/index.html", "/classics.html", "index.html", "classics.html", "cred.html"]


logging.basicConfig(level=logging.DEBUG, filename='output.log', filemode='w')
visitlog = logging.getLogger('visited')

def rank_link(link):
    rank = 0 # the higher the rank, the greater the priority to crawl 

    return rank

def is_self_referencing(link): # self referencing links in library are denoted with '#' and always in the innermost directory
    i = len(link) - 1
    while link[i] != '/':
        if link[i] == '#':
            return True
        i -= 1

    return False

def parse_links_sorted(root, html, get_all_homelinks):
    urls = []

    soup = BeautifulSoup(html, 'html.parser')

    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href in bad_links:
            break # short circuit to prevent crawler from reading credits, teaching materials etc. and also from going back into the library's home page
        if href:
            text = link.string
            if not text:
                text = ''
            text = re.sub('\s+', ' ', text).strip()
            urls.append((parse.urljoin(root, link.get('href')), text))

    # TODO: Link rank (important for overall library traversal)
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

def count_number_directories(url):
    num_directories = 0
    for c in url:
        if c == "/":
            num_directories += 1

def get_author_name_from_workpage(url):
    url = strip_http_request(url)

    i = 0
    while url[i] != "/":
        i += 1
    i += 1
    name = ""
    while i < len(url) and url[i] != "/" :
        name += url[i]
        i += 1
    name.title()

    for key, value in html_naming_conventions.items():
        if value == "name":
            return key

    return name.title()

def crawl(root_domain, authors=[]):
    queue = PriorityQueue()

    get_all_home_links = False # to tell crawler that no author was specified and thus dealing with a homepage on first iteration of queue
    if len(authors) != 0: # if the user specified an author, alter root domain to just traverse those authors's works
        for author in authors:
            link_to_traverse = ""

            if author in html_naming_conventions: # for authors with special naming conventions in library
                link_to_traverse += root_domain + "/" + html_naming_conventions[author]
            else:
                link_to_traverse += root_domain + "/" + author.lower() # standard naming convention (e.g., for people with short names)

            if author == "Catullus" or author == "Gellius": # Catullus, Gellius are only author with shtml formatting
                queue.put(link_to_traverse + ".shtml") 
            else:
                queue.put(link_to_traverse + ".html")
    else:
        queue.put(root_domain) # otherwise, just traverse the whole library
        get_all_home_links = True
        
    visited = []
    
    while not queue.empty():  
        url = queue.get()
        if url == "https://www.thelatinlibrary.com/christian" or url == "https://www.thelatinlibrary.com/medieval" or url == "https://www.thelatinlibrary.com/ius":
            url += ".html" # fixing broken link on page

        try:
            req = request.urlopen(url)
            html = req.read()

            if not get_all_home_links: # i.e., if we are not on the homepage and thus on an author's profile
                # check for special url cases which open two a "2nd homepage"
                if url != "https://www.thelatinlibrary.com/christian.html" or url != "https://www.thelatinlibrary.com/medieval.html" or url != "https://www.thelatinlibrary.com/neo.html":
                    author = get_author_name_from_workpage(url)

            visited.append(url)
            visitlog.debug(url)
            
            links_on_page = parse_links_sorted(url, html, get_all_home_links)
            links_added_to_queue = [] # prevents repeat links from being added 

            for link, title in links_on_page:
              if link not in links_added_to_queue:
                if link not in visited:
                  
                  if not is_self_referencing(link):
                    if get_link_domain(link) == strip_www(strip_http_request(root_domain)): # only crawl TheLatinLibrary itself
                        
                        links_added_to_queue.append(link) 
                        queue.put(link)

            if len(links_added_to_queue) == 0 and not get_all_home_links:
                extract_information(url, html, author)

            get_all_home_links = False

        except Exception as e:
            print(e, url)

    return extracted_works

def extract_information(address, html, author):
    soup = BeautifulSoup(html, 'html.parser')
   
    title = ""  # title of work and corresponding text to be returned
    text = "" 

    for header in soup.find_all('h1'):
        title = header.getText()

    for paragraph in soup.find_all('p'):
        if paragraph.get('class') == None: # check that it is not internal navigation
            add_section = True
            for section in paragraph.find_all('a'): # check for footer
                if section.getText() == "The Latin Library" or section.getText() == "The Classics Page" or section.getText() == author:
                    add_section = False
            if add_section:
                text += paragraph.getText()

    if author not in extracted_works:
        extracted_works[author] = dict()

    (extracted_works[author])[title] = text

def write_to_csv(dict):
    with open('extracted_texts.csv', 'w') as f:
        for key in dict.keys():
            f.write("%s,%s,\n"%(key, dict[key]))

def main():
    authors = [] # to test crawler, otherwise, crawl imported and handled by processor
    crawl("https://www.thelatinlibrary.com", authors) # populates extracted_works
    # TODO: rank_link?
    write_to_csv(extracted_works)

if __name__ == '__main__':
    main()