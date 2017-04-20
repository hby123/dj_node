from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.test import Client
from django.test import TestCase

from dj_node.models import Review, Content
from dj_node.nodes.content import sample_data

my_email = "test@domain.com"
my_domain = "testserver"

class DjNodeReviewFormNodeTest(TestCase):
    URL_NAME = 'review-add'

    def setUp(self):
        sample_data()

    def test_review_form_get(self):
        c = Client()
        id = Content.objects.all().first().id
        content_type = ContentType.objects.get_for_model(Content)
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

    def test_review_form_post(self):
        review_count = Review.objects.all().count()
        c = Client()
        id = Content.objects.all().first().id
        content_type = ContentType.objects.get_for_model(Content)
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


class DjNodeReviewListNodeTest(TestCase):
    URL_NAME = 'review-list'

    def setUp(self):
        sample_data()

    def test_review_list(self):
        c = Client()
        id = Content.objects.all().first().id
        content_type = ContentType.objects.get_for_model(Content)
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
