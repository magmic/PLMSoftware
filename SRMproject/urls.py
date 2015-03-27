from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'SRMproject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    #url(r'^products/', include(products.urls)),
    url(r'^products/', products.views.index, name='index'),
    url(r'', include(admin.site.urls)),
)
