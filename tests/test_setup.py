import sys 
from django.test import TestCase
from django.test import Client
from django.conf import settings
from django.contrib.auth.models import User
 
class dj_nodeSetupTest(TestCase):
    def setUp(self):
        pass

    def test_app_install(self):
        assert 'widget_tweaks' in settings.INSTALLED_APPS
        assert 'dj_node' in settings.INSTALLED_APPS

    def test_user_extra_fields(self):
        fields = [f.name for f in User._meta.local_fields]
        assert 'website' in fields
        assert 'actual_email' in fields
        assert 'display_name' in fields

    def test_index(self):
        c = Client()
        response = c.get('/')
        self.assertEqual(response.status_code, 200)
