from django.shortcuts import render
import requests, bs4, time, re, os, datetime, shutil
from pathlib import Path
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

# Create your views here.

def mainPage():
    return

def check_url(base_url):
    '''Checks if given URL is of right domain and if actual thread'''
    val = URLValidator()
    try:
        val(base_url)
    except ValidationError:
        print("Not valid Url")
        raise 

    can_continue = False
    accepted_urls = ['spacebattles.com/threads/','sufficientvelocity.com/threads/']
    for url in accepted_urls:
        if url in base_url:
            can_continue = True

    if not can_continue:
        print("Domain not accepted")
        raise

    if not re.match('.*\/$', base_url):
        base_url+= '/'

    if re.match('.*\/reader\/$', base_url):
        base_url.removesuffix('reader/')

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
        #Two strings that need to be appended to content.opf in order.
        self.manifest = '\n'
        #TODO, add introduction.ncx into spine.
        self.spine = '\n    <itemref idref="chapter_0"/>\n    <itemref idref="nav"/>'

    def webscrape(self, base_url, options=None):
        self.headers = {
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
        self.base_url = base_url

        response = requests.get(base_url, self.headers)
        response.encoding = 'utf-8'
        self.main_page_soup = bs4.BeautifulSoup(response.text, 'html.parser')
        self.zip_up()
        return

        time.sleep(0.1)

        self.start_boilerplate()
        
        self.scrape_catagory(self.base_url+'reader/')
        

        # scrape each catagory options says too.

        self.close_boilerplate()

        # Calculates how many pages need to be fetched.
        

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

        # finish boilerstuff

    def scrape_catagory(self, reader_url):
        '''Scrapes an entire thread for a given catagory'''
        print(f'{reader_url=}')
        response = requests.get(reader_url, self.headers)
        response.encoding = 'utf-8'
        soup = bs4.BeautifulSoup(response.text, 'html.parser')

        self.pack_articles(soup)

        pages_to_get = soup.find('ul', class_='pageNav-main')
        last_page = pages_to_get.find_all('li')[-1]
        last_page_number = int(last_page.find('a').text)

        return
        for i in range(2, last_page_number+1):
            response = requests.get(f'{base_url}page-{i}', headers)
            self.pack_articles(response)
            if i % 2 ==0:
                time.sleep(0.6)


    def pack_articles(self, soup):
        '''Takes a GET Request response, and converts the chapters inside that response into chapters of the files.'''
        page_message_chain = soup.find('div', class_='block--messages')
        articles = page_message_chain.find_all('article', class_='message--post')
        for i in range(len(articles)):
            # Step 3. Converting each post, articles[i], into an chapter file, format.
            #The chapters title, <span class='threadmarkLabel'> articles[i].find('span', class_='threadmarkLabel')
            ##The chapter text
            chapter_title = articles[i].find("span",class_="threadmarkLabel").get_text(strip=True)
            with open(f'ToZip/EPUB/Chapter-{self.chapter_num}.xhtml', 'w', encoding='utf8') as f:
                #TODO, write as proper html file
                f.write(f'<?xml version=\'1.0\' encoding=\'utf-8\'?>\n<!DOCTYPE html>\n<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" epub:prefix="z3998: http://www.daisy.org/z3998/2012/vocab/structure/#" lang="en" xml:lang="en">\n  <head>\n    <title>{chapter_title}</title>\n    <link href="style/main.css" rel="stylesheet" type="text/css"/>\n  </head>\n  <body>\n    <h2>{chapter_title}</h2>\n')
                #TODO, strip of attributes
                f.write(str(articles[i].find('div', class_='bbWrapper').get_text() ))
                f.write('\n  </body>\n</html>')
            

            #Update boilerplate
            # nav needs new li
            with open('ToZip/EPUB/nav.xhtml', 'a', encoding='utf8') as f:
                f.write(f'\n        <li>\n          <a href="Chapter-{self.chapter_num}.xhtml">{chapter_title}</a>\n        </li>')
            # toc needs new nav point
            with open('ToZip/EPUB/toc.ncx', 'a', encoding='utf8') as f:
                
                f.write(f'<navPoint id="Chapter-{self.chapter_num}" playOrder="{self.chapter_num + 1}">\n      <navLabel>\n        <text>Chapter {self.chapter_num}</text>\n      </navLabel>\n      <content src="Chapter-{self.chapter_num}.xhtml"/>\n    </navPoint>')
            self.manifest += f'    <item href="Chapter-{self.chapter_num}.xhtml" id="chapter_{self.chapter_num}" media-type="application/xhtml+xml"/>\n'
            self.spine += f'    <itemref idref="chapter_{self.chapter_num}"/>\n'
            self.chapter_num += 1
        
    def zip_up(self):
        #TODO
        '''Takes the entire thing, and converts to epub file'''
        thread_title = self.main_page_soup.find('h1', class_='p-title-value').get_text()
        archive_name = os.path.expanduser(os.path.join('~', f'{thread_title}'))
        shutil.make_archive(archive_name, 'zip', 'ToZip')
        return


    def start_boilerplate(self):
        '''Create content.opf, introduction.xhtml, nav and toc'''

        if (not os.path.exists('ToZip/')):
            os.makedirs('ToZip/')

        if (not os.path.exists('ToZip/EPUB/')):
            os.makedirs('ToZip/EPUB/')

        if (not os.path.exists('ToZip/EPUB/style')):
            os.makedirs('ToZip/EPUB/style')

        if (not os.path.exists('ToZip/META-INF')):
            os.makedirs('ToZip/META-INF')

        thread_title = self.main_page_soup.find('h1', class_='p-title-value')
        thread_description = self.main_page_soup.find('article', class_='threadmarkListingHeader-extraInfoChild')
        creator = self.main_page_soup.find('a', class_='username').get_text()
        datetime_now = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ%Z")
        #Given that there is no UUID, DOI or ISBN typically associated with the content scraped. A hash is instead generated for a identifier that will likely be unique.
        identifier = hash(thread_title.get_text()+creator+datetime_now)
        with open('ToZip/EPUB/introduction.xhtml', 'w', encoding='utf8') as f:
            f.write('<?xml version=\'1.0\' encoding="utf-8"?>\n<!DOCTYPE html>\n<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" epub:prefix="z3998: http://www.daisy.org/z3998/2012/vocab/structure/#" lang="en" xml:lang="en">')
            f.write(f'\n  <head>\n    <title>{ thread_title.get_text(strip=True) }</title>\n  </head>\n<body>')
            f.write(f"""
    <h1>{thread_title.get_text(strip=True)}</h1>
	<p><b>Written by: {creator}</b></p>
	<p>{thread_description.get_text(strip=True)}</p>
	<p>Status: {1}</p>
	<p>Published: {4}</p>
	
	<p>Updated: {datetime.datetime.now().strftime("%Y-%m-%d")}</p>
	
	<p>Words: {11779}</p>
	
	<p>Chapters: {5}</p>
	
	<p>Original source:
		<a rel="noopener noreferrer" href="{self.base_url}">{self.base_url}</a></p>
	
	<p>Exported by: <a href="{1}">XFReader</a></p>""")
            #TODO, Add in the nessecary information

        with open('ToZip/EPUB/content.opf', 'w', encoding='utf8') as f:
            f.write(f'<?xml version=\'1.0\' encoding=\'utf-8\'?>\n<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="id" version="3.0" prefix="rendition: http://www.idpf.org/vocab/rendition/#">')
            f.write(f'\n  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">\n    <meta property="dcterms:modified">{datetime_now}</meta>\n    <meta name="generator" content="Ebook-lib 0.17.1"/>')
            f.write(f'\n    <dc:identifier id="id">{identifier}</dc:identifier>\n    <dc:title>{thread_title.get_text(strip=True) }</dc:title>\n    <dc:language>en</dc:language>\n    <dc:creator id="creator">{creator}</dc:creator>\n    <dc:description>{thread_description.get_text(strip=True)}</dc:description>\n  </metadata>')
            f.write(f'\n  <manifest>\n    <item href="style/main.css" id="doc_style" media-type="text/css"/>\n    <item href="style/nav.css" id="style_nav" media-type="text/css"/>\n    <item href="introduction.xhtml" id="chapter_0" media-type="application/xhtml+xml"/>\n    <item href="nav.xhtml" id="nav" media-type="application/xhtml+xml" properties="nav"/>')

        with open('ToZip/EPUB/nav.xhtml', 'w', encoding='utf8') as f:
            f.write(f'<?xml version=\'1.0\' encoding=\'utf-8\'?>\n<!DOCTYPE html>\n<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en" xml:lang="en">\n  <head>\n    <title>{thread_title.get_text(strip=True) }</title>\n    <link href="style/main.css" rel="stylesheet" type="text/css"/>\n  </head>\n  <body>\n    <nav epub:type="toc" id="id" role="doc-toc">\n      <h2>{thread_title.get_text(strip=True) }</h2>')
            f.write(f'<li>\n          <a href="introduction.xhtml">Introduction</a>\n        </li>')

        with open('ToZip/EPUB/toc.ncx', 'w', encoding='utf8') as f:
            f.write(f'<?xml version=\'1.0\' encoding=\'utf-8\'?>\n<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">\n  <head>\n    <meta content="{identifier}" name="dtb:uid"/>\n    <meta content="0" name="dtb:depth"/>\n    <meta content="0" name="dtb:totalPageCount"/>\n    <meta content="0" name="dtb:maxPageNumber"/>\n  </head>\n  <docTitle>\n    <text>{thread_title.get_text(strip=True)}</text>\n  </docTitle>\n  <navMap>')
            f.write(f'    <navPoint id="intro" playOrder="1">\n     <navLabel>\n       <text>Introduction</text>\n     </navLabel>\n     <content src="introduction.xhtml"/>\n   </navPoint>')


        # The defaullt boilerplate, requires nothing from what is fetched.
        with open('ToZip/EPUB/style/main.css', 'w', encoding='utf8') as f:
            f.write('@namespace epub "http://www.idpf.org/2007/ops";\nbody {\n    font-family: Verdana, Helvetica, Arial, sans-serif;\n}\nh1 {\n    text-align: center;\n}\nh2 {\n    text-align: left;\n    font-weight: bold;\n}\nol {\n    list-style-type: none;\n    margin: 0;\n}\nol > li {\n    margin-top: 0.3em;\n}\nol > li > span {\n    font-weight: bold;\n}\nol > li > ol {\n    margin-left: 0.5em;\n}\n.spoiler {\n    padding-left: 0.4em;\n    border-left: 0.2em solid #c7ccd1;\n}\n')
        
        with open('ToZip/EPUB/style/nav.css', 'w', encoding='utf8') as f:
            f.write('BODY {color: white;}')        

        with open('ToZip/EPUB/nav.xhtml', 'w', encoding='utf8') as f:
            f.write(f'<?xml version=\'1.0\' encoding=\'utf-8\'?>\n<!DOCTYPE html>\n<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en" xml:lang="en">\n  <head>\n    <title>{thread_title.get_text(strip=True)}</title>\n    <link href="style/main.css" rel="stylesheet" type="text/css"/>\n  </head>\n  <body>\n    <nav epub:type="toc" id="id" role="doc-toc">\n      <h2>{thread_title.get_text(strip=True)}</h2>\n      <ol>')

        with open('ToZip/mimetype', 'w', encoding='utf8') as f:
            f.write('application/epub+zip')

        with open('ToZip/META-INF/container.xml', 'w', encoding='utf8') as f:
            f.write('<?xml version=\'1.0\' encoding=\'utf-8\'?>\n<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container" version="1.0">\n  <rootfiles>\n    <rootfile media-type="application/oebps-package+xml" full-path="EPUB/content.opf"/>\n  </rootfiles>\n</container>')


    def close_boilerplate(self):
        '''Appends to content.opf, introduction.xhtml, nav and toc the closing tags'''


        with open('ToZip/EPUB/introduction.xhtml', 'a', encoding='utf8') as f:
            f.write('\n  </body>\n</html>')

        with open('ToZip/EPUB/content.opf', 'a', encoding='utf8') as f:
            f.write(self.manifest)
            f.write('    <item href="toc.ncx" id="ncx" media-type="application/x-dtbncx+xml"/>\n  </manifest>\n  <spine toc="ncx">')
            f.write(self.spine)
            f.write('  </spine>\n</package>')   

        with open('ToZip/EPUB/nav.xhtml', 'a', encoding='utf8') as f:
            f.write('\n      </ol>\n    </nav>\n  </body>\n</html>')

        with open('ToZip/EPUB/toc.ncx', 'a', encoding='utf8') as f:
            f.write('\n  </navMap>\n</ncx>')