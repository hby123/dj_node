from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import Client
from django.test import TestCase

my_email = "test@domain.com"
my_domain = "testserver"

class DjNodeAccountBaseTest(TestCase):
    URL_NAME = "login"

    def test_login_post(self):
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
        response = c.post(reverse(self.URL_NAME), data, follow=True) #NOTE: if a follows=False, the next few lines will fail.

        # check is user logged in
        assert response.context['user'].id != None
        assert response.context['user'].id != ""
        assert response.context['user'].id == User.objects.filter(actual_email=my_email)[0].id

class DjNodeSignUpTest(TestCase):
    URL_NAME = "sign-up"

    def test_signup_get(self):
        # check template
        c = Client()
        response = c.get(reverse(self.URL_NAME))
        self.assertEqual(response.status_code, 200)

        # check fields
        soup = BeautifulSoup(response.content, 'html.parser')
        email_field = soup.find('input', {'name':'email'})
        assert email_field != None

        password_field = soup.find('input', {'name':'password'})
        assert password_field != None

        password_field = soup.find('input', {'name':'confirm_password'})
        assert password_field != None

        submit_field = soup.find('input', {'type':'submit'})
        assert submit_field != None

        rechapcha_field = soup.find('input', {'name':'verify_human'})
        assert rechapcha_field != None

        rechapcha_image = soup.find('img', {'class':'recap'})
        assert rechapcha_image != None
        assert rechapcha_image['src'] != None

        img_url = rechapcha_image['src']
        assert img_url != ""
        assert img_url != None


    def test_signup_post(self):
        assert User.objects.filter(actual_email=my_email).count() == 0

        # check template
        c = Client()
        response = c.get(reverse('logout'))
        response = c.get(reverse(self.URL_NAME))
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
        response = c.post(reverse(self.URL_NAME), data, follow=False)

        # check redirect
        assert response.url == "http://%s%s" % (str(my_domain), reverse('login'))
        self.assertEqual(response.status_code, 302)

        # check user
        assert User.objects.filter(actual_email=my_email).count() >  0

    def test_signup_email_twice(self):
        assert User.objects.filter(actual_email=my_email).count() == 0

        # check template
        c = Client()
        response = c.get(reverse('logout'))
        response = c.get(reverse(self.URL_NAME))
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
        response = c.post(reverse(self.URL_NAME), data, follow=False)
        assert response.status_code == 302
        assert User.objects.filter(actual_email=my_email).count() >  0

        # 2nd post
        response = c.get(reverse('logout'))
        data = {'email': 'test@domain.com',
                'display_name': 'My Name',
                'password': 'password',
                'confirm_password': 'password',
                'verify_human': recap_code,
                'verify_human_path': recap_img_name}
        response = c.post(reverse(self.URL_NAME), data, follow=False)
        assert "email already exists" in response.content

    def test_signup_display_name_twice(self):
        assert User.objects.filter(actual_email=my_email).count() == 0

        # check template
        c = Client()
        response = c.get(reverse('logout'))
        response = c.get(reverse(self.URL_NAME))
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
        response = c.post(reverse(self.URL_NAME), data, follow=False)
        assert response.status_code == 302
        assert User.objects.filter(actual_email=my_email).count() >  0

        # 2nd post
        response = c.get(reverse('logout'))
        data = {'email': 'test2@domain.com',
                'display_name': 'My Name',
                'password': 'password',
                'confirm_password': 'password',
                'verify_human': recap_code,
                'verify_human_path': recap_img_name}
        response = c.post(reverse(self.URL_NAME), data, follow=False)
        assert response.status_code != 302

    def test_signup_invalid_display_name(self):
        assert User.objects.filter(actual_email=my_email).count() == 0

        # check template
        c = Client()
        response = c.get(reverse('logout'))
        response = c.get(reverse(self.URL_NAME))
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
                'display_name': 'ab',
                'password': 'password',
                'confirm_password': 'password',
                'verify_human': recap_code,
                'verify_human_path': recap_img_name}
        response = c.post(reverse(self.URL_NAME), data, follow=False)
        assert response.status_code != 302
        assert User.objects.filter(actual_email=my_email).count() ==  0

    def test_signup_invalid_password(self):
        assert User.objects.filter(actual_email=my_email).count() == 0

        # check template
        c = Client()
        response = c.get(reverse('logout'))
        response = c.get(reverse(self.URL_NAME))
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
                'display_name': 'ab',
                'password': '1234',
                'confirm_password': '1234',
                'verify_human': recap_code,
                'verify_human_path': recap_img_name}
        response = c.post(reverse(self.URL_NAME), data, follow=False)
        assert response.status_code != 302
        assert User.objects.filter(actual_email=my_email).count() ==  0

    def test_signup_after_login(self):
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
        response = c.post(reverse('login'), data, follow=True)

        # check is user logged in
        assert response.context['user'].id != None
        assert response.context['user'].id != ""
        assert response.context['user'].id == User.objects.filter(actual_email=my_email)[0].id

        response = c.get(reverse('sign-up'), data, follow=False)
        assert  response.status_code == 302

