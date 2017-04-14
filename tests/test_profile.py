from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import Client
from django.test import TestCase

my_email = "test@domain.com"
my_domain = "testserver"

class DjProfileTest(TestCase):

    def test_profile(self):
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
        response = c.post(reverse('sign-up'), data, follow=True) #NOTE: if a follows=False, the next few lines will fail.

        # check is user logged in
        assert response.context['user'].id != None
        assert response.context['user'].id != ""
        assert response.context['user'].id == User.objects.filter(actual_email=my_email)[0].id


        #2nd login
        response = c.get(reverse('login'))
        assert response.status_code == 302

        # test get profile page
        response = c.get(reverse('my-profile'))
        self.assertEqual(response.status_code, 200)

