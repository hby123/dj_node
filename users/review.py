from django import forms
from django.contrib.contenttypes.models import ContentType
from dj_node.models import Review
from dj_node.nodes.form import FormNode
from dj_node.nodes.list import ListNode


class ReviewForm(FormNode, forms.Form):

    name = forms.CharField(required=True, label="Name")
    description = forms.CharField(required=True, widget=forms.Textarea, label="Please tell us the detail")
    rating = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
         if kwargs.has_key('request'):
            self.request = kwargs['request']
            del kwargs['request']
         super (ReviewForm, self).__init__(*args,**kwargs)

         #add recaptcha
         #if not Utils.is_login(self.request):
         #   self = Utils.add_recaptcha_to_form(self.request, self)

    def _process(self, request):
        review =  request.POST.get('description')

        user_id = None
        if request.user: 
            user_id = request.user.id

        content_type_id = request.GET.get('content_type')
        content_type = ContentType.objects.get(id=content_type_id)

        e = Review(site = None,
                   display_name = request.POST.get('name', 'Somebody'),
                   user_id = user_id,
                   review = review,
                   date = None,
                   content_type = content_type,
                   object_id = int(request.GET.get('object_id')),
                   rating = int(request.POST.get('rating'), 0), )
        e.save()
        
        return {'return':302,
                'redirect_url':'#' }

class ReviewNode(FormNode):
    x_form = ReviewForm
    x_name = "Review"
    x_template = "users/review/z_form.html"
    x_parent_template = "empty.html"

    def _GET_data(self, request):
        return {'name':request.user.display_name}

class ReviewListNode(ListNode):
    x_model = Review
    x_template = "users/review/z_list_ajax.html"
    x_parent_template = "empty.html"
    x_skip_keys=["page", "sort", "profile"]

    def _extra(self, request, node_dict):
        extras = {}
        if request.GET.get('profile'):
            extras['flag_profile'] = True
        return extras

    