class DjNodeLoginTest(DjNodeAccountBaseTest):
    URL_NAME = "login"

    def test_login_get(self):
        # check template
        c = Client()
        response = c.get(reverse(self.URL_NAME))
        self.assertEqual(response.status_code, 200)

        # check email, password, and submit elements
        soup = BeautifulSoup(response.content, 'html.parser')
        email_field = soup.find('input', {'name':'email'})
        assert email_field != None

        password_field = soup.find('input', {'name':'password'})
        assert password_field != None

        submit_field = soup.find('input', {'type':'submit'})
        assert submit_field != None

        # check sign up and forgot password links
        flag_signup_link = False
        flag_forgot_password_link = False
        for link in soup.findAll('a', href=True):
            if "sign up" in link.text.lower():
                url = link['href']
                response = c.get(url)
                self.assertEqual(response.status_code, 200)
                flag_signup_link = True
            elif "forgot password" in link.text.lower():
                url = link['href']
                response = c.get(url)
                self.assertEqual(response.status_code, 200)
                flag_forgot_password_link = True

        assert flag_signup_link == True
        assert flag_forgot_password_link == True


    def test_login_after_login(self):
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
        response = c.post(reverse(self.URL_NAME), data, follow=True) #NOTE: if a follows=False, the next few lines will fail.

        # check is user logged in
        assert response.context['user'].id != None
        assert response.context['user'].id != ""
        assert response.context['user'].id == User.objects.filter(actual_email=my_email)[0].id


        #2nd login
        response = c.get(reverse('login'))
        assert response.status_code == 302

    def test_login_incorrect_email_and_incorret_password(self):
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
        data = {'email': 'incorrect@domain.com',
                'password': 'incorrect', }
        response = c.post(reverse(self.URL_NAME), data, follow=True) #NOTE: if a follows=False, the next few lines will fail.

        # check is user logged in
        assert response.context['user'].id == None

    def test_login_incorret_password(self):
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
                'password': 'incorrect', }
        response = c.post(reverse(self.URL_NAME), data, follow=True) #NOTE: if a follows=False, the next few lines will fail.

        # check is user logged in
        assert response.context['user'].id == None

    def test_login_locked_account(self):
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

        user = User.objects.filter(actual_email=my_email).first()
        user.is_active = False
        user.save()

        # login
        response = c.get(reverse('logout'))
        data = {'email': 'test@domain.com',
                'password': 'password', }
        response = c.post(reverse(self.URL_NAME), data, follow=True) #NOTE: if a follows=False, the next few lines will fail.
        assert "account is locked" in response.content

