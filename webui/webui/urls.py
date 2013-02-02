from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'extractor.views.index', name='index'),
    url(r'^playlists/(?P<importer_name>\w+)$', 'extractor.views.playlists', name='playlists'),
    url(r'^songs$', 'extractor.views.songs', name='songs'),
    url(r'^search$', 'extractor.views.search', name='search'),
    url(r'^process$', 'extractor.views.process', name='process')
    # url(r'^webui/', include('webui.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
