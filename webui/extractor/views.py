from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from .utils import get_importer
from urllib.parse import urlencode


def index(request, importer_name=None):
    importer = get_importer(importer_name, default=True)
    if request.method == 'POST':
        form = importer.Form(request.POST)
        if form.is_valid():
            qs = urlencode(form.cleaned_data)
            return redirect(reverse('playlists', kwargs={'importer_name':importer.name}) + '?'+qs)
    else:
        form = importer.Form()

    return render_to_response('extractor/index.html',
                              {'form': form},
                              context_instance=RequestContext(request))


def playlists(request, importer_name):
    importer = get_importer(importer_name)(request.GET)
    return render_to_response('extractor/playlists.html')


def songs(request, importer_name):
    importer = get_importer(importer_name)(request.GET)
    return render_to_response('extractor/songs.html')
