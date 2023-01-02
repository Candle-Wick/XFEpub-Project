from django.shortcuts import render
import requests, bs4, time, re
from pathlib import Path
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

# Create your views here.

def mainPage():
    return

def api_webscrape_call():

    

    #base_url = 'https://forums.sufficientvelocity.com/threads/warhammer-fantasy-divided-loyalties-an-advisors-quest.44838/reader/'
    #base_url = 'Fail'
    base_url = 'https://forums.sufficientvelocity.com/threads/warhammer-fantasy-divided-loyalties-an-advisors-quest.44838'

    val = URLValidator()
    try:
        val(base_url)
    except ValidationError:
        print("Not valid Url")
        return

    can_continue = False
    accepted_urls = ['spacebattles.com','sufficientvelocity.com']
    for url in accepted_urls:
        if url in base_url:
            can_continue = True

    if not can_continue:
        print("Domain not accepted")
        return

    if not re.match('.*\/$', base_url):
        base_url+= '/'

    if not re.match('.*\/reader\/$', base_url):
        base_url += 'reader/'

    print(base_url)
    obj = web_scraper()
    obj.start_boilerplate()
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
        
        response = requests.get(base_url, headers)
        self.start_boilerplate(response)
        self.pack_articles(response)
        soup = bs4.BeautifulSoup(response.content, 'html.parser')

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
            print(f"https://forums.sufficientvelocity.com/threads/warhammer-fantasy-divided-loyalties-an-advisors-quest.44838/reader/page-{i}")
            response = requests.get(f'{base_url}page-{i}', headers)
            self.pack_articles(response)
            if i % 2 ==0:
                time.sleep(0.6)

        # finish boilerstuff

    def pack_articles(self, response):
        '''Takes a GET Request response, and converts the chapters inside that response into chapters of the files.'''
        soup = bs4.BeautifulSoup(response.content, 'html.parser')
        page_message_chain = soup.find('div', class_='block--messages')
        articles = page_message_chain.find_all('article', class_='message--post')
        for i in range(len(articles)):
            # Step 3. Converting each post, articles[i], into an chapter file, format.
            #The chapters title, <span class='threadmarkLabel'> articles[i].find('span', class_='threadmarkLabel')
            ##The chapter text
            with open(f'ToZip/EPUB/Chapter-{self.chapter_num}.xhtml', 'w') as f:
                f.write(str(articles[i].find('div', class_='bbWrapper')))
            self.chapter_num += 1
            pass
    
    def zip_up(self):
        #TODO
        '''Takes the entire thing, and converts to epub file'''
        return


    def start_boilerplate(self, response):
        '''Create content.opf, introduction.xhtml, nav and toc'''
        soup = bs4.BeautifulSoup(response.content, 'html.parser')
        introduction_block = soup.find('div', class_='threadmarkListingHeader')

        with open('ToZip/EPUB/introduction.xhtml', 'w') as f:
            f.write('<?xml version=\'1.0\' encoding="utf-8"?>\n<!DOCTYPE html>\n<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" epub:prefix="z3998: http://www.daisy.org/z3998/2012/vocab/structure/#" lang="en" xml:lang="en">')
            f.write(f'<head>\n<title>{str( introduction_block.find("h1")) }</title>\n</head><body>')