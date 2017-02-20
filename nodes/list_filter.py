class ListFilterBasic(object):
    """
    ListFilter has 3 parts.
        HTML (Option List)
        HTML (Selected)
        URL
    """

    def __init__(self, model, request, *args, **kwargs):
        """ Constructor
        :param ref_cls - The list node class
        :param request - Django request object
        :return: None
        """

        self.option_filters = []
        self.selected_filters = []
        self.db_filters = {}
        self.url_query = ""

class ListFilter(object):
    """
    ListFilter has 3 parts.
        HTML (Option List)
        HTML (Selected)
        URL
    """

    def __init__(self, ref_cls, request, *args, **kwargs):
        """ Constructor
        :param ref_cls - The list node class
        :param request - Django request object
        :return: None
        """

        self.ref_cls = ref_cls
        self.skip_keys=ref_cls.x_skip_keys
        self.option_filters = self._build_option_filters(request)
        self.selected_filters = self._build_selected_filters(request)
        self.db_filters = self.selected_filters
        self.url_query = self._build_url_query(request)

    def _build_option_filters(self, request):
        """ Build filter option list
        :param request - Django request object
        :return: None
        """

        option_filters = []
        for row in self.ref_cls.x_option_filters:
            option = {  'label':row['label'],
                        'name':row['name']}
            if not (row.has_key('option_list') and row['option_list']):
                option['option_list'] = self.ref_cls.x_model.objects.values_list(row['name'], flat=True).distinct()
            option_filters.append(option)
        return option_filters


    def _build_selected_filters(self, request):
        """ Build selected filter list, this depends self.x_option_filters, so this object need to call
        build_option_filters() first before calling this function.
        :param request - Django request object
        :param skip_keys - filter names to skip
        :return: None
        """

        def get_label(obj, k):
            for filter_row in obj.ref_cls.x_option_filters:
                  if k == filter_row['name']:
                      return filter_row['label']

        # get filters
        filters = {}
        for k in request.GET.keys():
            if k.lower() not in self.skip_keys:
                if "oo_" not in k and "dd_" not in k:
                    filters[k] = {'label':get_label(self, k),
                                  'name': k,
                                  'val': request.GET.get(k)}

        # override
        for k in request.GET.keys():
            if ("oo_" in k):
                k2 = k.replace("oo_", "")
                if k2 not in self.skip_keys:
                    filters[k2] = {'label':get_label(self, k2),
                                   'name': k2,
                                   'val': request.GET.get(k)}
        # delete
        for k in request.GET.keys():
            if "dd_" in k:
                k2 = k.replace("dd_", "")
                if k2 in filters.keys():
                    del filters[k2]
        return filters


    def _build_url_query(self, request):
        """ Build url part,  to be used in temp;late.
        :param request - Django request object
        :return: None
        """

        query = ""
        skip_keys=['page']
        selected_filters = self._build_selected_filters(request)
        for k in selected_filters.keys():
            v =  selected_filters[k]
            if v['name'] not in skip_keys:
                if query:
                    query = query + "&%s=%s" % (v['name'], v['val'])
                else:
                    query = "%s=%s" % (v['name'], v['val'])
        return query


