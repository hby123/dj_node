# import sys
# import math
# from django.test import TestCase
# from django.test import Client
# from django.conf import settings
# from dj_node.nodes.search import ESGeoNode
#
# class dj_nodeGeoTest(TestCase):
#
#     def setUp(self):
#         pass
#
#     def test_elastic_search(self):
#         # ----- setup -----
#         class MyGeoTestNode(ESGeoNode):
#             ES_INDEX = 'test_geo_data001'
#             ES_DOC = 'my_type'
#             ES_SERVER = '127.0.0.1'
#             ES_PORT = 9200
#
#             CREATE_INDEX_MAPPING = {
#               "mappings": {
#                 ES_DOC: {
#                   "properties": {
#                     "location": {
#                       "type": "geo_point"
#                     }
#                   }
#                 }
#               }
#             }
#
#             SEARCH_MAPPING = {
#                 "query": {
#                     "bool" : {
#                         "must" : {
#                             "match_all" : {}
#                         },
#                         "filter" : {
#                             "geo_distance" : {
#                                 "distance" : "250mi",
#                                 'location': {
#                                     "lat": 38.907192,
#                                     "lon": -77.036871
#                                 }
#                             }
#                         }
#                     }
#                 },
#                 "sort" : [
#                     {
#                         "_geo_distance" : {
#                             "location" : [38.907192, -77.036871],
#                             "order" : "asc",
#                             "unit" : "mi",
#                             "mode" : "min",
#                             "distance_type" : "sloppy_arc"
#                         }
#                     }
#                 ],
#                 "from": 0,
#                 "size": 0,
#             }
#
#         # ----- create index -----
#         node = MyGeoTestNode()
#         node.es.indices.delete(index=MyGeoTestNode.ES_INDEX, ignore=[400, 404])
#         node.es.indices.create(index=MyGeoTestNode.ES_INDEX, body=node.CREATE_INDEX_MAPPING)
#         node.es.indices.refresh(index=MyGeoTestNode.ES_INDEX)
#
#         # ----- insert doc -----
#         for i in range(1, 101):
#             doc = {'text': 'DC %d' % i,
#                    'location': {
#                         "lat": 38.907192,
#                         "lon": -77.036871
#                     }}
#             node.es.index(MyGeoTestNode.ES_INDEX, doc_type="my_type", body=doc)
#
#             doc = {'text': 'New York %d' % i,
#                    'location': {
#                         "lat": 40.712784,
#                         "lon": -74.005941
#                     }}
#             node.es.index(MyGeoTestNode.ES_INDEX, doc_type="my_type", body=doc)
#
#             doc = {'text': 'San Francisco %d' % i,
#                    'location': {
#                         "lat": 37.771582,
#                         "lon": -122.409904
#                     }}
#             node.es.index(MyGeoTestNode.ES_INDEX, doc_type="my_type", body=doc)
#
#
#         #----- paging setup  -----
#         ipp = 20;
#         node.es.indices.refresh(index=MyGeoTestNode.ES_INDEX)
#         res = node.es.search(index=MyGeoTestNode.ES_INDEX, body=node.SEARCH_MAPPING)
#         total =  res['hits']['total']
#         print "total: %d" % res['hits']['total']
#
#         # ----- loop thru each page -----
#         counter = 0
#         dc_array = []
#         ny_array = []
#         for page in range(1, int(math.ceil(float(total)/float(ipp))+1)):
#             print ">>>>>Working on page: %d" % page
#             node.SEARCH_MAPPING['from'] = (page -1) * ipp
#             node.SEARCH_MAPPING['size'] = ipp
#             node.es.indices.refresh(index=MyGeoTestNode.ES_INDEX)
#             res = node.es.search(index=MyGeoTestNode.ES_INDEX, body=node.SEARCH_MAPPING)
#             for hit in res['hits']['hits']:
#                 counter = counter + 1
#                 city = hit['_source']['text']
#                 print str(counter) + " - " + city
#
#                 if "DC" in city:
#                     self.assertTrue(city not in dc_array )
#                     dc_array.append(city)
#                 elif "New York" in city:
#                     self.assertTrue(city not in ny_array )
#                     ny_array.append(city)
#                 else:
#                     raise Exception("Error city: %s" % city )
#
#         self.assertTrue(len(dc_array) == 100)
#         self.assertTrue(len(ny_array) == 100)
#
#     # def test_get_zip_by_ip(self):
#     #     c = Client()
#     #     response = c.get('/mojo/login/?test_ip=74.125.224.72', follow=True)
#     #     self.assertTrue(response.context['request'].zip_obj)
#     #
#     # def test_get_zip_by_str(self):
#     #     from dj_node.geo.geo import Geo
#     #     zip_obj = Geo.get_zip_obj_by_str("Rockville, MD")
#     #     self.assertTrue(zip_obj)