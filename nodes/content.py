import datetime
import factory
import factory.fuzzy
from dj_node.models import Content
from .item import ItemNode
from .list import ListNode

class ContentFactory(factory.django.DjangoModelFactory):
	rating = factory.fuzzy.FuzzyInteger(1, 5)
	value = factory.fuzzy.FuzzyText(length=30)
	date = factory.fuzzy.FuzzyDate(datetime.date(2016, 1, 1))
	class Meta:
		model = Content

def sample_data(count=105):
	'''
from dj_node.models import *
from dj_node.nodes.content import *
sample_data()
	'''
	print "Number of content before factory: %d" % Content.objects.count()
	[ContentFactory() for i in range(0, count)]
	print "Number of content after factory: %d" % Content.objects.count()

class ContentItemNode(ItemNode):
	x_model = Content
	
class ContentListNode(ListNode):
	x_model = Content
	x_list_url_name = 'content-list'
	x_item_url_name = 'content-item'
	x_option_filters = [{'label': 'Rating', 'name': 'rating'}]
	x_sort_list = ['date', '-date']