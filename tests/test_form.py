# import math
# import time
# from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
#
# from django import forms
# from django.core.urlresolvers import reverse
# from django.test import TestCase
# from django.test import Client
# from dj_node.models import Content
# from dj_node.nodes.node import Node, NodeVariable
# from dj_node.nodes.form import FormNode, ModelFormNode
#
# class dj_nodeModelFormTest(TestCase):
#
#     URL_NAME = 'user-content-model-form'
#
#     def setUp(self):
#         Content.dummy()
#
#     def test_form_get(self):
#         self.assertTrue(Content.objects.all().count() > 50 )
#
#         c = Client()
#         user_content = Content.objects.all().first()
#         response = c.get(reverse(self.URL_NAME) + "?id=%d" % user_content.id)
#
#         # check template
#
#         # check field
#         soup = BeautifulSoup(response.content, 'html.parser')
#         value_field = soup.find('input', {'name':'value'})
#         assert value_field != None
#
#         submit_field = soup.find('button', {'type':'submit'})
#         assert submit_field != None
#
#     def test_form_post(self):
#         self.assertTrue(Content.objects.all().count() > 50 )
#
#         c = Client()
#         user_content = Content.objects.all().first()
#         url = reverse(self.URL_NAME) + "?id=%d" % user_content.id
#         response = c.post(url, {'value': 'new test value'}, follow=False)
#
#         user_content = Content.objects.get(id=user_content.id)
#         assert user_content.value == 'new test value'
#
#
#
#
#
