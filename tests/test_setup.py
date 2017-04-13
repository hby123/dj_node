import sys 
from django.test import TestCase
from django.test import Client
from django.conf import settings
from django.contrib.staticfiles import finders
from django.core.urlresolvers import reverse
from django.template import loader

class DjNodeSetupTest(TestCase):

    def test_app_install(self):
        assert 'django.contrib.sites' in settings.INSTALLED_APPS
        assert 'widget_tweaks' in settings.INSTALLED_APPS
        assert 'dj_node' in settings.INSTALLED_APPS

        self.assertTrue(settings.STATIC_URL)
        self.assertTrue(settings.STATIC_ROOT)

    def test_app_config(self):
        assert hasattr(settings, 'DJ_NODE_SITES')

        key = settings.DJ_NODE_SITES.keys()[0]
        site = settings.DJ_NODE_SITES[key]

        assert 'folder' in site.keys()
        assert 'theme' in site.keys()
        assert 'fallback_theme' in site.keys()
        assert 'site_code' in site.keys()
        assert 'ssl' in site.keys()
        assert 'anonymous_recaptcha' in site.keys()
        assert 'recaptcha_placeholder' in site.keys()
        assert 'recaptcha_class' in site.keys()
        assert 'django.core.context_processors.static' in settings.TEMPLATES[0]['OPTIONS']['context_processors']

    def test_templates(self):
        key = settings.DJ_NODE_SITES.keys()[0]
        site = settings.DJ_NODE_SITES[key]

        loader.get_template("dj_node/" + "themes/" + site['fallback_theme'] + "/" + "404.html")
        loader.get_template("dj_node/" + "themes/" + site['fallback_theme'] + "/" + "500.html")
        loader.get_template("dj_node/" + "themes/" + site['fallback_theme'] + "/" + "base.html")
        loader.get_template("dj_node/" + "themes/" + site['fallback_theme'] + "/" + "empty.html")
        loader.get_template("dj_node/" + "themes/" + site['fallback_theme'] + "/" + "error.html")
        loader.get_template("dj_node/" + "themes/" + site['fallback_theme'] + "/" + "index.html")
        loader.get_template("dj_node/" + "themes/" + site['fallback_theme'] + "/" + "step_parent.html")
        loader.get_template("dj_node/" + "themes/" + site['fallback_theme'] + "/" + "terms.html")

        loader.get_template("dj_node/" + "themes/" + site['fallback_theme'] + "/" + "form/form.html")
        loader.get_template("dj_node/" + "themes/" + site['fallback_theme'] + "/" + "form/z_form.html")
        loader.get_template("dj_node/" + "themes/" + site['fallback_theme'] + "/" + "item/item.html")
        loader.get_template("dj_node/" + "themes/" + site['fallback_theme'] + "/" + "list/list.html")
        loader.get_template("dj_node/" + "themes/" + site['fallback_theme'] + "/" + "list/z_filter_options.html")
        loader.get_template("dj_node/" + "themes/" + site['fallback_theme'] + "/" + "list/z_filter_selected.html")
        loader.get_template("dj_node/" + "themes/" + site['fallback_theme'] + "/" + "list/z_grid.html")
        loader.get_template("dj_node/" + "themes/" + site['fallback_theme'] + "/" + "list/z_info.html")
        loader.get_template("dj_node/" + "themes/" + site['fallback_theme'] + "/" + "list/z_pagination.html")
        loader.get_template("dj_node/" + "themes/" + site['fallback_theme'] + "/" + "list/z_sort.html")

        loader.get_template("dj_node/" + "themes/" + site['fallback_theme'] + "/" + "users/account/login.html")
        loader.get_template("dj_node/" + "themes/" + site['fallback_theme'] + "/" + "users/account/profile.html")
        loader.get_template("dj_node/" + "themes/" + site['fallback_theme'] + "/" + "users/account/sign_up.html")

        loader.get_template("dj_node/" + "themes/" + site['fallback_theme'] + "/" + "users/bookmark/sp_bookmark.html")
        loader.get_template("dj_node/" + "themes/" + site['fallback_theme'] + "/" + "users/bookmark/z_block.html")

        loader.get_template("dj_node/" + "themes/" + site['fallback_theme'] + "/" + "users/comment/z_block.html")
        loader.get_template("dj_node/" + "themes/" + site['fallback_theme'] + "/" + "users/comment/z_form.html")
        loader.get_template("dj_node/" + "themes/" + site['fallback_theme'] + "/" + "users/comment/z_list_ajax.html")

        loader.get_template("dj_node/" + "themes/" + site['fallback_theme'] + "/" + "users/email/mailing_form.html")

        loader.get_template("dj_node/" + "themes/" + site['fallback_theme'] + "/" + "users/password/forgot_password.html")
        loader.get_template("dj_node/" + "themes/" + site['fallback_theme'] + "/" + "users/password/reset_password.html")
        loader.get_template("dj_node/" + "themes/" + site['fallback_theme'] + "/" + "users/password/sp_change_password.html")

        loader.get_template("dj_node/" + "themes/" + site['fallback_theme'] + "/" + "users/review/rating.html")
        loader.get_template("dj_node/" + "themes/" + site['fallback_theme'] + "/" + "users/review/sp_review.html")
        loader.get_template("dj_node/" + "themes/" + site['fallback_theme'] + "/" + "users/review/z_block.html")
        loader.get_template("dj_node/" + "themes/" + site['fallback_theme'] + "/" + "users/review/z_form.html")
        loader.get_template("dj_node/" + "themes/" + site['fallback_theme'] + "/" + "users/review/z_list_ajax.html")

    def test_statics(self):
        self.assertTrue(finders.find('dj_node/lib/jquery-3.1.1.min.js'))
        self.assertTrue(finders.find('dj_node/js/ajax.js'))
        self.assertTrue(finders.find('dj_node/js/base.js'))

        self.assertTrue(finders.find('dj_node/themes/bootstrap/css/bootstrap.min.css'))
        self.assertTrue(finders.find('dj_node/themes/bootstrap/js/bootstrap.min.js'))
        self.assertFalse(finders.find('dj_node/themes/bootstrap/js/bootstrap.min.js.invalid'))

    def test_index(self):
        c = Client()
        response = c.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
