from django.conf.urls import include, url, handler400, handler403, handler404, handler500
from django.contrib import admin
from .views import BdayWisherSitemap


sitemaps = {
    'home': BdayWisherSitemap
}

urlpatterns = [

    url(r'^admin/', include(admin.site.urls)),
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    url(r'^robots\.txt$', include('robots.urls')),

    url(r'', include('Greeting.urls')),
    url(r'', include('UserAuth.urls')),
]

handler400 = 'Birthday_wisher_drchrono.views.handler_400'
handler403 = 'Birthday_wisher_drchrono.views.handler_403'
handler404 = 'Birthday_wisher_drchrono.views.handler_404'
handler500 = 'Birthday_wisher_drchrono.views.handler_500'
