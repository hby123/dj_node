
from django import forms
from dj_node.nodes.form import FormNode
from dj_node.models import  MaillingList
from dj_node.nodes.db import Db
from dj_node.nodes.list import ListInfo


class MailingListForm(FormNode, forms.Form):
    
    x_name = "MailingList"
    x_template = "user/mailing_form.html"
    x_parent_template = "empty.html"

    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
         super (MailingListForm, self).__init__(*args,**kwargs)
         if not self.request.user.is_authenticated(): 
            self.fields["verify_human"] = XRechapField(label = "Please verify you are human")

    def _process(self, request):
        email = request.POST.get('email')
        name = request.GET.get('mailing_list_name', 'primary')

        list_info = ListInfo(request)
        list_info.model = MaillingList
        list_info.filters = {'name':  {'name': u'name', 'val': name, 'op': '='},
                             'email': {'name': u'email', 'val': email, 'op': '='}}
        list_info = Db.get_list(request, list_info)

        if len(list_info.results) == 0: 
                e = MaillingList(site = request.site,
                                name = name,
                                email = email)
                e.save()

        return {self.XK_RETURN:self.XC_RETURN__REDIRECT, 
                self.XK_REDIRECT:'#' }

class MailingListDeleteForm(FormNode, forms.Form):
    
    x_name = "MailingList"
    x_template = None
    x_parent_template = None

    def __init__(self, *args, **kwargs):
         super (MailingListForm, self).__init__(*args,**kwargs)

    def _process(self, request):
        review =  request.POST.get('description') 
        filters = self.__class__._get_url_filters(request)

        user_id = None
        if request.user: 
            user_id = request.user.id
        
        list_info = ListInfo(request)
        list_info.model = MailingList
        list_info.filters = {'model':filters.get('model'), 
                            'instance_id':filters.get('instance_id'),
                            'user_id': {'name': u'user_id', 'val': user_id, 'op': '='}}
        list_info = Db.get_list(request, list_info)

        if len(list_info.results) == 1: 
            list_info.results[0].delete()
    
        return {'return':302,
                'redirect_url':'#' }


