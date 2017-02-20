from bs4 import BeautifulSoup

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test import Client
from django.conf import settings
from django.test import TestCase, modify_settings


class SiteTestCase(TestCase):

    @modify_settings(MIDDLEWARE={
        'append': 'dj_node.middlewares.SiteLockMiddleware',
    })
    def test_site_lock(self):
        c = Client()
        response = c.get(reverse('site-lock'))

        soup = BeautifulSoup(response.content, 'html.parser')
        passcode = soup.find('input', {'name':'passcode'})
        assert passcode != None


        data = {'passcode':'6688'}
        response = c.post(reverse('site-lock'), data)

        response = c.get(reverse('index'))
        soup = BeautifulSoup(response.content, 'html.parser')
        passcode = soup.find('input', {'name':'passcode'})
        assert passcode == None

    @modify_settings(MIDDLEWARE={
        'append': 'dj_node.middlewares.SiteLockMiddleware',
    })
    def test_site_lock_invalid_code(self):
        c = Client()
        data = {'passcode':'0000'}
        response = c.post(reverse('site-lock'), data, follow=True)

        soup = BeautifulSoup(response.content, 'html.parser')
        passcode = soup.find('input', {'name':'passcode'})
        assert passcode != None

