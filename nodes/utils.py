import warnings
import requests

from django.core import urlresolvers
from django.conf import settings
from django.db.models.base import ModelBase
from django.db.models.manager import Manager
from django.db.models.query import QuerySet
from django.http import (
    Http404, HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect,
)
from django.template import RequestContext, loader
from django.template.context import _current_app_undefined
from django.template.engine import (
    _context_instance_undefined, _dictionary_undefined, _dirs_undefined,
)
from django.utils import six
from django.utils.deprecation import RemovedInDjango110Warning
from django.utils.encoding import force_text
from django.utils.functional import Promise

from django.conf import settings
from django.contrib import messages
from dj_node.nodes.extra.fields.recaptcha.recaptcha import XRecaptchaField

class Utils(object):
    """Uitls class for dj_node
    """

    # --- begin user related util functions
    @staticmethod
    def is_login(request):
        """Check is a user login
        """
        if hasattr(request, 'user') and request.user:
            return request.user.is_authenticated()
        return False

    @staticmethod
    def set_session(request, k, v):
        """Set a session key-value pair for current user
        """
        request.session[k] = v

    @staticmethod
    def del_session(request, k):
        """Set a session variable for current user
        """
        if request.session.has_key(k):
            del request.session[k]

    @staticmethod
    def set_msg(request, msg):
        """Set a message for the curent user
        """
        messages.add_message(request, messages.INFO, msg)
    
    @staticmethod
    def has_perm(request, perm):
        """ Check does user has permission
        """
        if perm == 'login':
            if request.user.is_authenticated(): 
                return True
        else:    # pragma: no cover
            if request.user.is_authenticated() and request.user.has_perm(perm):
                return True
        return False


    # --- begin site related util functions
    @staticmethod
    def get_mojo_domain(request):
        """Get the current site domain
        """
        try:
            domain = request.META['HTTP_HOST']
        except KeyError, e:
            domain = 'localhost'
        return domain
    
    @staticmethod
    def get_mojo_site(request):
        """Get the current site domain settings
        """
        domain = Utils.get_mojo_domain(request)
        domain = domain.split(":")[0]
        mojo_site = settings.DJ_NODE_SITES.get(domain)
        if not mojo_site: 
            mojo_site = settings.DJ_NODE_SITES.get('localhost')
        if not mojo_site:
            raise Exception("Oops, mojo_site settings not found")   # pragma: no cover
        return mojo_site

    @staticmethod
    def add_recaptcha_to_form(request, form):
        """Add recpatchat forom
        """
        mojo_site = Utils.get_mojo_site(request)
        if mojo_site and mojo_site.get('anonymous_recaptcha'):
            form.fields['verify_you_are_human'] = XRecaptchaField(label = "Please verify you are human")
            form.fields['verify_you_are_human'].widget.recaptcha_class = mojo_site.get('recaptcha_class')
            form.fields['verify_you_are_human'].widget.recaptcha_placeholder = mojo_site.get('recaptcha_placeholder')
        return form

    @staticmethod
    def render_to_string(template_name, context=None,
                           context_instance=_context_instance_undefined,
                           content_type=None, status=None, dirs=_dirs_undefined,
                           dictionary=_dictionary_undefined, using=None):
        """
        Returns a string whose content is filled with the result of calling
        django.template.loader.render_to_string() with the passed arguments.
        """
        if (context_instance is _context_instance_undefined
                and dirs is _dirs_undefined
                and dictionary is _dictionary_undefined):
            # No deprecated arguments were passed - use the new code path
            content = loader.render_to_string(template_name, context, using=using)

        else:
            # Some deprecated arguments were passed - use the legacy code path
            content = loader.render_to_string(
                template_name, context, context_instance, dirs, dictionary,
                using=using)
        return content

class EmailUtils(object):
    @staticmethod
    def send_email(from_address, to_address, subject, text):
        if settings.EMAIL_PROVIDER == 'mailgun':
            return EmailUtils.send_email_mailgun(settings.EMAIL_API_KEY, settings.EMAIL_API_URL,
                                                 from_address, to_address, subject, text)
        else:
            raise Exception("email not send")

    @staticmethod
    def send_email_mailgun(api_key, api_url, from_address, to_address, subject, text):
        return requests.post(
            api_url,
            auth=("api", api_key),
            data={"from": from_address,
                  "to": to_address,
                  "subject": subject,
                  "text": text})
