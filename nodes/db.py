from django.core.paginator import Paginator
from dj_node.nodes.utils import Utils


class Db(object):

    @staticmethod
    def save_item(request, instance):
        """
        Return a Django model instance from the database

        Parameters
        ----------
        request : Django request object
        instance : a Djago model instance that's not yet save.
        """

        return instance.save()

    @staticmethod
    def get_item(request, model, id):
        """
        Return a Django model instance from the database

        Parameters
        ----------
        request : Django request object
        model : model class
        id : int
        """

        return model.objects.get(id=id)

    @staticmethod
    def get_list_simple(request, model, filters={}):
        """
        Return a list of Django model instances

        Parameters
        ----------
        request : Django request object
        model : model class
        filters: dict, {'field1':'val1', 'field2':'val2}
        """
        from dj_node.nodes.list_info import ListInfoBasic
        from dj_node.nodes.list_filter import ListFilterBasic

        # reformat filters
        new_filters = {}
        for k in filters.keys():
            new_filters[k] = {'name': k, 'val': filters[k], 'op': '='}

        # setup to call get_list()
        list_info = ListInfoBasic(model, request)
        list_info.model = model 
        list_info.filters = filters
        list_info.ipp = -1

        list_filter = ListFilterBasic(model, request)
        list_filter.db_filters = new_filters

        # get the list
        list_info = Db.get_list(request, list_info, list_filter)
        results =  list_info.results

        #raise Exception(results)
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
        
        # run 
        instant_list = None
        query_str = "instant_list = %s " % filter_str
        exec(query_str)

        if list_info.ipp > 0:   # paging
            list_paginator = Paginator(instant_list, list_info.ipp)
            paginator_page = list_paginator.page(list_info.page)
            list_info.start = 1 + list_info.ipp * (list_info.page - 1)
            list_info.end =  list_info.start + len(paginator_page.object_list) - 1
            list_info.page_count = list_paginator.num_pages

            # total
            total = 0
            exec("total = %s.count()" % filter_str)
            list_info.total = total

            # result
            list_info.results = paginator_page.object_list
            list_info.result_count = len(paginator_page.object_list)
        else: # no paging
            #total
            total = 0
            exec("total = %s.count()" % filter_str)
            list_info.total = total

            #result
            list_info.results = instant_list
            list_info.result_count = total

        # return result
        return list_info
