# import math
# import time
# from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
#
# from django.core.urlresolvers import reverse
# from django.test import TestCase
# from django.test import Client
# from django.test.client import RequestFactory
# from dj_node.models import UserContent
# from dj_node.models import UserContent
# from dj_node.nodes.db import Db
# from dj_node.nodes.user_content import UserContentListNode
# from dj_node.nodes.list_info import ListInfo
# from dj_node.nodes.list_filter import ListFilter
#
# class dj_nodeDbTest(TestCase):
#
#     def setUp(self):
#         UserContent.dummy()
#
#     def test_save(self):
#         user_content = UserContent.objects.all().first()
#         user_content.value = "updated val 123"
#         Db.save_item(None, user_content)
#
#         user_content = UserContent.objects.all().first()
#         assert(user_content.value == "updated val 123")
#
#     def test_get_list_simple(self):
#         factory = RequestFactory()
#         request = factory.get(reverse('user-content-list'))
#         user_content_list = Db.get_list_simple(request, UserContent, filters={'category_a':'category 1'})
#         assert len(user_content_list) > 0
#
#         for user_content in user_content_list:
#             assert user_content.category_a == 'category 1'
#
#     def test_get_list_no_paging(self):
#         factory = RequestFactory()
#         request = factory.get(reverse('user-content-list'))
#         list_info = ListInfo(UserContentListNode, request)
#         list_filter = ListFilter(UserContentListNode, request)
#         list_info.ipp = -1
#
#         list_info = Db.get_list(request, list_info, list_filter)
#         assert len(list_info.results) > 0
