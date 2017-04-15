from .item import ItemNode
from .list import ListNode
from dj_node.models import Content

class ContentItem(ItemNode):
	x_model = Content
	
class ContentList(ListNode):
	x_model = Content
	

