import requests, bs4, time, os, datetime, zipfile, shutil, re
from pathlib import Path
class web_scraper:

    #TODO Rethink entire file storage idea.

    chapter_num = 1

    def __init__(self) -> None:
        self.chapter_num = 1
        #Two strings that need to be appended to content.opf in order.
        self.manifest = '\n'
        self.spine = '\n    <itemref idref="chapter_0"/>\n    <itemref idref="nav"/>\n'
        self.toc_list = ''
        self.nav_list = ''
        self.word_count = 0
        self.clear_ToZip()

    def webscrape(self, base_url, options=[]):
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
        if response.status_code != 200:
            raise Exception
        self.main_page_soup = bs4.BeautifulSoup(response.text, 'html.parser')


        time.sleep(0.1)


        
        self.scrape_catagory(self.base_url+'reader/')

        if (options):
            for i in range(0,len(options)):
                # Options contains an array of numbers that represent each threadmark catagory. 
                self.scrape_catagory(self.base_url+f'{options[i]}/reader/', options[i])
                self.sleep(0.2)
        

        # scrape each catagory options says too.


        self.start_boilerplate()
        self.close_boilerplate()

        return self.zip_up()

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

    def scrape_catagory(self, reader_url, catagory=0):
        '''Scrapes an entire thread for a given catagory'''
        response = requests.get(reader_url, self.headers)
        response.encoding = 'utf-8'
        soup = bs4.BeautifulSoup(response.text, 'html.parser')

        subheadings = {0:'Threadmarks', 4:'Apocrypha', 3:'Media', 10:'Media', 6:'Informational', 16:'Sidestory', 13:'Apocrypha', 19:'Informational'}
        self.nav_list += f'\n        <li>\n          <h3>{subheadings[catagory]}</h3>\n        </li>'


        self.pack_articles(soup)

        pages_to_get = soup.find('ul', class_='pageNav-main')
        last_page = pages_to_get.find_all('li')[-1]
        last_page_number = int(last_page.find('a').text)

        for i in range(2, last_page_number+1):
            response = requests.get(f'{reader_url}page-{i}', self.headers)
            self.pack_articles(bs4.BeautifulSoup(response.text, 'html.parser'))
            time.sleep(0.3)


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
                f.write(f'<?xml version=\'1.0\' encoding=\'utf-8\'?>\n<!DOCTYPE html>\n<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" epub:prefix="z3998: http://www.daisy.org/z3998/2012/vocab/structure/#" lang="en" xml:lang="en">\n  <head>\n    <title>{chapter_title}</title>\n    <link href="style/main.css" rel="stylesheet" type="text/css"/>\n  </head>\n  <body>\n    <h2>{chapter_title}</h2>\n')
                text_body = articles[i].find('div', class_='bbWrapper')
                f.write(str(text_body) )
                f.write('\n  </body>\n</html>')

                self.word_count +=  len(str(text_body).split(' '))

            self.nav_list += f'\n        <li>\n          <a href="Chapter-{self.chapter_num}.xhtml">  {chapter_title}</a>\n        </li>'
            self.toc_list += f'<navPoint id="Chapter-{self.chapter_num}" playOrder="{self.chapter_num + 1}">\n      <navLabel>\n        <text>Chapter {self.chapter_num}</text>\n      </navLabel>\n      <content src="Chapter-{self.chapter_num}.xhtml"/>\n    </navPoint>'    
            self.manifest += f'    <item href="Chapter-{self.chapter_num}.xhtml" id="chapter_{self.chapter_num}" media-type="application/xhtml+xml"/>\n'
            self.spine += f'    <itemref idref="chapter_{self.chapter_num}"/>\n'
            self.chapter_num += 1
        
    def zip_up(self):
        '''Takes the entire thing, and converts to epub file, returns path to file.'''
        thread_title = self.main_page_soup.find('h1', class_='p-title-value').get_text()
        thread_title = " ".join(thread_title.split()).replace(" ", "_")
        thread_title = "".join([c for c in thread_title if re.match(r'\w', c)])

        ToZip_EPUB = Path('ToZip/EPUB')
        ToZip_META = Path('ToZip/META-INF')
        ToZip_Style = Path('ToZip/EPUB/style')

        with zipfile.ZipFile(f'Epubs/{thread_title}.zip', 'w') as zip:
            zip.write('ToZip/mimetype', 'mimetype')
        with zipfile.ZipFile(f'Epubs/{thread_title}.zip', 'a', compression=zipfile.ZIP_DEFLATED) as zip:

            for file_path in ToZip_EPUB.iterdir():
                zip.write(file_path, 'EPUB/'+file_path.name.removesuffix('ToZip/'))
            for file_path in ToZip_Style.iterdir():
                zip.write(file_path, 'EPUB/style/'+file_path.name.removesuffix('ToZip/'))
            for file_path in ToZip_META.iterdir():
                zip.write(file_path, 'META-INF/'+file_path.name.removesuffix('ToZip/'))

        

        epub_path = Path(f'Epubs/{thread_title}.zip')

        if (os.path.exists(epub_path.with_suffix('.epub'))):
            os.remove(epub_path.with_suffix('.epub'))

        epub_path.rename(epub_path.with_suffix('.epub'))


        return epub_path.with_suffix('.epub')


    def start_boilerplate(self):
        '''Gives each file the beginning parts, standard for a epub file.'''

        thread_title = self.main_page_soup.find('h1', class_='p-title-value')
        thread_description = self.main_page_soup.find('article', class_='threadmarkListingHeader-extraInfoChild')
        creator = self.main_page_soup.find('a', class_='username').get_text()
        datetime_now = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ%Z")
        pair_rows = self.main_page_soup.find_all('dl', class_='pairs--rows')
        creation_date = pair_rows[0].find('dd').get_text()
        index_progress = pair_rows[1].find('dd').get_text()
        #Given that there is no UUID, DOI or ISBN typically associated with the content scraped. A hash is instead generated for a identifier that will likely be unique.
        identifier = hash(thread_title.get_text()+creator+datetime_now)

        with open('ToZip/EPUB/introduction.xhtml', 'w', encoding='utf8') as f:
            f.write('<?xml version=\'1.0\' encoding="utf-8"?>\n<!DOCTYPE html>\n<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" epub:prefix="z3998: http://www.daisy.org/z3998/2012/vocab/structure/#" lang="en" xml:lang="en">')
            f.write(f'\n  <head>\n    <title>{ thread_title.get_text(strip=True) }</title>\n  </head>\n<body>')
            f.write(f"""
    <h1>{thread_title.get_text(strip=True)}</h1>
	<p><b>Written by: {creator}</b></p>
	<p>{thread_description.get_text(strip=True)}</p>
	<p>Status: {index_progress}</p>
	<p>Published: {creation_date}</p>
	
	<p>Updated: {datetime.datetime.now().strftime("%Y-%m-%d")}</p>
	
	<p>Words: {self.word_count}</p>
	
	<p>Chapters: {self.chapter_num-1}</p>
	
	<p>Original source:
		<a rel="noopener noreferrer" href="{self.base_url}">{self.base_url}</a></p>
	
	<p>Exported by: <a href="{1}">XFReader</a></p>""")
            #TODO, Add in the url to the site here.

        with open('ToZip/EPUB/content.opf', 'w', encoding='utf8') as f:
            f.write(f'<?xml version=\'1.0\' encoding=\'utf-8\'?>\n<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="id" version="3.0" prefix="rendition: http://www.idpf.org/vocab/rendition/#">')
            f.write(f'\n  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">\n    <meta property="dcterms:modified">{datetime_now}</meta>\n    <meta name="generator" content="Ebook-lib 0.17.1"/>')
            f.write(f'\n    <dc:identifier id="id">{identifier}</dc:identifier>\n    <dc:title>{thread_title.get_text(strip=True) }</dc:title>\n    <dc:language>en</dc:language>\n    <dc:creator id="creator">{creator}</dc:creator>\n    <dc:description>{thread_description.get_text(strip=True)}</dc:description>\n  </metadata>')
            f.write(f'\n  <manifest>\n    <item href="style/main.css" id="doc_style" media-type="text/css"/>\n    <item href="style/nav.css" id="style_nav" media-type="text/css"/>\n    <item href="introduction.xhtml" id="chapter_0" media-type="application/xhtml+xml"/>\n    <item href="nav.xhtml" id="nav" media-type="application/xhtml+xml" properties="nav"/>')

        with open('ToZip/EPUB/nav.xhtml', 'w', encoding='utf8') as f:
            f.write(f'<?xml version=\'1.0\' encoding=\'utf-8\'?>\n<!DOCTYPE html>\n<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en" xml:lang="en">\n  <head>\n    <title>{thread_title.get_text(strip=True) }</title>\n    <link href="style/main.css" rel="stylesheet" type="text/css"/>\n  </head>\n  <body>\n    <nav epub:type="toc" id="id" role="doc-toc">\n      <h2>{thread_title.get_text(strip=True) }</h2>\n')
            f.write(f'      <ol>\n        <li>\n          <a href="introduction.xhtml">Introduction</a>\n        </li>')
            f.write(self.nav_list)

            

        with open('ToZip/EPUB/toc.ncx', 'w', encoding='utf8') as f:
            f.write(f'<?xml version=\'1.0\' encoding=\'utf-8\'?>\n<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">\n  <head>\n    <meta content="{identifier}" name="dtb:uid"/>\n    <meta content="0" name="dtb:depth"/>\n    <meta content="0" name="dtb:totalPageCount"/>\n    <meta content="0" name="dtb:maxPageNumber"/>\n  </head>\n  <docTitle>\n    <text>{thread_title.get_text(strip=True)}</text>\n  </docTitle>\n  <navMap>')
            f.write(f'    <navPoint id="intro" playOrder="1">\n     <navLabel>\n       <text>Introduction</text>\n     </navLabel>\n     <content src="introduction.xhtml"/>\n   </navPoint>')
            f.write(self.toc_list)

        # The defaullt boilerplate, requires nothing from what is fetched.
        with open('ToZip/EPUB/style/main.css', 'w', encoding='utf8') as f:
            f.write('@namespace epub "http://www.idpf.org/2007/ops";\nbody {\n    font-family: Verdana, Helvetica, Arial, sans-serif;\n}\nh1 {\n    text-align: center;\n}\nh2 {\n    text-align: left;\n    font-weight: bold;\n}\nol {\n    list-style-type: none;\n    margin: 0;\n}\nol > li {\n    margin-top: 0.3em;\n}\nol > li > span {\n    font-weight: bold;\n}\nol > li > ol {\n    margin-left: 0.5em;\n}\n.spoiler {\n    padding-left: 0.4em;\n    border-left: 0.2em solid #c7ccd1;\n}\n')
        
        with open('ToZip/EPUB/style/nav.css', 'w', encoding='utf8') as f:
            f.write('BODY {color: white;}')        


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

    def clear_ToZip(self):
        '''Empties ToZip of the last EPUB checked.'''
        dir = 'ToZip/EPUB'
        if (os.path.exists('ToZip/EPUB/')):
            shutil.rmtree(dir)
        
        if (not os.path.exists('ToZip/')):
            os.makedirs('ToZip/')

        if (not os.path.exists('ToZip/EPUB/')):
            os.makedirs('ToZip/EPUB/')

        if (not os.path.exists('ToZip/EPUB/style')):
            os.makedirs('ToZip/EPUB/style')

        if (not os.path.exists('ToZip/META-INF')):
            os.makedirs('ToZip/META-INF')