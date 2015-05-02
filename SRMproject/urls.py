from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = [
    url(r'^SRMapp/', include('SRMapp.urls')),
    url(r'^admin/', include(admin.site.urls)),
]


admin.site.site_header = 'SRM App Administration'