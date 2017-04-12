import json
from django.core.urlresolvers import NoReverseMatch
from django.http import HttpResponsePermanentRedirect
from django.http import HttpResponse
from django.shortcuts import redirect, render_to_response
from django.template import Context, RequestContext, loader, TemplateDoesNotExist
from dj_node.nodes.utils import Utils
try:
    # Python 2.x
    from urlparse import urlsplit, urlunsplit
except ImportError:
    # Python 3.x
    from urllib.parse import urlsplit
    from urllib.parse import urlunsplit


def perm_check(dummy):     # pragma: no cover
    """ Permission decorator to to used on node's rounte() method
    """
    def wrap_outer(func):
        def wrap_inner(*args, **kargs):
            # get the argument frrom the func (method route(cls, request)
            kclass = args[0]
            request = args[1]

            # count number of permisson passed
            passed_count = 0
            flag_pass = False
            flag_login_required = False
            for perm in kclass.x_perm:
                if perm == 'login':
                        flag_login_required = True
                if Utils.has_perm(request, perm):
                    passed_count = passed_count + 1

            # determine pass or not
            if len(kclass.x_perm) == passed_count:
                flag_pass = True

            # handle failed permission
            if flag_pass == False:
                if flag_login_required:
                        result = {'return':'302',
                                  'msg':'Please login to continue',
                                  'redirect_url':'/login/' }
                        return kclass()._render(request, result)
                else:
                        result = {'return':'302',
                                   'msg':'Sorry, you do not have permission to continue',
                                   'redirect_url':'/'}
                        return kclass()._render(request, result)
            # handle passed permission
            return func(*args, **kargs)
        return wrap_inner
    return wrap_outer


def ssl_check(dummy):     # pragma: no cover
    """ Permission decorator to to used on node's rounte() method
    """
    def wrap_outer(func):
        def wrap_inner(*args, **kwargs):
            # get the argument frrom the func (method route(cls, request)
            kclass = args[0]
            request = args[1]
            if kwargs.get('ssl'):
                if not request.is_secure():
                    url = request.build_absolute_uri(request.get_full_path())
                    url_split = urlsplit(url)
                    scheme = 'https' if url_split.scheme == 'http' else url_split.scheme
                    ssl_port = 443
                    url_secure_split = (scheme, "%s:%d" % (url_split.hostname or '', ssl_port)) + url_split[2:]
                    secure_url = urlunsplit(url_secure_split)
                    return HttpResponsePermanentRedirect(secure_url)
            elif (not kwargs.get('ssl')) and request.is_secure():
                    url = request.build_absolute_uri(request.get_full_path())
                    url_split = urlsplit(url)
                    scheme = 'http'
                    port = 8002
                    url_secure_split = (scheme, "%s:%d" % (url_split.hostname or '', port)) + url_split[2:]
                    secure_url = urlunsplit(url_secure_split)
                    return HttpResponsePermanentRedirect(secure_url)
            return func(*args, **kwargs)
        return wrap_inner
    return wrap_outer


class NodeVariable(object):
    """ Basic variables
    """
    x_name = None
    x_model = None
    x_perm = []
    x_step_parent = None

class NodeTemplate(object):
    """ Template handler
    """
    x_tab = None
    x_base_template = "base.html"
    x_parent_template = "mojo.html"
    x_step_parent_template = "step_parent.html"
    x_template = "mojo.html"
    x_error_template = "error.html"
    x_empty_template = "empty.html"

    x_pre_html = ""
    x_post_html = ""

    def _get_pre_html(self, request):
        return ""

    def _get_post_html(self, request):
        return ""

    @staticmethod
    def fallback_template(request, filename):
        mojo_site = Utils.get_mojo_site(request)
        if filename:
            try:
                path = mojo_site['folder'] + "/themes/" + mojo_site['site_theme'] + "/" + filename
                loader.get_template(path)
                return path
            except (TemplateDoesNotExist, AttributeError), e:
                pass

            try:
                path = "dj_node/" + "themes/" + mojo_site['dj_node_theme'] + "/" + filename
                print "\n\n path: %s " % path

                loader.get_template(path)
                return path
            except (TemplateDoesNotExist, AttributeError), e:
                pass

            try:
                path = filename
                loader.get_template(path)
                return path
            except (TemplateDoesNotExist, AttributeError), e:
                raise TemplateDoesNotExist("dj_node - failed to find template {}".format(filename))

    def templates_to_node_dict(self, request, node_dict):
        """ The entry point of node, to be used from urls.py
        :param request - Django request object
        :param node_dict -the dict to be return back to the template
        :return: modified node_dict
        """
        node_dict['x_tab'] = self.x_tab
        node_dict['x_base_template'] = self._get_base_template(request)     # (optional) parent for current templat
        node_dict['x_parent_template'] = self._get_parent_template(request) # highest parent
        node_dict['x_step_parent_template'] = self._get_step_parent_template(request) # highest parent
        node_dict['x_template'] = self._get_template(request)               # the actual template
        node_dict['x_error_template'] = self._get_error_template(request)   # (optional) parent for current template
        node_dict['x_empty_template'] = self._get_empty_template(request)
        node_dict['x_pre_html'] = self._get_pre_html(request)
        node_dict['x_post_html'] = self._get_post_html(request)
        return node_dict

    def _get_template(self, request):
        return self.fallback_template(request, self.x_template)

    def _get_parent_template(self, request):
        return self.fallback_template(request, self.x_parent_template)

    def _get_step_parent_template(self, request):
        return self.fallback_template(request, self.x_step_parent_template)

    def _get_base_template(self, request):
        return self.fallback_template(request, self.x_base_template)

    def _get_error_template(self, request):
        return self.fallback_template(request, self.x_error_template)

    def _get_empty_template(self, request):
        return self.fallback_template(request, self.x_empty_template)

