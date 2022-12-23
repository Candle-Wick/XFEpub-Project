from django.shortcuts import render
import requests, bs4, validators
from pathlib import Path


# Create your views here.

def mainPage():
    return

def webScrape():
    '''
    So.
    to Read out post.
    Every post in html file needs to become chapter.
    Interested only in <Body>
    <div class='block-body'>
    <article class= 'message-body'> 
        <div class = bbWrapper> 

    
    '''
    if (not Path('res.txt').is_file()):
        headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
        }
        response = requests.get("https://forums.sufficientvelocity.com/threads/warhammer-fantasy-divided-loyalties-an-advisors-quest.44838/reader/", headers)
        with open('res.txt', "w") as f:
            f.write(response.text)
            pass
    else:
        with open('res.txt', 'r') as f:

            # Step 1, 
            #Take URL, check if valid
            #validators.url(url)
            #If url doesnt match regex .*\/reader\/$
            # Add reader/
            #If url not valid, break.

            #Else, get page Reader.
            soup = bs4.BeautifulSoup(f, 'html.parser')
            # soup = bs4.BeautifulSoup(response.content, 'html.parser')

            page_message_chain = soup.find('div', class_='block--messages') # Reference to the block of all posts on the page

            chapter_number = 1
            
            # 

            # Step 2, Caluclating the amount of pages needed to be fecthed, fetching, with delays. all pages up to it. 
            #Calculating how many pages this needs to fetch. With the first reader page alreadt fetched.
            pages_to_get = soup.find('ul', class_='pageNav-main')
            last_page = pages_to_get.find_all('li')[-1]
            last_page_number = int(last_page.find('a').text)

            for i in range(2, last_page_number+1):
                print(f"https://forums.sufficientvelocity.com/threads/warhammer-fantasy-divided-loyalties-an-advisors-quest.44838/reader/page-{i}")
                #Get page.
                #Delay, 1 second every 2 requests

                # Step 3. Converting each post, articles[i], into an chapter file, format.
                articles = page_message_chain.find_all('article', class_='message--post')
                for i in range(len(articles)):
                    #The chapters title, <span class='threadmarkLabel'>
                    ##The chapter text
                    #print(articles[i].find('div', class_='bbWrapper'))
                    #Save as f'chapter_{chapter_number}.xhtml'
                    chapter_number += 1
                    pass
                    
            pass
    return