class DjNodeLogoutTest(TestCase):
    URL_NAME = "logout"

    def test_logout(self):
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

        # check is user logged in
        assert response.context['user'].id != None
        assert response.context['user'].id != ""
        assert response.context['user'].id == User.objects.filter(actual_email=my_email)[0].id

        response = c.get(reverse(self.URL_NAME), follow=True)

        # check if user still logged in
        user_id = response.context['user'].id
        assert user_id == None


class DjNodeForgotPasswordTest(TestCase):
    URL_NAME = "forgot-password"

    def test_forgot_password_get(self):
        # check template
        c = Client()
        response = c.get(reverse(self.URL_NAME))
        self.assertEqual(response.status_code, 200)

        # check email, password, and submit elements
        soup = BeautifulSoup(response.content, 'html.parser')
        email_field = soup.find('input', {'name':'email'})
        assert email_field != None

        submit_field = soup.find('input', {'type':'submit'})
        assert submit_field != None

        rechapcha_field = soup.find('input', {'name':'verify_human'})
        assert rechapcha_field != None

        rechapcha_image = soup.find('img', {'class':'recap'})
        assert rechapcha_image != None
        assert rechapcha_image['src'] != None

        img_url = rechapcha_image['src']
        assert img_url != ""
        assert img_url != None


    def test_forgotpassword_post(self):
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
        data = {'email': my_email,
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

        # logout
        response = c.get(reverse('logout'), follow=True)
        user_id = response.context['user'].id
        assert user_id == None

        # retive my password
        response = c.get(reverse(self.URL_NAME))

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
        data = {'email': my_email,
                'verify_human': recap_code,
                'verify_human_path': recap_img_name}
        response = c.post(reverse(self.URL_NAME), data, follow=True)
        assert "check your email" or "diffculty to send you email" in  response.content

    def test_forgotpassword_wrong_email(self):
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
        data = {'email': my_email,
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

        # logout
        response = c.get(reverse('logout'), follow=True)
        user_id = response.context['user'].id
        assert user_id == None

        # retive my password
        response = c.get(reverse(self.URL_NAME))

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
        data = {'email': 'wrong@domain.com',
                'verify_human': recap_code,
                'verify_human_path': recap_img_name}
        response = c.post(reverse(self.URL_NAME), data)
        assert "Please enter valid email" in response.content


class DjNodeResetPasswordTest(TestCase):
    URL_NAME = "reset-password"

    def test_forgotpassword_post(self):
        #
        # fill out a forgot password form first
        #
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
        data = {'email': my_email,
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

        # logout
        response = c.get(reverse('logout'), follow=True)
        user_id = response.context['user'].id
        assert user_id == None

        # retive my password
        response = c.get(reverse('forgot-password'))

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
        data = {'email': my_email,
                'verify_human': recap_code,
                'verify_human_path': recap_img_name}
        response = c.post(reverse('forgot-password'), data, follow=True)

        #
        # go to the reset password page
        #
        from dj_node.models import Token
        t = Token.objects.filter(email=my_email).first()
        url = response = reverse(self.URL_NAME,  kwargs={'code':t.token})
        response = c.post(url,  follow=True)

        # check fields
        soup = BeautifulSoup(response.content, 'html.parser')
        email_field = soup.find('input', {'name':'new_password'})
        assert email_field != None

        password_field = soup.find('input', {'name':'confirm_password'})
        assert password_field != None

        #
        # POST the reset password page
        #
        data = {'new_password':     'abc123',
                'confirm_password': 'abc123',}
        response = c.post(url, data, follow=True)


        #
        # attemp log in again
        #
        response = c.get(reverse('logout'))
        data = {'email': my_email,
                'password': 'abc123', }
        response = c.post(reverse('login'), data, follow=True) #NOTE: if a follows=False, the next few lines will fail.

        # check is user logged in
        assert response.context['user'].id != None
        assert response.context['user'].id != ""
        assert response.context['user'].id == User.objects.filter(actual_email=my_email)[0].id


    def test_forgotpassword_new_password_not_meet_requirment(self):
        #
        # fill out a forgot password form first
        #
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
        data = {'email': my_email,
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

        # logout
        response = c.get(reverse('logout'), follow=True)
        user_id = response.context['user'].id
        assert user_id == None

        # retive my password
        response = c.get(reverse('forgot-password'))

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
        data = {'email': my_email,
                'verify_human': recap_code,
                'verify_human_path': recap_img_name}
        response = c.post(reverse('forgot-password'), data, follow=True)

        #
        # go to the reset password page
        #
        from dj_node.models import Token
        t = Token.objects.filter(email=my_email).first()
        url = response = reverse(self.URL_NAME,  kwargs={'code':t.token})
        response = c.post(url,  follow=True)

        # check fields
        soup = BeautifulSoup(response.content, 'html.parser')
        email_field = soup.find('input', {'name':'new_password'})
        assert email_field != None

        password_field = soup.find('input', {'name':'confirm_password'})
        assert password_field != None

        #
        # POST the reset password page
        #
        data = {'new_password':     '12',
                'confirm_password': '12',}
        response = c.post(url, data, follow=True)


        #
        # attemp log in again
        #
        response = c.get(reverse('logout'))
        data = {'email': my_email,
                'password': '12', }
        response = c.post(reverse('login'), data, follow=True) #NOTE: if a follows=False, the next few lines will fail.

        # check is user logged in
        assert response.context['user'].id == None

    def test_forgotpassword_mismatch_new_password(self):
        #
        # fill out a forgot password form first
        #
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
        data = {'email': my_email,
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

        # logout
        response = c.get(reverse('logout'), follow=True)
        user_id = response.context['user'].id
        assert user_id == None

        # retive my password
        response = c.get(reverse('forgot-password'))

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
        data = {'email': my_email,
                'verify_human': recap_code,
                'verify_human_path': recap_img_name}
        response = c.post(reverse('forgot-password'), data, follow=True)

        #
        # go to the reset password page
        #
        from dj_node.models import Token
        t = Token.objects.filter(email=my_email).first()
        url = response = reverse(self.URL_NAME,  kwargs={'code':t.token})
        response = c.post(url,  follow=True)

        # check fields
        soup = BeautifulSoup(response.content, 'html.parser')
        email_field = soup.find('input', {'name':'new_password'})
        assert email_field != None

        password_field = soup.find('input', {'name':'confirm_password'})
        assert password_field != None

        #
        # POST the reset password page
        #
        data = {'new_password':     'abc123',
                'confirm_password': 'abc123_wrong',}
        response = c.post(url, data, follow=True)

        #
        # attemp log in again
        #
        response = c.get(reverse('logout'))
        data = {'email': my_email,
                'password': 'abc123', }
        response = c.post(reverse('login'), data, follow=True) #NOTE: if a follows=False, the next few lines will fail.

        # check is user logged in
        assert response.context['user'].id == None


    def test_forgotpassword_invalid_link(self):
        c = Client()
        url = response = reverse(self.URL_NAME,  kwargs={'code':'wrong'})
        response = c.post(url,  follow=False)
        assert "link is invalid" in response.content


class DjNodeChangePassowrdTest(TestCase):
    URL_NAME = "login"


    def test_change_password_post(self):
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
        response = c.post(reverse(self.URL_NAME), data, follow=True) #NOTE: if a follows=False, the next few lines will fail.

        # check is user logged in
        assert response.context['user'].id != None
        assert response.context['user'].id != ""
        assert response.context['user'].id == User.objects.filter(actual_email=my_email)[0].id

        # change passowrd
        url = reverse('change-password')
        data = {'current_password': 'password',
                'new_password': 'letmein',
                'confirm_new_password': 'letmein',}
        response = c.post(url, data, follow=True)

        # login
        response = c.get(reverse('logout'))
        data = {'email': 'test@domain.com',
                'password': 'letmein', }
        response = c.post(reverse(self.URL_NAME), data, follow=True) #NOTE: if a follows=False, the next few lines will fail.

        # check is user logged in
        assert response.context['user'].id != None
        assert response.context['user'].id != ""
        assert response.context['user'].id == User.objects.filter(actual_email=my_email)[0].id

    def test_change_password_current_password_incorrect(self):
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
        response = c.post(reverse(self.URL_NAME), data, follow=True) #NOTE: if a follows=False, the next few lines will fail.

        # check is user logged in
        assert response.context['user'].id != None
        assert response.context['user'].id != ""
        assert response.context['user'].id == User.objects.filter(actual_email=my_email)[0].id

        # change passowrd
        url = reverse('change-password')
        data = {'current_password': 'password-wrong',
                'new_password': 'letmein',
                'confirm_new_password': 'letmein',}
        response = c.post(url, data, follow=True)

        # login
        response = c.get(reverse('logout'))
        data = {'email': 'test@domain.com',
                'password': 'letmein', }
        response = c.post(reverse(self.URL_NAME), data, follow=True) #NOTE: if a follows=False, the next few lines will fail.

        # check is user logged in
        assert response.context['user'].id == None

    def test_change_password__missed_requirement(self):
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
        response = c.post(reverse(self.URL_NAME), data, follow=True) #NOTE: if a follows=False, the next few lines will fail.

        # check is user logged in
        assert response.context['user'].id != None
        assert response.context['user'].id != ""
        assert response.context['user'].id == User.objects.filter(actual_email=my_email)[0].id

        # change passowrd
        url = reverse('change-password')
        data = {'current_password': 'password',
                'new_password': '12',
                'confirm_new_password': '12',}
        response = c.post(url, data, follow=True)

        # login
        response = c.get(reverse('logout'))
        data = {'email': 'test@domain.com',
                'password': '12', }
        response = c.post(reverse(self.URL_NAME), data, follow=True) #NOTE: if a follows=False, the next few lines will fail.

        # check is user logged in
        assert response.context['user'].id == None

    def test_change_password_new_passowrd_missed_requirement(self):
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
        response = c.post(reverse(self.URL_NAME), data, follow=True) #NOTE: if a follows=False, the next few lines will fail.

        # check is user logged in
        assert response.context['user'].id != None
        assert response.context['user'].id != ""
        assert response.context['user'].id == User.objects.filter(actual_email=my_email)[0].id

        # change passowrd
        url = reverse('change-password')
        data = {'current_password': 'password',
                'new_password': 'letmein',
                'confirm_new_password': 'letmein2',}
        response = c.post(url, data, follow=True)

        # login
        response = c.get(reverse('logout'))
        data = {'email': 'test@domain.com',
                'password': 'letmein', }
        response = c.post(reverse(self.URL_NAME), data, follow=True) #NOTE: if a follows=False, the next few lines will fail.

        # check is user logged in
        assert response.context['user'].id == None

    def test_change_password_without_login(self):
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
        response = c.post(reverse(self.URL_NAME), data, follow=True) #NOTE: if a follows=False, the next few lines will fail.

        # check is user logged in
        assert response.context['user'].id != None
        assert response.context['user'].id != ""
        assert response.context['user'].id == User.objects.filter(actual_email=my_email)[0].id


        # change passowrd
        response = c.get(reverse('logout'))
        url = reverse('change-password')
        data = {'current_password': 'password',
                'new_password': 'letmein',
                'confirm_new_password': 'letmein'}
        response = c.post(url, data, follow=True)

        # login
        response = c.get(reverse('logout'))
        data = {'email': 'test@domain.com',
                'password': 'letmein', }
        response = c.post(reverse(self.URL_NAME), data, follow=True) #NOTE: if a follows=False, the next few lines will fail.

        # check is user logged in
        assert response.context['user'].id == None
