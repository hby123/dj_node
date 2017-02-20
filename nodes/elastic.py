"""
ElasticSearch Node (Install as below, https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-elasticsearch-on-ubuntu-14-04)
>> sudo add-apt-repository -y ppa:webupd8team/java
   sudo apt-get update
   sudo apt-get -y install oracle-java8-installer
   wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-5.1.2.deb
   sudo dpkg -i elasticsearch-5.1.2.deb
   sudo apt-get install apt-transport-https
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

try:
    from elasticsearch import Elasticsearch, RequestsHttpConnection
except ImportError:
    pass

try:
    from dj_geo.models import Zipcode
except ImportError:
    pass

from dj_node.nodes.list import ListNode
from dj_node.nodes.list_info import ListInfo
from dj_node.nodes.list_filter import ListFilter


class ElasticNode(ListNode):
    x_list_info_cls = ListInfo
    x_list_filter_cls = ListFilter
    x_col = "<col>"

    ES_INDEX = 'geo_data'
    ES_SERVER = '127.0.0.1'
    ES_PORT = 9200
    es = Elasticsearch(hosts=[{'host': ES_SERVER, 'port': ES_PORT}],
                       connection_class=RequestsHttpConnection)

    def _process(self, request):
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
