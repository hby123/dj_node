# ####
# #  I added TEST_RUNNER = "dj_node.test.testrunner.DiscoverRunner" to settings.py
# #  File dj_node.unittests.testrunner is copy from django/unittests/runner.py, and modified to
# #  use the dj_node.lib.HTMLTestRunner that I download from the internet.
# #
# #  This will allow the test result to be showin in HTML format.
# #  >> python manage.py test > test_result.html
# ###
#
# import time
# import urllib2
# from urllib2 import Request, urlopen, URLError, HTTPError
# from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# from django.test import TestCase
#
# class TestHelper(object):
#     @staticmethod
#     def collect_css(html):
#          soup = BeautifulSoup(html)
#          m = [ link["href"] for link in soup.findAll("link") if "stylesheet" in link.get("rel", [])]
#          return m
#
#     @staticmethod
#     def collect_js(html):
#         # <script src="/static/travel_site/theme_traveler/template/js/jquery.js"></script>
#         soup = BeautifulSoup(html)
#         m = []
#         for x in soup.findAll('script'):
#           try:
#             m.append(x['src'])
#           except KeyError:
#             pass
#         return m
#
#     @staticmethod
#     def collect_link(html):
#         soup = BeautifulSoup(html)
#         m = []
#         for x in soup.findAll('a'):
#             if x.has_attr('href'):
#                 m.append(x['href'])
#         return m
#
#     @staticmethod
#     def test_download(site, url):
#         if url.startswith("//"):
#             url = "http:" + url
#         else:
#           url  = site+url
#         print " testing to download url: %s" % url
#         req = urllib2.Request(url)
#
#
#         try:
#             urllib2.urlopen(req)
#         except URLError as e:
#             print e.reason
#             return False
#         return True
#
#     @staticmethod
#     def test_link(site, url):
#         if url.startswith("//"):
#             url = "http:" + url
#         else:
#           url  = site+url
#         print " testing to download url: %s" % url
#         req = urllib2.Request(url)
#
#         try:
#             urllib2.urlopen(req)
#         except URLError as e:
#             print e.reason
#             return False
#         return True
#
#     @staticmethod
#     def test_browse(site, url):
#         if url.startswith("//"):
#             url = "http:" + url
#         else:
#           url  = site+url
#
#         firefox = webdriver.Firefox()
#         firefox.get(url)
#         firefox.quit()
#         return True
#
#     @staticmethod
#     def fill_form(browser, form_dict):
#         for w in form_dict:
#             selector = w["selector"]
#             value = w["val"]
#
#             element =  browser.find_element_by_css_selector(selector)
#             element.send_keys(value)
#
#
# class TestPage(object):
#
#     def testCSS(self):
#         # open website
#         firefox = webdriver.Firefox()
#         firefox.get(self.site)
#         html = firefox.page_source
#
#         # test css links
#         css_links = TestHelper.collect_css(html)
#         print "css links: %s" % str(css_links)
#         for url in css_links:
#             css_download_flag = TestHelper.test_download(self.site, url)
#             self.assertEqual(css_download_flag, True)
#
#         # test false
#         css_download_flag = TestHelper.test_download(self.site, "/no-file.css")
#         self.assertEqual(css_download_flag, False)
#         firefox.quit()
#
#     def testJS(self):
#         # open website
#         firefox = webdriver.Firefox()
#         firefox.get(self.site)
#         html = firefox.page_source
#
#         # test js links
#         js_links = TestHelper.collect_js(html)
#         print "js links: %s" % str(js_links)
#         for url in js_links:
#             js_download_flag = TestHelper.test_download(self.site, url)
#             self.assertEqual(js_download_flag, True)
#
#         # test false
#         js_download_flag = TestHelper.test_download(self.site, "/no-file.js")
#         self.assertEqual(js_download_flag, False)
#         firefox.quit()
#
#     def testLinkHelper(self, page_url):
#         # open website
#         firefox = webdriver.Firefox()
#         firefox.get(page_url)
#         html = firefox.page_source
#         firefox.quit()
#
#         # test js links
#         links = TestHelper.collect_link(html)
#         for url in links:
#             download_flag = TestHelper.test_link(self.site, url)
#             self.assertEqual(download_flag, True)
#
#         # test false
#         download_flag = TestHelper.test_download(self.site, "/no-file/error-link/")
#         self.assertEqual(download_flag, False)
#
#
#
#
#
#
#
#