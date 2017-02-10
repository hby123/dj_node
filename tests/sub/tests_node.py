# from django.contrib.sites.models import Site
# from django.test import TestCase, RequestFactory
# from django.test import Client
# from dj_node.models import Comment
# from dj_node.nodes.item import ItemNode
#
# class TestItemNode(TestCase):
#     def setUp(self):
#         site = Site(domain="site.com")
#         site.save()
#
#         for i in range (0, 10):
#             c = Comment(site=site, comment = str(i) )
#             c.save()
#
#     def test_node(self):
#         class CommentItemNode(ItemNode):
#             pass
#         request = RequestFactory(data={'id':Comment.objecta.all()[0].id})
#
#     def _process(self, request):
#         result = {}
#         id = request.GET.get("id")
#         if self.X_model and id:
#             result['instance'] = Db.get_item(request, self.X_model, id)
#         return result
#
# class TestListNode(TestCase):
#     def setUp(self):
#         pass
#
#     def test_node(self):
#         pass
#
#     def test_filter(self):
#         pass
#
#     def test_sort(self):
#         pass
#
#     def test_pagination(self):
#         pass
#
# class TestFormNode(TestCase):
#     def setUp(self):
#         pass
#
#     def test_node(self):
#         pass
#
# class TestModelFormNode(TestCase):
#     def setUp(self):
#         pass
#
#     def test_node(self):
#         pass
#
#