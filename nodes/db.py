from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType

class Db(object):
    @staticmethod
    def get_content_type_for_model(model):
        return ContentType.objects.get_for_model(model)

    @staticmethod
    def get_distinct_values(model, field_name):
        return model.objects.values_list(field_name, flat=True).distinct().order_by(field_name)

    @staticmethod
    def get_item(model, id):
        return model.objects.get(id=id)

    @staticmethod
    def get_list_easy(model, filters={}, order_by=None):
        """
        Return a list of Django model instances

        Parameters
        ----------
        model : model class
        filters: dict, {'field1':'val1', 'field2':'val2}
        order_by: field (str) name
        """

        from dj_node.nodes.list_info import ListInfo
        from dj_node.nodes.list_filter import ListFilter

        # reformat filters
        new_filters = {}
        for k in filters.keys():
            new_filters[k] = {'name': k, 'val': filters[k], 'op': '='}

        # setup to call get_list()
        list_info = ListInfo(model)
        list_info.sort = order_by

        list_filter = ListFilter(model)
        list_filter.db_filters = new_filters

        # get the list
        list_info = Db.get_list(list_info, list_filter)
        results = list_info.results
        return results


    @staticmethod
    def get_list(request, list_info, list_filter):
        """
        Return modified list_info

        Parameters
        ----------
        request : Django request object
        list_info : ListInfo instance
        list_filters: ListFilter instance
        """

        # filter str
        filter_str ="list_info.model.objects.all()"
        for r in list_filter.db_filters.keys():
            d = list_filter.db_filters[r]
            field = d.get('name', None)
            value = d.get('val', None)
            op = d.get('op', "=")
            filter_str = filter_str + ".filter(%s%s'%s')" % (str(field), str(op), str(value))

        # sort str
        if list_info.sort: 
            filter_str = filter_str + ".order_by('%s')" %  list_info.sort            
        
        # 1st run to get all results
        instant_list = None
        query_str = "instant_list = %s " % filter_str
        exec(query_str)

        # 2nd run to get result count
        total = 0
        exec("total = %s.count()" % filter_str)
        list_info.total = total

        # paging
        if list_info.ipp > 0:
            list_paginator = Paginator(instant_list, list_info.ipp)
            paginator_page = list_paginator.page(list_info.page)
            list_info.start = 1 + list_info.ipp * (list_info.page - 1)
            list_info.end =  list_info.start + len(paginator_page.object_list) - 1
            list_info.page_count = list_paginator.num_pages
            list_info.results = paginator_page.object_list
            list_info.result_count = len(paginator_page.object_list)
        else:
            list_info.results = instant_list
            list_info.result_count = total
        return list_info

    @staticmethod
    def save_item(instance):
        return instance.save()
