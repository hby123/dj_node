from django.template import RequestContext
from dj_node.nodes.db import Db
from dj_node.nodes.node import NodeTemplate, Node, perm_check
from dj_node.nodes.utils import Utils


class FormNode(Node):
    x_template = "form/form.html"
    x_template_html = "form/z_form.html"
    x_process_get = False
    x_submit = "Submit"

    @perm_check('')
    def _run(self, request):
        # permission check method
        check_flag, check_dict = self._check(request)
        if not check_flag: 
            return self._render(request, check_dict)    # pragma: no cover

        # form processing
        flag_processed = 0
        node_dict = {'form_cls':self}
        if request.method == 'POST' or self.x_process_get:
            node_dict['form'] = self._create(request=request)
            if node_dict['form'].is_valid():
                result = node_dict['form']._process(request)
                node_dict = dict(result.items() + node_dict.items())
                flag_processed = 1
        elif request.method == 'GET':
            node_dict['form'] = self._create(request)

        # render
        if not node_dict.has_key('return'):
            node_dict['return'] = 200
        node_dict['flag_processed'] = flag_processed
        return self._render(request, node_dict)

    def _render_string(self, request, node_dict={}):
        node_dict['node'] = self
        node_dict['form'] = self._create(request=request)
        node_dict = self.templates_to_node_dict(request, node_dict)
        template_html = NodeTemplate.fallback_template(request, self.x_template_html)
        return Utils.render_to_string(template_html, node_dict, context_instance=RequestContext(request))


    def _create(self, request):
        if request.method == 'GET':
            if self.x_process_get:
                form = self.x_form(request.GET, request=request)
            else:
                GET_data = self._GET_data(request)
                if GET_data:
                    form = self.x_form(initial=GET_data, request=request)
                else:
                    form = self.x_form(request=request)
        elif request.method == 'POST':
            form = self.x_form(request.POST, request.FILES, request=request)
        return form

    def _GET_data(self, request):
        return False


class ModelFormNode(FormNode):
    x_form = None
    x_model = None

    @classmethod
    def _create(self, request):
        # get the instance
        id = request.GET.get('id')
        instance = Db.get_item(self.x_model, id)

        # instantiate form
        if request.method == 'GET':
            form = self.x_form(instance=instance, request=request)
        elif request.method == 'POST':
            form = self.x_form(request.POST, request.FILES, instance=instance, request=request)
        return form

    def _GET_data(self, request):
        return False