class Node(NodeVariable, NodeTemplate):

    @classmethod
    @perm_check("dummy")
    @ssl_check("dummy")
    def route(cls, request, *args, **kwargs):
        """ The entry point of node, to be used from urls.py
        :param request - Django request object
        :return: _run()
        """
        request.kwargs = kwargs
        return cls()._run(request)

    def _run(self, request):
        """ Run a node, 1) check permission, 2) process node 3) _render
        :param request - Django request object
        :return: _render()
        """

        # 1: call check method
        check_flag, check_dict = self._check(request)
        if not check_flag: 
            return self._render(request, check_dict)    # pragma: no cover
        else: 
            # 2: call process
            node_dict  = self._process(request)

            # 3: call render
            return self._render(request, node_dict)

    def _check(self, request):
        """ Extra function to check for permission.
        :param request - Django request object
        :return: bool, dict
        """
        return True, {}

    def _process(self, request):
        """ Process the node
        :param request - Django request object
        :return: dict, should have key "return", and optionally "msg", and "redirect"
        """
        return {'return':200,
                'msg':None,
                'redirect':None }

    def _extra(self, request, node_dict):
        """ Add extra key-val pair to the node_dict, call from _render() method
        :param request - Django request object
        :return: dict
        """
        return {}

    def _render(self, request, node_dict):
        """ Primary render method
        :param request - Django request object
        :param node_dict - dict to be passed to template
        :return: dict
        """

        # add template
        node_dict['node'] = self
        node_dict = self.templates_to_node_dict(request, node_dict)

        # add extras
        self.node_dict = node_dict
        extra = self._extra(request, node_dict)
        node_dict.update(extra)

        # add step parent extra
        if self.x_step_parent:
            step_parent_extra = self.x_step_parent()._extra(request, node_dict)
            node_dict.update(step_parent_extra)
        
        # ajax or http
        if request.is_ajax() or request.GET.get('ajax') == 'true':
            return self._render_ajax(request, node_dict)
        else: 
            return self._render_http(request, node_dict)

    def _render_string(self, request, node_dict={}):
        """ Sub render method for inline-html
        :param request - Django request object
        :param node_dict - dict to be passed to template
        :return: dict
        """
        return Utils.render_to_string(node_dict['x_template'], node_dict, context_instance=RequestContext(request))

    def _render_http(self, request, node_dict, flag_html=False):
        """ Sub render method for normal HTTP
        :param request - Django request object
        :param node_dict - dict to be passed to template
        :return: dict
        """

        code = int(node_dict.get('return'))
        msg = node_dict.get('msg')
        redirect_url = node_dict.get('redirect_url')

        # check for error in implementation
        if int(code) == 302 and not redirect_url:
            raise Exception("Redirect URL is not found. ")     # pragma: no cover
        elif int(code) >= 400 and not msg:
            raise Exception("No error detail. ")       # pragma: no cover

        # msg
        if msg:
            Utils.set_msg(request, msg)

        # redirect
        if redirect_url:
            try:
                return redirect(redirect_url)
            except NoReverseMatch:
                return redirect("/")

        # error
        if code >= 400:
            return render_to_response(node_dict['x_error_template'], node_dict, context_instance=RequestContext(request))

        # render
        if flag_html:
            t = loader.get_template(node_dict['x_template'])
            c = Context(node_dict)
            html = t.render(c)
            return html
        return render_to_response(node_dict['x_template'], node_dict, context_instance=RequestContext(request))

    def _render_ajax(self, request, node_dict):
        """ Sub render method for ajax
        :param request - Django request object
        :param node_dict - dict to be passed to template
        :return: dict
        """

        json_dict = {}
        if node_dict['x_template']:
            template_loader = loader.get_template(node_dict['x_template'])
            context_instance = RequestContext(request)
            context_instance.update(Context(node_dict))
            html = template_loader.render(context_instance)
            html = html.strip()
            json_dict['html'] = html

        # jsonize items
        for k in node_dict.keys():
            v = node_dict[k]
            try:
                json.dumps({k:v}) # attemp to dump json format
                json_dict[k] = v
            except:
                if hasattr(node_dict[k], 'jsonize'):
                    json_dict[k] = node_dict[k].jsonize()

        return HttpResponse(json.dumps(json_dict), content_type="application/json")

