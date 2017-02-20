import json

from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.test import Client
from django.test import TestCase

from dj_node.models import Comment, UserContent

my_email = "test@domain.com"
my_domain = "testserver"

class dj_nodeCommentFormNodeTest(TestCase):
    URL_NAME = 'comment-add'

    def setUp(self):
        UserContent.dummy()

    def test_comment_form_anonymous_get(self):
        c = Client()
        id = UserContent.objects.all().first().id
        content_type = ContentType.objects.get_for_model(UserContent)
        response = c.get(reverse(self.URL_NAME)+"content_type=%d&object_id=%s" % (id, content_type.id))
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')
        name_field = soup.find('input', {'name':'name'})
        assert name_field != None

        comment_field = soup.find('textarea', {'name':'comment'})
        assert comment_field != None

        rechapcha_field = soup.find('input', {'name':'verify_human'})
        assert rechapcha_field != None

    def test_comment_form_anonymous_post(self):
        comment_count = Comment.objects.all().count()
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
                'comment':'test',
                'verify_human':recap_code,
                'verify_human_path':recap_img_name}
        response = c.post(url, data,
                          #content_type='application/json',
                          #HTTP_X_REQUESTED_WITH='XMLHttpRequest'  Error with ajax request
                          )
        assert comment_count + 1 == Comment.objects.all().count()


    def test_comment_form_anonymous_invalid(self):
        comment_count = Comment.objects.all().count()
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
                #'comment':'test',
                'verify_human':recap_code,
                'verify_human_path':recap_img_name}
        response = c.post(url, data,
                          #content_type='application/json',
                          #HTTP_X_REQUESTED_WITH='XMLHttpRequest'  Error with ajax request
                          )
        assert comment_count  == Comment.objects.all().count()


        # send post
        data = {#'name':'123',
                'comment':'test',
                'verify_human':recap_code,
                'verify_human_path':recap_img_name}
        response = c.post(url, data,
                          #content_type='application/json',
                          #HTTP_X_REQUESTED_WITH='XMLHttpRequest'  Error with ajax request
                          )
        assert comment_count  == Comment.objects.all().count()


        # send post
        data = { 'name':'123',
                'comment':'test',
                'verify_human':'',
                'verify_human_path':recap_img_name}
        response = c.post(url, data,
                          #content_type='application/json',
                          #HTTP_X_REQUESTED_WITH='XMLHttpRequest'  Error with ajax request
                          )
        assert comment_count  == Comment.objects.all().count()


    def test_comment_form_login_valid(self):
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
        comment_count = Comment.objects.all().count()
        data = {'name':'123',
                'comment':'test'}
        id = UserContent.objects.all().first().id
        content_type = ContentType.objects.get_for_model(UserContent)
        url = reverse(self.URL_NAME)+"?content_type=%d&object_id=%d" % (content_type.id, id)
        response = c.post(url, data,
                          #content_type='application/json',
                          #HTTP_X_REQUESTED_WITH='XMLHttpRequest'  Error with ajax request
                          )
        print response.content
        assert comment_count + 1  == Comment.objects.all().count()


    def test_comment_form_login_invalid(self):
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
        comment_count = Comment.objects.all().count()
        data = {#'name':'123',
                'comment':'test'}
        content_type = ContentType.objects.get_for_model(UserContent)
        url = reverse(self.URL_NAME)+"?content_type=%d&object_id=%s" % (content_type.id, id)
        response = c.post(url, data,
                          #content_type='application/json',
                          #HTTP_X_REQUESTED_WITH='XMLHttpRequest'  Error with ajax request
                          )
        assert comment_count   == Comment.objects.all().count()

        # send post
        comment_count = Comment.objects.all().count()
        data = {'name':'123'}
        content_type = ContentType.objects.get_for_model(UserContent)
        url = reverse(self.URL_NAME)+"?content_type=%d&object_id=%s" % (content_type.id, id)
        response = c.post(url, data,
                          #content_type='application/json',
                          #HTTP_X_REQUESTED_WITH='XMLHttpRequest'  Error with ajax request
                          )
        assert comment_count  == Comment.objects.all().count()

class dj_nodeCommentListNodeTest(TestCase):
    URL_NAME = 'comment-list'

    def setUp(self):
        UserContent.dummy()

    def test_comment_list(self):

        c = Client()
        id = UserContent.objects.all().first().id
        content_type = ContentType.objects.get_for_model(UserContent)
        url = reverse('comment-add')+"?content_type=%d&object_id=%s" % (content_type.id, id)
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
        assert Comment.objects.all().count() == 0

        for i in range(1, 65):
            comment_count = Comment.objects.all().count()
            data = {'name':'123 %s' % str(i),
                    'comment':'test %s' % str(i),
                    'verify_human':recap_code,
                    'verify_human_path':recap_img_name}
            response = c.post(url, data,
                              #content_type='application/json',
                              #HTTP_X_REQUESTED_WITH='XMLHttpRequest'  Error with ajax request
                              )
            assert comment_count + 1 == Comment.objects.all().count()

        assert 64 == Comment.objects.all().count()

        # get multi page comments
        id_dict = {}
        content_type = ContentType.objects.get_for_model(UserContent)
        for i in range (1,5):
            url = reverse(self.URL_NAME)+"?content_type=%d&object_id=%s&page=%d" % (content_type.id, id, i)
            response = c.get(url, content_type='application/json',
                                  HTTP_X_REQUESTED_WITH='XMLHttpRequest')
            self.assertEqual(response.status_code, 200)

            #gert back id
            html = json.loads(response.content)['html']
            soup = BeautifulSoup(html, "html.parser")
            comment_li = soup.findAll("li", { "class" : "comment-item" })

            # test pagination list
            for li in comment_li:
                key = li['id'].split("-")[-1]
                if id_dict.has_key(key):
                    raise Exception("Dupliate comment: %s" % str(li))   # pragma: no cover
                id_dict[key] = ''
        assert len(id_dict.keys()) == Comment.objects.all().count()

