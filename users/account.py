import time, datetime, random, string
from django import forms
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login as auth_login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.template import Context, RequestContext, loader, TemplateDoesNotExist
from django.template.defaultfilters import slugify
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from dj_node.nodes.node import NodeVariable, Node
from dj_node.nodes.form import FormNode
from dj_node.nodes.item import ItemNode
from dj_node.nodes.utils import Utils
from dj_node.models import Token


class SignUpForm(forms.Form, NodeVariable):
    email = forms.EmailField(required=True, help_text="We never share your email address with anyone!")
    display_name = forms.CharField(required=True, help_text="This will be your public username on the site.")
    password = forms.CharField(widget=forms.PasswordInput, required=True, help_text="Please enter a password that's at least 6 characters long.")
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True, help_text="Please type your password again.")

    def __init__(self, *args, **kwargs):
         if kwargs.has_key('request'):
            self.request = kwargs['request']
            del kwargs['request']
         super (SignUpForm, self).__init__(*args,**kwargs)

         #add recaptcha
         Utils.add_recaptcha_to_form(self.request, self)

    @staticmethod
    def normalize_email(request, email):
        norm_email = None
        mojo_domain = Utils.get_mojo_domain(request)
        if email: 
            norm_email = mojo_domain + "-" + email
        return norm_email

    def clean_email(self):
        raw_email = self.cleaned_data.get('email', '')
        email = SignUpForm.normalize_email(self.request, raw_email)
        if User.objects.filter(username__iexact=email).count() > 0:
            raise forms.ValidationError("Sorry, email already exists.")   
        return raw_email
  
    def clean_display_name(self):
        display_name = self.cleaned_data.get('display_name', '')
        if len(display_name) < 3: 
            raise forms.ValidationError("Your display name need at least 3 characters long.") 
        if User.objects.filter(display_name__iexact=display_name).count() > 0:
            raise forms.ValidationError("Sorry, display name already exists. ") 
        return display_name
         
    def clean_password(self):
        password = self.cleaned_data.get('password', '')
        if len(password) < 5: 
            raise forms.ValidationError("Password need at least 6 characters long.") 
        return password
    
    def clean(self):
        if self.cleaned_data.get('password', '') != self.cleaned_data.get('confirm_password', ''):
            raise forms.ValidationError("Passwords do not match.")            
        return self.cleaned_data

    def _process(self, request):
        # Create user account                
        raw_email = self.cleaned_data.get("email", None) 
        display_name = self.cleaned_data.get("display_name", None)
        password = self.cleaned_data.get("password", None)
        
        user_email = SignUpForm.normalize_email(self.request, raw_email)
        new_user = User.objects.create_user(user_email, user_email, password=password)
        new_user.is_active = True
        new_user.actual_email = raw_email
        new_user.display_name = display_name
        new_user.display_name_slug = slugify(display_name)
        new_user.save()
        
        user = authenticate(username=user_email, password=password)
        if user is not None: 
            auth_login(self.request, user)   
            Utils.set_msg(self.request, "Thank you, your account has been created. ")
        return {'return':'302',
                'redirect_url':reverse('login') }


class SignUpNode(FormNode):
    x_form = SignUpForm
    x_name = "Sign Up"
    x_template = "users/account/sign_up.html"

    def _check(self, request):
        flag = True
        result = {}

        # if user already log in
        if request.user.is_authenticated():
            flag = False
            result = {'return':'302',
                      'redirect_url':'/' }
        return flag, result

    def _get_post_html(self, request):
        return "<a href=\"%s\">Have an account already? login here</a>" % reverse('login')

class LoginForm(forms.Form, NodeVariable):
    email = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def __init__(self, *args, **kwargs):
         if kwargs.has_key('request'):
            self.request = kwargs['request']
            del kwargs['request']
         super(LoginForm, self).__init__(*args,**kwargs)

    def clean(self):
        raw_email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        email = SignUpForm.normalize_email(self.request, raw_email)

        ulist = User.objects.filter(username=email)
        if len(ulist) > 0:
            self.user_cache = authenticate(username=email, password=password)
            if not self.user_cache:
                raise forms.ValidationError("Sorry, wrong password.")
            if self.user_cache and not self.user_cache.is_active:
                raise forms.ValidationError("Sorry, account is locked.")
        else:
            raise forms.ValidationError("Oops, email and password do not match.")
        return self.cleaned_data

    def _process(self, request):
        auth_login(self.request, self.user_cache)
        return {'return':302,
                'redirect_url':reverse('index') }


class LoginNode(FormNode):
    x_form = LoginForm
    x_name = "Login"
    x_template = "users/account/login.html"

    def _check(self, request):
        flag = True
        result = {}

        # if user already login
        if request.user.is_authenticated():
            flag = False
            result = {'return':302,
                      'redirect_url':reverse('index') }
        return flag, result

    def _get_post_html(self, request):
        return "<a href=\"%s\">Sign up for a free account here.</a> <a href=\"%s\">Or forgot password</a>?" % \
               (reverse('sign-up'), reverse('forgot-password'))


class Logout(ItemNode):

    @classmethod
    def _run(cls, request):
        logout(request)
        return {'return':302,
                'redirect_url':reverse('login') }
