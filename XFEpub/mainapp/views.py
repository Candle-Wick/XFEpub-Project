from django.shortcuts import render
import requests, bs4, time, re, os, datetime, zipfile, html, shutil
from pathlib import Path
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.core.files.base import ContentFile
from json import loads

from django.views.decorators.csrf import csrf_exempt

from django.conf import settings
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

    request_body = loads(request.body.decode("utf-8"))
    base_url = request_body['base_url']
  
    try:
        base_url = check_url(base_url)
    except Exception as err:
        print(f'invalid! {base_url} {err}' )
        return # TODO Handle exception here

    
    #subheadings = {4:'Apocrypha', 3:'Media', 10:'Media', 6:'Informational', 16:'Sidestory', 13:'Apocrypha', 19:'Informational'}
    # Each 'catagory', subset of the threadmarked posts, can be found with the format '{thread_url}/{number}/reader'
    # Exception is threadmarks, the main subset. 
    # The numbers corespond to each catagory as such:

    # Site: Spacebattles | Sufficient velocity
    # Sidestory:      16 |                  5
    # Apocyrpha       13 |                  4
    # Media:          10 |                  3
    # Informational:  19 |                  6

    if 'spacebattles' in base_url:
        catagories = [ 16, 13, 10, 19]
    else:
        catagories = [ 5, 4, 3, 6]

    options = []
    if request_body["sidestory"]:
        options.append(catagories[0])
    if request_body["apoc"]:
        options.append(catagories[1])
    if request_body["media"]:
        options.append(catagories[2])
    if request_body["info"]:
        options.append(catagories[3])

    #TODO Test options; test return
    obj = web_scraper()
    file_path = str(obj.webscrape(base_url, options))
    #Note: Remember that webscraper now grabs entire thread, not just first page.
    return HttpResponse(content=f'{settings.SITE_URL}{file_path}')

    #return
    #file = ContentFile(file_path)
    with open(file_path, 'rb') as f:
        file = f.read()
    response = HttpResponse(file, 'application/epub+zip')
    #response['Content-Length'] = file.size
    response['Content-Disposition'] = f'attachment; filename="{file_path[6:]}"'
    return response
    #Now, send FIle off to Client to download at leisure.
