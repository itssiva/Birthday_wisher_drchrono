from django.core.urlresolvers import reverse
from django.contrib.sitemaps import Sitemap
from django.shortcuts import render_to_response
from django.template import RequestContext


class BdayWisherSitemap(Sitemap):
    changefreq = "weekly"
    priority = 1.0

    def items(self):
        return ['home']

    def location(self, item):
        return reverse(item)


def handler_400(request):
    response = render_to_response('400.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler_403(request):
    response = render_to_response('403.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler_404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler_500(request):
    response = render_to_response('500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response
