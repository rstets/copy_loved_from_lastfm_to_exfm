from django.shortcuts import render_to_response
from django.template import RequestContext
from .forms import LastFMSourceForm

def index(request):
    if request.method == 'POST':
        form = LastFMSourceForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = LastFMSourceForm()

    return render_to_response('extractor/index.html',
                              {'form': form},
                              context_instance=RequestContext(request))
