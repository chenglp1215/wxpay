from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'TheBest.views.home', name='home'),
    url(r'', include("pay.base.urls")),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    (r'^admin_media/(.*)$', 'django.views.static.serve', {'document_root': settings.WEB_ADMIN_MEDIA}),
    (r'^img/(.*)$', 'django.views.static.serve', {'document_root': settings.WEB_IMAGE}),
    (r'^css/(.*)$', 'django.views.static.serve', {'document_root': settings.WEB_STYLE}),
    (r'^js/(.*)$', 'django.views.static.serve', {'document_root': settings.WEB_SCRIPT}),
    (r'^html/(.*)$', 'django.views.static.serve', {'document_root': settings.WEB_HTML}),
    #(r'^static/(.*)$', 'django.views.static.serve', {'document_root': settings.STATICFILES_DIRS}),
)

