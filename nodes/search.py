from dj_node.nodes.list import ListNode
from dj_node.nodes.list_info import ListInfo
from dj_node.nodes.list_filter import ListFilter
try:
    from dj_geo.models import Zipcode
except ImportError:
    pass
try:
    from elasticsearch import Elasticsearch, RequestsHttpConnection
except ImportError:
    pass

class SearchNode(ListNode):
    """SearhNode, to be used with other thrid party software
    """
    x_list_info_cls = ListInfo
    x_list_filter_cls = ListFilter

    def _process(self, request):
        raise Exception("Subclass need to implement this function ")

class ESGeoNode(SearchNode):
    """ ElasticSearch Node (Install as below, https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-elasticsearch-on-ubuntu-14-04)
        >> sudo add-apt-repository -y ppa:webupd8team/java
           sudo apt-get update
           sudo apt-get -y install oracle-java8-installer
           wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-5.1.2.deb,
           sudo dpkg -i elasticsearch-5.1.2.deb sudo
           apt-get install apt-transport-https
        >> Need to change the vm's memory as follow: (edited)
            vb.memory = "4000"
        >> sudo -i service elasticsearch start
        >> lynx -dump http://localhost:9200
        {
          "name" : "gC5BQeP",
          "cluster_name" : "elasticsearch",
          "cluster_uuid" : "81tjKavHRsG-j3Y2b5UaFg",
          "version" : {
            "number" : "5.1.1",
            "build_hash" : "5395e21",
            "build_date" : "2016-12-06T12:36:15.409Z",
            "build_snapshot" : false,
            "lucene_version" : "6.3.0"
          },
          "tagline" : "You Know, for Search"
        }
    """

    # --- variables ---
    x_list_info_cls = ListInfo
    x_list_filter_cls = ListFilter
    x_col = "<col>"

    ES_INDEX = 'geo_data'
    ES_SERVER = '127.0.0.1'
    ES_PORT = 9200
    es = Elasticsearch( hosts=[{'host': ES_SERVER, 'port': ES_PORT}],
                        connection_class=RequestsHttpConnection )


    # --- methods ---
    def _process(self, request):
        """ Process a Sphinx search request
        :param request - Django request object
        :return: dict
        """
        if not self.es:
            raise Exception("No ES Server setup properly. ")

        # list info & list filter
        list_info = self.x_list_info_cls(self, request)
        list_filter = self.x_list_filter_cls(self, request)
        list_filter.radius_a = 0
        list_filter.radius_b = 200

        query = {}
        if request.GET.get('zip'):
            zip = Zipcode.objects.get(id=request.GET.get('zip'))
            list_filter.lat = zip.lat
            list_filter.lng = zip.lng
            list_filter.radius_b = request.GET('radius', 200)
            query = {
                "query": {
                    "bool" : {
                        "must" : {
                            "match_all" : {}
                        },
                        "filter" : {
                            "geo_distance" : {
                                "distance" : str(request.GET('radius', 200)) + "mi",
                                "geo.location" : {
                                    "lat" : zip.lat,
                                    "lon" : zip.lng
                                }
                            }
                        }
                    }
                }
            }
        res = self.es.search(index='geodata', body=query)
        raise Exception(res)

# class SphinxGeoNode(SearchNode):
#     """Sphinx Search Node
#     """
#
#     x_list_info_cls = ListInfo
#     x_list_filter_cls = ListFilter
#     x_col = "<col>"
#
#     SPHINX_INDEX = ''
#     SPHINX_SERVER = ''
#     SPHINX_PORT = ''
#     SPHINX_API_VERSION = ''
#
#     def get_sphinx_filters(self, request):
#         """ get the sphinx filters, to be used in the sphinx search query
#         :param request - Django request object
#         :return: dict
#         """
#         raise Exception("Subclass need to implement this method ")
#
#     def _process(self, request):
#         """ Process a Sphinx search request
#         :param request - Django request object
#         :return: dict
#         """
#
#         # list info & list filter
#         list_info = self.x_list_info_cls(self, request)
#         list_filter = self.x_list_filter_cls(self, request)
#         list_filter.radius_a = 0
#         list_filter.radius_b = 200
#         if request.GET.get('zip'):
#             zip = Zipcode.objects.get(id=request.GET.get('zip'))
#             list_filter.lat = zip.lat
#             list_filter.lng = zip.lng
#             list_filter.radius_b = request.GET('radius', 200)
#
#         # sphinx search obj
#         search = sphinxapi.SphinxClient()
#         search.SetServer(self.SPHINX_SERVER, self.SPHINX_PORT )
#
#         # form query and set serach certieria
#         query = ""
#         f = self.get_sphinx_filters(request)
#         if f and len(f.keys()) > 0:
#              query  = "".join([" @%s (%s) " % (k, f[k])  for k in f.keys()])
#              search.SetMatchMode(sphinxapi.SPH_MATCH_EXTENDED)
#         if list_filter.lat and list_filter.lng:
#              search.SetGeoAnchor('latitude','longitude',float(math.radians(list_filter.lat)), float(math.radians(list_filter.lng)))
#              if list_info.radius_b:
#                  search.SetFilterFloatRange('@geodist', 0.00, 1.61*1000*float(list_filter.radius_b));
#                  search.SetSortMode(sphinxapi.SPH_SORT_EXTENDED, "@geodist asc")
#
#         # attemp search
#         search.SetLimits(0, 1)
#         sphinx_result = search.Query(query, self.SPHINX_INDEX)
#         list_info.total = sphinx_result['total']
#
#         # actual search
#         offset = list_info.ipp * (list_info.page - 1)
#         search.SetLimits(offset, list_info.ipp)
#         sphinx_result = search.Query(query, self.SPHINX_INDEX)
#
#         # get instances
#         id_list = [ m['id'] for m in sphinx_result['matches']]
#         list_info.results = [self.x_model.objects.get(pk=id) for id in id_list]
#
#         # update pagination information
#         list_info.total_page = int(math.ceil(list_info.total/list_info.ipp))
#         list_info.pages = [n for n in range(list_info.page - 8, list_info.page + 8) if n > 0 and n <= list_info.total_page ]
#         result = {'list_info':list_info, 'list_filter':list_filter}
#
#         search.Close()
#         return result
