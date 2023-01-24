from django.shortcuts import render
import requests, bs4, time, re, os, datetime, zipfile, html, shutil
from pathlib import Path
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from .web_scraper import *
# Create your views here.

def mainPage(request):
    return render(request, "index.html", {})



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

    #Need to catch https://forums.sufficientvelocity.com/threads/warhammer-fantasy-divided-loyalties-an-advisors-quest.44838/4/
 
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
    print(obj.webscrape(base_url))
    #Now, send FIle off to Client to download at leisure.
