try:
    # Python 2.x
    from urlparse import urlsplit, urlunsplit
except ImportError:
    # Python 3.x
    from urllib.parse import urlsplit
    from urllib.parse import urlunsplit

from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import redirect
from dj_node.nodes.utils import Utils

class SiteLockMiddleware(object):

    def process_request(self, request):
        if not (request.session.get('site_lock') and request.session['site_lock'] == "1"):
            site_lock_url = reverse('site-lock')
            if request.path != site_lock_url:
                return redirect(site_lock_url)


# adopted from https://github.com/rdegges/django-sslify/blob/master/sslify/middleware.py
class SSLMiddelware(object):

    def process_request(self, request):
        site = Utils.get_site(request)
        # If the user has explicitly disabled SSLify, do nothing.
        if site['site_https'] == False:
            return None

        # Evaluate callables that can disable SSL for the current request
        per_request_disables = getattr(settings, 'SSLIFY_DISABLE_FOR_REQUEST', [])
        for should_disable in per_request_disables:
            if should_disable(request):
                return None

        # If we get here, proceed as normal.
        if site['site_has_ssl'] and (not request.is_secure()):
            url = request.build_absolute_uri(request.get_full_path())
            url_split = urlsplit(url)
            scheme = 'https' if url_split.scheme == 'http' else url_split.scheme
            ssl_port = 443
            url_secure_split = (scheme, "%s:%d" % (url_split.hostname or '', ssl_port)) + url_split[2:]
            secure_url = urlunsplit(url_secure_split)
            return HttpResponseRedirect(secure_url)


