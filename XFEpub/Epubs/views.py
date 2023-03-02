
from django.http import HttpResponse

def epub_view(request, epub_path):
    if request.method != "GET":
        return
    with open('Epubs/'+epub_path, 'rb') as f:
        file = f.read()
        #Delete file?
    response = HttpResponse(file, 'application/epub+zip')
    #response['Content-Length'] = file.size
    response['Content-Disposition'] = f'attachment; filename="{epub_path}"'


    return response

