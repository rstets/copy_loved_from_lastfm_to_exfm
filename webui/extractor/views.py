from django.shortcuts import render_to_response
from django.template import RequestContext
from .forms import LastFMSourceForm

importers = {
    'lastfm': LastFMSourceForm
}

def _get_form(importer_name):
    if importer_name is None:
        importer_name = 'lastfm'
    return importers[importer_name]

def index(request, importer_name=None):
    Form = _get_form(importer_name)
    if request.method == 'POST':
        form = Form(request.POST)
        if form.is_valid():
            pass
    else:
        form = Form()

    return render_to_response('extractor/index.html',
                              {'form': form},
                              context_instance=RequestContext(request))

def playlists(request):
    return render_to_response('extractor/playlists.html')

def songs(request):
    return render_to_response('extractor/songs.html')
