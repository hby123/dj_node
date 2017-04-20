from django import forms
from django.contrib.contenttypes.models import ContentType

from dj_node.models import Comment
from dj_node.nodes.form import FormNode
from dj_node.nodes.list import ListNode
from dj_node.nodes.node import Node
from dj_node.nodes.utils import Utils


class CommentForm(forms.Form, Node):

    name = forms.CharField(required=True)
    comment = forms.CharField(widget=forms.Textarea, required=True)

    def __init__(self, *args, **kwargs):
         if kwargs.has_key('request'):
            self.request = kwargs['request']
            del kwargs['request']
         super (CommentForm, self).__init__(*args,**kwargs)

         #add recaptcha
         if not Utils.is_login(self.request):
            self = Utils.add_recaptcha_to_form(self.request, self)

    def _process(self, request):
        comment = request.POST.get('comment')
        e = Comment( site = None,
                     display_name = request.POST.get('name'),
                     user_id = None,
                     comment = comment,
                     date = None,
                     content_type = ContentType.objects.get(id=request.GET.get('content_type')),
                     object_id = int(request.GET.get('object_id')))
        e.save()

        # return
        return {'return':302,
                'redirect_url':'#' }

class CommentNode(FormNode):
    x_form = CommentForm
    x_name = "Comment"
    x_template = "users/comment/z_form.html"

class CommentListNode(ListNode):
    x_model = Comment
    x_template = "users/comment/z_list_ajax.html"
    x_parent_template = "empty.html"
    x_skip_keys=["page", "sort", "profile"]

    def _extra(self, request, node_dict):
        extras = {}
        if request.GET.get('profile'):
            extras['flag_profile'] = True
        return extras
