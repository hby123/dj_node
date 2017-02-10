from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.test import Client
from django.test import TestCase

from dj_node.models import Review, UserContent

my_email = "test@domain.com"
my_domain = "testserver"


class dj_nodeReviewFormNodeTest(TestCase):
    URL_NAME = 'review-add'

    def setUp(self):
        UserContent.dummy()

    def test_review_form_anonymous_get(self):
        c = Client()
        id = UserContent.objects.all().first().id
        content_type = ContentType.objects.get_for_model(UserContent)
        response = c.get(reverse(self.URL_NAME)+"?content_type=%d&object_id=%s" % (content_type.id, id))
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')
        name_field = soup.find('input', {'name':'name'})
        assert name_field != None

        rating_field = soup.find('input', {'name':'rating'})
        assert rating_field != None

        desc_field = soup.find('textarea', {'name':'description'})
        assert desc_field != None

        rechapcha_field = soup.find('input', {'name':'verify_human'})
        assert rechapcha_field != None

    def test_review_form_anonymous_post(self):
        review_count = Review.objects.all().count()
        c = Client()
        id = UserContent.objects.all().first().id
        content_type = ContentType.objects.get_for_model(UserContent)
        url = reverse(self.URL_NAME)+"?content_type=%d&object_id=%s" % (content_type.id, id)
        response = c.get(url)
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
        data = {'name':'123',
                'rating':'5',
                'description':'This is my description',
                'verify_human':recap_code,
                'verify_human_path':recap_img_name}
        response = c.post(url, data,
                          #content_type='application/json',
                          #HTTP_X_REQUESTED_WITH='XMLHttpRequest'  Error with ajax request
                          )
        assert review_count + 1 == Review.objects.all().count()


    def test_review_form_anonymous_invalid(self):
        review_count = Review.objects.all().count()
        c = Client()
        id = UserContent.objects.all().first().id
        content_type = ContentType.objects.get_for_model(UserContent)
        url = reverse(self.URL_NAME)+"?content_type=%d&object_id=%s" % (content_type.id, id)
        response = c.get(url)
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
        data = {'name':'123',
                #'rating':'5',
                'description':'This is my description',
                'verify_human':recap_code,
                'verify_human_path':recap_img_name}
        response = c.post(url, data,
                          #content_type='application/json',
                          #HTTP_X_REQUESTED_WITH='XMLHttpRequest'  Error with ajax request
                          )
        assert review_count  == Review.objects.all().count()


        # send post
        data = {#'name':'123',
                'rating':'5',
                'description':'This is my description',
                'verify_human':recap_code,
                'verify_human_path':recap_img_name}
        response = c.post(url, data,
                          #content_type='application/json',
                          #HTTP_X_REQUESTED_WITH='XMLHttpRequest'  Error with ajax request
                          )
        assert review_count  == Review.objects.all().count()


        # send post
        data = {'name':'123',
                'rating':'5',
                'description':'This is my description',
                'verify_human':'',
                'verify_human_path':recap_img_name}
        response = c.post(url, data,
                          #content_type='application/json',
                          #HTTP_X_REQUESTED_WITH='XMLHttpRequest'  Error with ajax request
                          )
        assert review_count  == Review.objects.all().count()


    def test_review_form_login_valid(self):
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


        # send post
        review_count = Review.objects.all().count()
        data = {'name':'123',
                'rating':'5',
                'description':'This is my description',}
        id = UserContent.objects.all().first().id
        content_type = ContentType.objects.get_for_model(UserContent)
        url = reverse(self.URL_NAME)+"?content_type=%d&object_id=%d" % (content_type.id, id)
        response = c.post(url, data,
                          #content_type='application/json',
                          #HTTP_X_REQUESTED_WITH='XMLHttpRequest'  Error with ajax request
                          )
        assert review_count + 1  == Review.objects.all().count()


    def test_review_form_login_invalid(self):
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


        # send post
        review_count = Review.objects.all().count()
        data = {#'name':'123',
                'rating':'5',
                'description':'This is my description',
                }
        content_type = ContentType.objects.get_for_model(UserContent)
        url = reverse(self.URL_NAME)+"?content_type=%d&object_id=%s" % (content_type.id, id)
        response = c.post(url, data,
                          #content_type='application/json',
                          #HTTP_X_REQUESTED_WITH='XMLHttpRequest'  Error with ajax request
                          )
        assert review_count   == Review.objects.all().count()

        # send post
        review_count = Review.objects.all().count()
        data = {'name':'123',
                #'rating':'5',
                'description':'This is my description',
               }
        content_type = ContentType.objects.get_for_model(UserContent)
        url = reverse(self.URL_NAME)+"?content_type=%d&object_id=%s" % (content_type.id, id)
        response = c.post(url, data,
                          #content_type='application/json',
                          #HTTP_X_REQUESTED_WITH='XMLHttpRequest'  Error with ajax request
                          )
        assert review_count  == Review.objects.all().count()

class dj_nodeReviewListNodeTest(TestCase):
    URL_NAME = 'review-list'

    def setUp(self):
        UserContent.dummy()

    def test_review_list(self):
        c = Client()
        id = UserContent.objects.all().first().id
        content_type = ContentType.objects.get_for_model(UserContent)
        url = reverse('review-add')+"?content_type=%d&object_id=%s" % (content_type.id, id)
        response = c.get(url)
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
        assert Review.objects.all().count() == 0

        for i in range(1, 65):
            review_count = Review.objects.all().count()
            data = {'name':'123',
                    'rating':'5',
                    'description':'This is my description',
                    'verify_human':recap_code,
                    'verify_human_path':recap_img_name}
            response = c.post(url, data,
                              #content_type='application/json',
                              #HTTP_X_REQUESTED_WITH='XMLHttpRequest'  Error with ajax request
                              )
            assert review_count + 1 == Review.objects.all().count()

        assert 64 == Review.objects.all().count()

        # get multi page reviews
        id_dict = {}
        for i in range (1,5):
            url = reverse(self.URL_NAME)+"?content_type=%d&object_id=%s&page=%d" % (content_type.id, id, i)
            response = c.get(url)
            self.assertEqual(response.status_code, 200)

            #gert back id
            soup = BeautifulSoup(response.content, "html.parser")
            review_li = soup.findAll("li", { "class" : "review-item" })

            # test pagination list
            for li in review_li:
                key = li['id'].split("-")[-1]
                if id_dict.has_key(key):
                    raise Exception("Dupliate review: %s" % str(li))    # pragma: no cover
                id_dict[key] = ''
        assert len(id_dict.keys()) == Review.objects.all().count()

