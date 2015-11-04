from django.conf.urls import patterns, include, url


urlpatterns = patterns("pay.base.views",
    url(r'^$', 'index'),
    url(r'^oauth/$', 'oauth'),
    url(r'^detail/$', 'detail'),
    url(r'^join/(?P<product_id>\d+)/$', 'join'),
    url(r'^share/(?P<ps_id>\d+)/(?P<pl_id>\d+)/$', 'share'),
    url(r'^order/$', 'order'),
    #url(r'^order/$', 'test'),
    url(r'^seller/(.+)/$', 'seller'),
    url(r'^buyer/(?P<pl_id>\d+)/$', 'buyer'),
    url(r'^pay_ok/$', 'pay_ok'),
    url(r'^alert/$', 'alert'),
    )