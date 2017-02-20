import datetime
from django import template
from django.template.defaultfilters import slugify
from django import template

register = template.Library()

def dj_node_include(parser, token):
    name, format_string = token.split_contents()
    return dj_nodeIncludeNode(format_string)


class dj_nodeIncludeNode(template.Node):
    def __init__(self, format_string):
        self.format_string = format_string
    
    def render(self, context):
        from dj_node.nodes.node import Node
        token_list = self.format_string.split("|")
        filename = Node.fallback_template(context['request'], token_list[0])
        context[token_list[-1]] = filename
        return ""


def dj_node_is_selected(parser, token):
    name, format_string = token.split_contents()
    return dj_nodeIsSelectedNode(format_string)


class dj_nodeIsSelectedNode(template.Node):
    def __init__(self, format_string):
        self.format_string = format_string

    def render(self, context):
        token_list = self.format_string.split("|")
        selected_filters = template.Variable(token_list[0]).resolve(context)
        current_filter_label = token_list[1]
        current_filter_value = token_list[2]
        flag_var = token_list[3]
        return ""


def dj_node_bookmark(parser, token):
    name, format_string = token.split_contents()
    return BookmarkNode(format_string)


class BookmarkNode(template.Node):
    def __init__(self, format_string):
        self.format_string = format_string
    
    def render(self, context):
        token_list = self.format_string.split("|")
        content_type = template.Variable(token_list[0]).resolve(context)
        object = template.Variable(token_list[1]).resolve(context)

        request = context['request']
        user = request.user

        bookmark_flag = False
        if request.user.is_authenticated():
            from dj_node.models import Bookmark
            if Bookmark.objects.filter(content_type=content_type).filter(object_id=object.id).filter(user_id=user.id).count():
                bookmark_flag = True
        context[token_list[-1]] = bookmark_flag
        return ""

register.tag('dj_node_bookmark', dj_node_bookmark)
register.tag('dj_node_include', dj_node_include)


