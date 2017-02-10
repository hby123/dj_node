from django import forms
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from dj_node.nodes.node import Node, NodeVariable
from dj_node.nodes.db import Db
from dj_node.models import UserContent
from dj_node.nodes.item import ItemNode
from dj_node.nodes.list import ListNode
from dj_node.nodes.form import FormNode, ModelFormNode

class UserContentListNode(ListNode):
    """Sample list node
    """
    x_model = UserContent
    x_item_url_name = 'user-content-item'
    x_list_url_name = 'user-content-list'
    x_option_filters = [ {'label':'A', 'name':'category_a'},
                         {'label':'B', 'name':'category_b'},
                       ]


class UserContentItemNode(ItemNode):
    """Sample item node
    """
    x_model = UserContent

class UserContentForm(forms.Form, NodeVariable):
    """Sample form for form node
    """
    name = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
         if kwargs.has_key('request'):
            self.request = kwargs['request']
            del kwargs['request']
         super (UserContentForm, self).__init__(*args,**kwargs)

    def _process(self, request):
        return {'return':'302',
                'redirect_url':'/' }


class UserContentFormNode(FormNode):
    """ Sample form node
    """
    x_form = UserContentForm
    x_model = UserContent



class UserContentModelForm(forms.ModelForm, forms.Form, NodeVariable):
    """Sample form for form node
    """
    class Meta:
        model = UserContent
        exclude = ['slug']

    def __init__(self, *args, **kwargs):
         if kwargs.has_key('request'):
            self.request = kwargs['request']
            del kwargs['request']
         super (UserContentModelForm, self).__init__(*args,**kwargs)

    def _process(self, request):
        self.instance.slug = slugify(self.instance.value),
        self.save()

        url = reverse('user-content-item', kwargs={'slug':self.instance.slug, 'id':self.instance.id})
        return {'return':'302',
                'redirect_url':url }


class UserContentModelFormNode(ModelFormNode):
    """ Sample form node
    """
    x_form = UserContentModelForm
    x_model = UserContent
