try:
    # Python 2.x
    from urlparse import urlsplit, urlunsplit
except ImportError:
    # Python 3.x
    from urllib.parse import urlsplit
    from urllib.parse import urlunsplit

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from dj_node.nodes.utils import Utils

class SiteLockMiddleware(object):

    def process_request(self, request):
        if not (request.session.get('site_lock') and request.session['site_lock'] == "1"):
            site_lock_url = reverse('site-lock')
            if request.path != site_lock_url:
                return redirect(site_lock_url)


class SSLMiddelware(object):

    def process_request(self, request):
        if not request.is_secure():
            # get secure url
            site = Utils.get_site(request)
            url = request.build_absolute_uri(request.get_full_path())
            url_split = urlsplit(url)
            scheme = 'https' if url_split.scheme == 'http' else url_split.scheme
            ssl_port = 443
            url_secure_split = (scheme, "%s:%d" % (url_split.hostname or '', ssl_port)) + url_split[2:]
            secure_url = urlunsplit(url_secure_split)

            # enforce url for site
            if (site['site_https'] and site['site_has_ssl']):
                return HttpResponseRedirect(secure_url)

            # enforce https for /admin
            if (request.get_full_path().lower().startswith('/admin') and site['site_has_ssl']):
                return HttpResponseRedirect(secure_url)
