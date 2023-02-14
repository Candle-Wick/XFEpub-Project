from django.shortcuts import render
import requests, bs4, time, re, os, datetime, zipfile, html, shutil
from pathlib import Path
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.core.files.base import ContentFile


from django.views.decorators.csrf import csrf_exempt

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

    #To keep this consistant.
    if not re.match('.*\/$', base_url):
        base_url+= '/'

    print(base_url)
    threads = base_url.find('threads/') + 8
    last_slash = base_url.find('/', threads)
    base_url = base_url[:last_slash]
 
    return base_url + '/'

@csrf_exempt
def api_webscrape_call(request):

    

    #base_url = 'https://forums.sufficientvelocity.com/threads/warhammer-fantasy-divided-loyalties-an-advisors-quest.44838/reader/'
    #base_url = 'Fail'
    base_url = 'https://forums.sufficientvelocity.com/threads/warhammer-fantasy-divided-loyalties-an-advisors-quest.44838'
    #base_url = 'https://forums.sufficientvelocity.com/threads/from-the-brink-blood-ravens-quest-warhammer-40k.23731/'
    #base_url = 'https://stackoverflow.com/questions/52157937/python-return-exception-from-function'

    #base_url= 'https://forums.spacebattles.com/threads/the-great-caretaker-of-gaia-overlord-si-player.1069790/page-2?post=90021566#post-90021566'
    #base_url= 'https://forums.sufficientvelocity.com/threads/reverse-engineering-is-not-that-easy-planetary-annihilation-multicross-si.108388/5/'
    #base_url = 'https://forums.sufficientvelocity.com/threads/warhammer-fantasy-divided-loyalties-an-advisors-quest.44838/4/reader/'
    
    try:
        base_url = check_url(base_url)
    except Exception as err:
        print(f'invalid! {base_url} {err}' )
        return # TODO Handle exception here

    obj = web_scraper()
    file_path = str(obj.webscrape(base_url))
    # FIXME: File given not valid epub file. The process of downloading it breaks it.
    #return
    #file = ContentFile(file_path)
    with open(file_path, 'rb') as f:
        file = f.read()
    response = HttpResponse(file, 'application/epub+zip')
    #response['Content-Length'] = file.size
    response['Content-Disposition'] = f'attachment; filename="{file_path[6:]}"'
    return response
    #Now, send FIle off to Client to download at leisure.
