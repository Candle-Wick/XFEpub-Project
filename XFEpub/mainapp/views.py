from django.shortcuts import render
import requests, bs4, time, re, os
from pathlib import Path
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

# Create your views here.

def mainPage():
    return

def check_url(base_url):
    val = URLValidator()
    try:
        val(base_url)
    except ValidationError:
        print("Not valid Url")
        raise 

    can_continue = False
    accepted_urls = ['spacebattles.com','sufficientvelocity.com']
    for url in accepted_urls:
        if url in base_url:
            can_continue = True

    if not can_continue:
        print("Domain not accepted")
        raise

    if not re.match('.*\/$', base_url):
        base_url+= '/'

    if not re.match('.*\/reader\/$', base_url):
        base_url += 'reader/'

    return base_url

def api_webscrape_call():

    

    #base_url = 'https://forums.sufficientvelocity.com/threads/warhammer-fantasy-divided-loyalties-an-advisors-quest.44838/reader/'
    #base_url = 'Fail'
    base_url = 'https://forums.sufficientvelocity.com/threads/warhammer-fantasy-divided-loyalties-an-advisors-quest.44838'
    #base_url = 'https://stackoverflow.com/questions/52157937/python-return-exception-from-function'
    
    try:
        base_url = check_url(base_url)
    except Exception as err:
        
        return # TODO Handle exception here

    

    obj = web_scraper()
    obj.webscrape(base_url)

class web_scraper:

    chapter_num = 1

    def __init__(self) -> None:
        self.chapter_num = 1

    def webscrape(self, base_url):
        headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
        }
        # Fetch from user

        #Test without scraping
        # soup = None
        # with open('res.txt', 'r') as f:
        #     soup = bs4.BeautifulSoup(f, 'html.parser')
        
        response = requests.get(base_url, headers)
        soup = bs4.BeautifulSoup(response.content, 'html.parser')

        self.start_boilerplate(soup)
        self.pack_articles(soup)
        
        # Calculates how many pages need to be fetched.
        pages_to_get = soup.find('ul', class_='pageNav-main')
        last_page = pages_to_get.find_all('li')[-1]
        last_page_number = int(last_page.find('a').text)

        #Step 2.1, update package document, manifest, spine
        # Adding all tge files and folder boilerstuff
        '''
            mimetype
            META-INT
            > container.xml
            EPUB
            > content.opf
            > introduction.xhtml
            > nav.xhtml
            > toc.ncx
            style
                > main.css
                > nav.css
        
        '''


        return # TODO, Remove this
        
        for i in range(2, last_page_number+1):
            print(f"base_url{i}")
            response = requests.get(f'{base_url}page-{i}', headers)
            self.pack_articles(response)
            if i % 2 ==0:
                time.sleep(0.6)

        # finish boilerstuff

    def pack_articles(self, soup):
        '''Takes a GET Request response, and converts the chapters inside that response into chapters of the files.'''
        page_message_chain = soup.find('div', class_='block--messages')
        articles = page_message_chain.find_all('article', class_='message--post')
        for i in range(len(articles)):
            # Step 3. Converting each post, articles[i], into an chapter file, format.
            #The chapters title, <span class='threadmarkLabel'> articles[i].find('span', class_='threadmarkLabel')
            ##The chapter text
            with open(f'ToZip/EPUB/Chapter-{self.chapter_num}.xhtml', 'w') as f:
                f.write(" ".join(str(articles[i].find('div', class_='bbWrapper') ).split()))
            self.chapter_num += 1
            pass

        #Update boilerplate
        # nav needs new li
        # toc needs new nav point
        #Content needs both manifest and spine.
    
    def zip_up(self):
        #TODO
        '''Takes the entire thing, and converts to epub file'''
        return


    def start_boilerplate(self, soup):
        '''Create content.opf, introduction.xhtml, nav and toc'''

        if (not os.path.exists('ToZip/')):
            os.makedirs('ToZip/')

        if (not os.path.exists('ToZip/EPUB/')):
            os.makedirs('ToZip/EPUB/')

        if (not os.path.exists('ToZip/EPUB/style')):
            os.makedirs('ToZip/EPUB/style')

        if (not os.path.exists('ToZip/META-INF')):
            os.makedirs('ToZip/META-INF')

        thread_title = soup.find('h1', class_='p-title-value')
        with open('ToZip/EPUB/introduction.xhtml', 'w') as f:
            f.write('<?xml version=\'1.0\' encoding="utf-8"?>\n<!DOCTYPE html>\n<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" epub:prefix="z3998: http://www.daisy.org/z3998/2012/vocab/structure/#" lang="en" xml:lang="en">')
            f.write(f'<head>\n<title>{thread_title.get_text(strip=True) }</title>\n</head><body>')

        with open('ToZip/EPUB/content.opf', 'w') as f:
            pass
    
        with open('ToZip/EPUB/nav.xhtml', 'w') as f:
            pass

        with open('ToZip/EPUB/toc', 'w') as f:
            pass

        # The defaullt boilerplate, requieres nothing from what is fetched.
        with open('ToZip/EPUB/style/main.css', 'w') as f:
            f.write('@namespace epub "http://www.idpf.org/2007/ops";\nbody {\n    font-family: Verdana, Helvetica, Arial, sans-serif;\n}\nh1 {\n    text-align: center;\n}\nh2 {\n    text-align: left;\n    font-weight: bold;\n}\nol {\n    list-style-type: none;\n    margin: 0;\n}\nol > li {\n    margin-top: 0.3em;\n}\nol > li > span {\n    font-weight: bold;\n}\nol > li > ol {\n    margin-left: 0.5em;\n}\n.spoiler {\n    padding-left: 0.4em;\n    border-left: 0.2em solid #c7ccd1;\n}\n')
        
        with open('ToZip/EPUB/style/nav.css', 'w') as f:
            f.write('BODY {color: white;}')        

        with open('ToZip/EPUB/nav', 'w') as f:
            f.write(f'<?xml version="1.0" encoding="utf-8"?><!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en" xml:lang="en"><head><title>{thread_title.get_text(strip=True)}</title><link href="style/main.css" rel="stylesheet" type="text/css"/></head><body>')

        with open('ToZip/mimetype', 'w') as f:
            f.write('application/epub+zip')

        with open('ToZip/META-INF', 'w') as f:
            f.write('<?xml version="\'"1.0\' encoding=\'utf-8\'?>\n<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container" version="1.0">\n  <rootfiles>\n    <rootfile media-type="application/oebps-package+xml" full-path="EPUB/content.opf"/>\n  </rootfiles>\n</container>')


    def close_boilerplate():
        '''Appends to content.opf, introduction.xhtml, nav and toc the closing tags'''


        with open('ToZip/EPUB/introduction.xhtml', 'w') as f:
            f.write('</body>\n</html>')

        with open('ToZip/EPUB/content.opf', 'w') as f:
            pass
    
        with open('ToZip/EPUB/nav.xhtml', 'w') as f:
            pass

        with open('ToZip/EPUB/toc', 'w') as f:
            pass