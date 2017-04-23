from django import forms
from dj_node.nodes.node import Node
from dj_node.nodes.form import FormNode
from dj_node.nodes.utils import Utils

class SiteLockForm(forms.Form, Node):
    """Node-form used to lock down the site
    """
    passcode = forms.CharField(required=True, help_text="Please enter passcode to view the site.")

    def __init__(self, *args, **kwargs):
        """ Constructor
        :param request - Django request object
        """
        if kwargs.has_key('request'):
            self.request = kwargs['request']
            del kwargs['request']
        super(SiteLockForm, self).__init__(*args,**kwargs)

    def clean_passcode(self):
        """ check the passcode
        """
        passcode = self.cleaned_data.get('passcode', '')
        site = Utils.get_site(self.request)
        if site and site.get('site_code'):
                if site.get('site_code') != passcode:
                        raise forms.ValidationError("Invalid Password.")
        return passcode

    def _process(self, request):
        """ process the form
        """
        request.session['site_lock'] = "1"
        return {'return': 302,
                'redirect_url': '/' }

class SiteLockNode(FormNode):
    """Node used to lock down the site
    """
    x_form = SiteLockForm
