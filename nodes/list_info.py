import math


class ListInfoBasic(object):
    def __init__(self, model, request,  *args, **kwargs):
        """ Constructor
        :param ref_cls - list node class
        :return: None
        """

        # base info
        self.model = model

        self.query =  request.GET.get('query')  # the search query
        self.url = ""                           # the url from the browser

        # pagination
        self.page = int(request.GET.get('page', 1)) # current page
        self.ipp = 20                               # items per page
        self.start = 0                              # the starting number for the resulst list
        self.end = 0                                # the ending number, see above.
        self.total = 0                              # total number of items

        self.page_count = 1
        self.page_head_off = False
        self.page_tail_off = False

        # geo
        self.lat = None             # search lat
        self.lng = None             # search lng
        self.radius_a = 0           # radius search starting point
        self.radius_b = request.GET.get('radius', 99999)    # radius search ending point. Earth Radius: 3,959 miles (6,371 km)

        # sort
        self.sort = None
        if not self.sort:
            self.sort = request.GET.get('oo_sort', None)
            if not self.sort:
                self.sort = request.GET.get('sort', None)

        # result
        self.results = []
        self.result_count = 0


class ListInfo(object):

    def __init__(self, ref_cls, request, *args, **kwargs):
        """ Constructor
        :param ref_cls - list node class
        :return: None
        """

        self.ref_cls = ref_cls

        # base info
        self.model = self.ref_cls.x_model       # model to be searched on
        self.query =  request.GET.get('query')  # the search query
        self.url = ""                           # the url from the browser

        # pagination
        self.page = int(request.GET.get('page', 1)) # current page
        self.ipp = 20                               # items per page
        self.start = 0                              # the starting number for the resulst list
        self.end = 0                                # the ending number, see above.
        self.total = 0                              # total number of items

        self.page_count = 1
        self.page_head_off = False
        self.page_tail_off = False

        # geo
        self.lat = None             # search lat
        self.lng = None             # search lng
        self.radius_a = 0           # radius search starting point
        self.radius_b = int(request.GET.get('radius', 200))    # radius search ending point. Earth Radius: 3,959 miles (6,371 km)

        # sort
        self.sort = None
        if not self.sort:
            self.sort = request.GET.get('oo_sort', None)
            if not self.sort:
                self.sort = request.GET.get('sort', None)
        if not self.sort:
            self.sort = self.ref_cls.x_sort_list[0]

        # result
        self.results = []
        self.result_count = 0

    def jsonize(self):
        """ jasonlized object, to be used from the node ajax render method.
        :return: json dict
        """
        return {
            'page': self.page,
            'ipp': self.ipp,
            'start': self.start,
            'end': self.end,
            'total': self.total,
            'page_count': self.page_count,
        }

    def get_pagination(self):
        """ Build the pagination list
        :param ref_cls - list node class
        :return: None
        """

        # get number of pages
        self.page_count = int(math.ceil((self.total*1.0)/(self.ipp*1.0)))

        # go to the left, update to 9 times
        page_list = []
        page_list = [x for x in range(max(1, self.page-9), self.page + 1)]

        # go to the right, update to 9 times
        extra_offset = 20 - len(page_list)
        page_list = page_list + [x for x in range(self.page + 1,
                                 min(self.page+extra_offset, self.page_count+1))]

        # head and tail 
        if 1 not in page_list:
            self.page_head_off = True

        if self.page_count not in page_list:
            self.page_tail_off = True

        return page_list
