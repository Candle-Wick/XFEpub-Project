

#TODO test this
def epub_view(request, epub_path):
    if request.method != "GET":
        return
    with open(epub_path, 'rb') as f:
        file = f.read()
    response = HttpResponse(file, 'application/epub+zip')
    #response['Content-Length'] = file.size
    response['Content-Disposition'] = f'attachment; filename="{file_path[6:]}"'
    return response

