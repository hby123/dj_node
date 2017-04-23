from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.test import Client
from django.test import TestCase

from dj_node.models import Bookmark, Content
from dj_node.nodes.content import sample_data

my_email = "test@domain.com"
my_domain = "testserver"

class DjNodeBookmarkTest(TestCase):

    def setUp(self):
        sample_data()

    def test_bookmark_button(self):
        self.assertTrue(Content.objects.all().count() > 50 )

        c = Client()
        user_content = Content.objects.all().first()
        url  = reverse('content-item') + "?id=%s" % user_content.id
        response = c.get(url)

        # check template
        assert str(user_content) in response.content

        soup = BeautifulSoup(response.content, "html.parser")
        btn = soup.find("button", { "class" : "bookmark" })
        assert btn == None

    def test_bookmark_action(self):
        # login user first
        assert User.objects.filter(actual_email=my_email).count() == 0

        # check template
        c = Client()
        response = c.get(reverse('logout'))
        response = c.get(reverse('sign-up'))
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')
        rechapcha_image = soup.find('img', {'class':'recap'})
        assert rechapcha_image != None
        assert rechapcha_image['src'] != None

        recap_img_url = rechapcha_image['src']
        recap_img_name = int(recap_img_url.split("/")[-1].split(".")[0])

        # find out the recap code
        from dj_node.nodes.extra.fields.recaptcha.var import recaptcha_dict
        recap_code = recaptcha_dict[recap_img_name]

        # send post
        data = {'email': 'test@domain.com',
                'display_name': 'My Name',
                'password': 'password',
                'confirm_password': 'password',
                'verify_human': recap_code,
                'verify_human_path': recap_img_name}
        response = c.post(reverse('sign-up'), data, follow=False)

        # check redirect
        assert response.url == "http://%s%s" % (str(my_domain), reverse('login'))
        self.assertEqual(response.status_code, 302)

        # check user
        assert User.objects.filter(actual_email=my_email).count() >  0

        # login
        response = c.get(reverse('logout'))
        data = {'email': 'test@domain.com',
                'password': 'password', }
        response = c.post(reverse('login'), data, follow=True) #NOTE: if a follows=False, the next few lines will fail.

        # save the bookmark
        assert Bookmark.objects.all().count() == 0
        user_content = Content.objects.all().first()
        content_type = ContentType.objects.get_for_model(Content)
        url = reverse('bookmark-add') + "?post_now=true&ajax=true&content_type=%d&object_id=%s" % (content_type.id, user_content.id)
        response = c.get(url)

        assert Bookmark.objects.all().count() == 1
        bookmark =  Bookmark.objects.all().first()
        assert bookmark.content_type == content_type
        assert bookmark.object_id == user_content.id
        assert bookmark.user_id != None
        assert bookmark.user_id != ''

        # check the page again
        url = reverse('content-item') + "?id=%s" % user_content.id
        response = c.get(url)

        # check template
        assert str(user_content) in response.content

        soup = BeautifulSoup(response.content, "html.parser")
        btn = soup.find("button", { "class" : "bookmark" })
        assert btn == None

