import datetime

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.conf import settings

from dj_node.models import Token
from dj_node.nodes.form import FormNode
from dj_node.nodes.node import NodeVariable
from dj_node.nodes.utils import Utils, EmailUtils
from dj_node.users.account import SignUpForm
from dj_node.users.profile import ProfileStepParent


class ForgotPasswordForm(forms.Form, NodeVariable):
    x_name = "Forgot Password"
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
         if kwargs.has_key('request'):
            self.request = kwargs['request']
            del kwargs['request']
         super (ForgotPasswordForm, self).__init__(*args,**kwargs)
         Utils.add_recaptcha_to_form(self.request, self)

    def clean_email(self):
        raw_email = self.cleaned_data.get('email', '')
        norm_email = SignUpForm.normalize_email(self.request, raw_email)
        if User.objects.filter(email=norm_email).count() <= 0:
            raise forms.ValidationError("Please enter valid email address..")   
        return raw_email
  
    def _process(self, request):
        # create the token
        raw_email = self.cleaned_data.get('email', '')
        t = Token( domain = Utils.get_mojo_domain(request),
                   email = raw_email,
                   token = Token.generate_token(),
                   type = 'reset_password',
                   used = False,
                   expire = datetime.datetime.now() + datetime.timedelta(days=3),)
        t.save()

        # create the email
        mojo_site = Utils.get_mojo_site(self.request)
        if mojo_site and mojo_site.get('management_email'):
            from_email = mojo_site.get('management_email')
        else:
            raise Exception("No account email set.")    # pragma: no cover
        domain = Utils.get_mojo_domain(request)
        link = "https://%s/password/reset/?code=%s" % (domain, t.token)
        subject = "Reset your password"
        msg_plain = "Click there link to reset your password: <a href=\"%s\">%s</a>" % (link, link)

        t.url = link
        t.save()

        # send email
        try:
            EmailUtils.send_email(from_email, raw_email, subject, msg_plain)
        except Exception, e:                                                 # pragma: no cover
           raise Exception(e)
           return {'return': 302,                                           # pragma: no cover
                   'msg':'Oop, we are having diffculty to send you email',
                   'redirect_url': reverse('login')}

        # return back
        return {'return': 302,
                'msg':' Please check your email to reset your password.',
                'redirect_url': reverse('login') }


class ForgotPasswordNode(FormNode):
    x_form = ForgotPasswordForm
    x_name = "Forgot Passwaord"
    x_template = "users/password/forgot_password.html"
    x_perm = []


class RestPasswordForm(forms.Form, NodeVariable):
    x_name = "Reset Password"
    new_password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)

    def __init__(self, *args, **kwargs):
         if kwargs.has_key('request'):
            self.request = kwargs['request']
            del kwargs['request']
         super (RestPasswordForm, self).__init__(*args,**kwargs)

    def clean_new_password(self):
        password = self.cleaned_data.get('new_password', '')
        if len(password) < 6:
            raise forms.ValidationError("At least 6 characters long") 
        return password
    
    def clean(self):
        if self.cleaned_data.get('new_password', '') != self.cleaned_data.get('confirm_password', ''):
            raise forms.ValidationError("New passwords do not math")            
        return self.cleaned_data  
            
    def _process(self, request):
        t = Token.objects.get(token=self.request.kwargs.get('code'))
        norm_email = SignUpForm.normalize_email(request, t.email)
        user = User.objects.get(email=norm_email)
        
        password = self.cleaned_data.get('new_password', '')
        user.set_password(password)
        user.save()
        
        t.delete()
        
        # return back
        node_dict = {'return':302,
                'msg':'Your password have been updated, please log in now.',
                'redirect_url':'http://{}{}'.format(settings.DOMAIN, reverse('login')) }
        return node_dict


class ResetPasswordNode(FormNode):
    x_form = RestPasswordForm
    x_name = "Rest Passwaord"
    x_template = "users/password/reset_password.html"
    x_perm = []

    def _check(self, request):
        code = request.GET.get('code')
        count = Token.objects.filter(token=code).count()
        if not count:
            return False, {'return':400,
                           'msg':'Sorry, link is invalid.'}
        return True, None


class ChangePasswordForm(forms.Form, NodeVariable):
    current_password = forms.CharField(widget=forms.PasswordInput, required=True)
    new_password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_new_password = forms.CharField(widget=forms.PasswordInput, required=True)

    def __init__(self, *args, **kwargs):
         if kwargs.has_key('request'):
            self.request = kwargs['request']
            del kwargs['request']
         super (ChangePasswordForm, self).__init__(*args,**kwargs)

    def clean_current_password(self):
        password = self.cleaned_data.get('current_password', '')
        if not  authenticate(username=self.request.user.username, password=password):
            raise forms.ValidationError("Current password is incorrect.")
        return password

    def clean_new_password(self):
        password = self.cleaned_data.get('new_password', '')
        if len(password) <= 6:
            raise forms.ValidationError("At least 6 characters long")
        return password

    def clean(self):
        if self.cleaned_data.get('new_password', '') != self.cleaned_data.get('confirm_new_password', ''):
            raise forms.ValidationError("New passwords do not math")
        return self.cleaned_data

    def _process(self, request):
        user = self.request.user
        password = self.cleaned_data.get('new_password', '')
        user.set_password(password)
        user.save()

        Utils.set_msg(self.request, "You password has been updated. Please login now. ")
        return {'return':302,
                'redirect_url':'http://{}{}'.format(settings.DOMAIN, reverse('login')) }

class ChangePasswordNode(FormNode):
    x_form = ChangePasswordForm
    x_name = "Change Password"
    x_template = "users/password/sp_change_password.html"
    x_step_parent_template = "profile_step_parent.html"
    x_perm = ['login']
    x_step_parent = ProfileStepParent
    x_tab = "change-password"
    