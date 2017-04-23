from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import redirect


class SiteLockMiddleware(object):

    def process_request(self, request):
        if request.session.get('site_lock') and request.session['site_lock'] == "1":
            return
        lock_path = reverse('site-lock')
        if request.path != lock_path:
            return redirect(lock_path)


class SSLRedirect(object):

    def process_view(self, request, view_func, view_args, view_kwargs):
        flag = settings.DJ_NODE_SITES.get('ssl')
        if not flag:
            return None

        SSL = 'ssl'
        if SSL in view_kwargs:
            secure = view_kwargs[SSL]
            del view_kwargs[SSL]
        elif 'admin/login' in request.path:
        	secure = True
        else:
            secure = False

        if not secure == self._is_secure(request):
            protocol = secure and "https" or "http"
            newurl = "%s://%s%s" % (protocol, request.META['HTTP_HOST'] ,request.get_full_path())
            return HttpResponsePermanentRedirect(newurl)

    def _is_secure(self, request):
        if request.is_secure():
            return True
        # Handle the Webfaction case until this gets resolved in the request.is_secure()
        if 'HTTP_X_FORWARDED_SSL' in request.META:
            return request.META['HTTP_X_FORWARDED_SSL'] == 'on'
        return False

