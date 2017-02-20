from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from dj_node.models import UserContent, Review, Bookmark
from dj_node.nodes.item import ItemNode
from dj_node.nodes.node import Node

class ProfileStepParent(Node):
    x_step_parent_template = "profile_step_parent.html"
    def _extra(self, request):
        return {}

class ProfileNode(Node):
    x_template = "profile_step_parent.html"
    x_tab = "profile"

    def _extra(self, request):
        item_content_type = ContentType.objects.get_for_model(Review)
        return {'item_content_type':item_content_type}

    def _check(self, request):
        """ Extra function to check for permission.
        :param request - Django request object
        :return: bool, dict
        """
        display_name_slug = request.kwargs.get('display_name_slug')
        if User.objects.filter(display_name_slug__iexact=display_name_slug).count():
            return True, {}
        return False, {'return':302, 'redirect_url':'/?msg=invalid+name', 'msg': 'Sorry, that link was invalid.'}

class ProfileBookmarkNode(ProfileStepParent):
    x_perm = ['login']
    x_template = "users/bookmark/sp_bookmark.html"
    x_step_parent = ProfileStepParent
    x_tab = "bookmark"

class ProfileReviewNode(ProfileStepParent):
    x_perm = ['login']
    x_template = "users/review/sp_review.html"
    x_step_parent = ProfileStepParent
    x_tab = "review"