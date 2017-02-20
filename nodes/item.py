from django.contrib.contenttypes.models import ContentType

from dj_node.nodes.node import Node
from dj_node.nodes.db import Db
from dj_node.models import UserContent, Review, Bookmark

class ItemNode(Node):
    x_model = None
    x_template = "item/item.html"

    def _extra(self, request):
        content_type = ContentType.objects.get_for_model(self.x_model)
        return {'content_type':content_type}

    def _process(self, request):
        """ Process request
        :param request - Django request object
        :return: dict
        """

        node_dict = {}
        id = int(request.GET.get("id"))
        if self.x_model and id:
            node_dict['instance'] = Db.get_item(request, self.x_model, id)
            self.instance = node_dict['instance']
        node_dict['return'] = 200
        return node_dict
        