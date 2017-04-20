from django import forms
from django.contrib.contenttypes.models import ContentType

from dj_node.models import Bookmark
from dj_node.nodes.form import FormNode
from dj_node.nodes.list import ListNode
from dj_node.nodes.node import Node


class BookmarkListNode(ListNode):
    x_model = Bookmark
    x_template = "users/bookmark/z_list_ajax.html"
    x_parent_template = "empty.html"

    def _extra(self, request, node_dict):
        extras = {}
        if request.GET.get('profile'):
            extras['flag_profile'] = True
        return extras


class BookmarkForm(forms.Form, Node):
    
    x_name = "Bookmark"
    x_template = None
    x_parent_template = None


    def __init__(self, *args, **kwargs):
         if kwargs.has_key('request'):
            self.request = kwargs['request']
            del kwargs['request']
         super (BookmarkForm, self).__init__(*args,**kwargs)

    def _process(self, request):
        user_id = request.user.id
        content_type = ContentType.objects.get(id=request.GET.get('content_type'))
        object_id = int(request.GET.get('object_id'))

        if not Bookmark.objects.filter(user_id=user_id, content_type=content_type,object_id = object_id ).count():
            e = Bookmark(display_name='',
                         user_id = user_id,
                         content_type = content_type,
                         object_id = object_id,)
            e.save()
        return {'return': 302,
                'redirect_url': '#'}


class BookmarkNode(FormNode):
    x_form = BookmarkForm
    x_name = "Bookmark"
    x_template = None
    x_parent_template = None
    x_process_get = True




    
