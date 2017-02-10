from dj_node.nodes.node import Node
from dj_node.nodes.db import Db
from dj_node.models import UserContent
from .list_info import ListInfo
from .list_filter import ListFilter

class ListNode(Node):
    x_model = None
    x_template = "list/list.html"
    x_item_url_name = None

    x_list_info_cls = ListInfo
    x_list_filter_cls = ListFilter

    x_sort_list = ['id', '-id']
    x_db_filters = []
    x_option_filters = []

    def _process(self, request):
        """ Process request
        :param request - Django request object
        :return: dict
        """

        # get list info and list filter
        list_info = self.x_list_info_cls(self, request)
        list_filter = self.x_list_filter_cls(self, request)

        # get the list
        list_info = Db.get_list(request, list_info, list_filter)

        # return
        node_dict = {'list_info':list_info, 'list_filter':list_filter, 'list_cls':self,
                     'return':200}
        return node_dict

