import math
import urlparse

from bs4 import BeautifulSoup
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test import Client
from django.test.client import RequestFactory
from dj_node.models import Content
from dj_node.nodes.list_info import ListInfo
from dj_node.nodes.content import ContentListNode
from dj_node.nodes.content import sample_data

my_email = "test@domain.com"
my_domain = "testserver"


def get_page_item_id(response):
    id_list = []
    soup = BeautifulSoup(response.content, "html.parser")
    item_list = soup.find("ul", { "class" : "list-result" })
    item_group = item_list.findAll("li", { "class" : "list-item" })
    for li in item_group:
        id = li['id'].split('-')[-1]
        id_list.append(int(id))
    return id_list

class DjNodeListNodeTest(TestCase):
    URL_NAME = 'content-list'

    def setUp(self):
        sample_data()

    def test_list(self):
        self.assertTrue(Content.objects.all().count() > 50)

        c = Client()
        response = c.get(reverse(self.URL_NAME))

        # check template
        assert "1-20" in response.content

    def test_full_list(self):
        """Test: Make sure all items are in list
        """
        c = Client()
        response = c.get(reverse(self.URL_NAME))

        soup = BeautifulSoup(response.content, "html.parser")

        pagination = soup.find("ul", { "class" : "pagination" })
        pagination_li = pagination.findAll("li")

        href_list = []
        for li in pagination_li:
            a = li.find("a")
            if a.text != '1':
                href = a['href']
                href_list.append(href)
        assert len(href_list) > 0

        # form the id list from page
        item_list = get_page_item_id(response)
        for url in href_list:
            item_list = item_list + get_page_item_id(c.get(url))

        id_list = [x.id for x in  Content.objects.all()]
        assert len(id_list) == len(item_list)

        for id in id_list:
            assert id in item_list

    def test_list_info(self):
        """Test: Showing 1-20 of 150 results
        """
        count = Content.objects.all().count()

        # getfirst page
        c = Client()
        response = c.get(reverse(self.URL_NAME))

        # pre-calc start and end items
        factory = RequestFactory()
        request = factory.get(reverse(self.URL_NAME))
        list_info = ListInfo(ContentListNode, request)
        page = 1
        start = 1
        end = start + (list_info.ipp - 1)
        if end >= count:
            end = count
        info_str = "Showing %d-%d of %d results" % (start, end, count)

        # check info str on first page
        soup = BeautifulSoup(response.content, "html.parser")
        list_info = soup.find("div", {"class":'list-info'})
        assert info_str ==  ' '.join(list_info.text.split())

        # collect other page links
        pagination = soup.find("ul", { "class" : "pagination" })
        pagination_li = pagination.findAll("li")

        # test pagination list
        href_list = []
        for li in pagination_li:
            a = li.find("a")
            if a.text != '1':
                href = a['href']
                href_list.append(href)
        assert len(href_list) > 0

        # form the id list from page
        for url in href_list:
            # get page number
            page = dict(urlparse.parse_qsl(urlparse.urlsplit(url).query))['page']
            page = int(page)

            # pre-cal start and end number
            factory = RequestFactory()
            request = factory.get(reverse(self.URL_NAME))
            list_info = ListInfo(ContentListNode, request)
            start = 1 + (page - 1) * (list_info.ipp)
            end = start + (list_info.ipp- 1)
            if end >= count:
                end = count

            # check info str on the other page
            response = c.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            list_info = soup.find("div", {"class":'list-info'})
            info_str = "Showing %d-%d of %d results" % (start, end, count)
            assert info_str ==  ' '.join(list_info.text.split())


class DjNodeListPaginationTest(TestCase):
    URL_NAME = 'content-list'

    def setUp(self):
        sample_data()

    def test_pagination(self):
        count = Content.objects.all().count()
        assert count > 0

        c = Client()
        response = c.get(reverse(self.URL_NAME))

        # check paginatio in html
        soup = BeautifulSoup(response.content, "html.parser")
        pagination = soup.find("ul", { "class" : "pagination" })
        assert pagination != None

        pagination_fail = soup.find("ul", { "class" : "pagination_fail" })
        assert pagination_fail == None

        # check number of items in paginations
        pagination_li = pagination.findAll("li")

        factory = RequestFactory()
        request = factory.get(reverse(self.URL_NAME))
        list_info = ListInfo(ContentListNode, request)
        num_page = math.ceil(float(count)/float(list_info.ipp))
        assert num_page == len(pagination_li)

        # test pagination list
        href_count = 0
        for li in pagination_li:
            a = li.find("a")
            href = a['href']
            href_count = href_count + 1
            assert "?&" not in href
        assert href_count == len(pagination_li)


class DjNodeListSortTest(TestCase):
    URL_NAME = 'content-list'

    def setUp(self):
        sample_data()

    def test_list_sort_asc(self):
        """Test: Showing 1-20 of 150 results
        """
        # getfirst page
        id_list = []
        c = Client()
        response = c.get(reverse(self.URL_NAME)+"?sort=id")
        id_list = id_list + get_page_item_id(response)

        # check info str on first page
        soup = BeautifulSoup(response.content, "html.parser")
        pagination = soup.find("ul", { "class" : "pagination" })
        pagination_li = pagination.findAll("li")

        # collect other pagination links
        href_list = []
        for li in pagination_li:
            a = li.find("a")
            if a.text != '1':
                href = a['href']
                href_list.append(href)
                assert 'sort' in href
        assert len(href_list) > 0

        # form the id list from page
        for url in href_list:
            # check info str on the other page
            response = c.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            id_list = id_list + get_page_item_id(response)

        # check order of ids
        db_list = [x.id for x in Content.objects.all().order_by("id")]
        assert len(id_list) > 0
        assert len(id_list) == len(db_list)
        for i in range(0, len(id_list)):
            assert id_list[i] == db_list[i]

    def test_list_sort_desc(self):
        """Test: Showing 1-20 of 150 results
        """

        # getfirst page
        id_list = []
        c = Client()
        response = c.get(reverse(self.URL_NAME)+"?sort=-id")
        id_list = id_list + get_page_item_id(response)

        # check info str on first page
        soup = BeautifulSoup(response.content, "html.parser")
        pagination = soup.find("ul", { "class" : "pagination" })
        pagination_li = pagination.findAll("li")

        # collect other pagination links
        href_list = []
        for li in pagination_li:
            a = li.find("a")
            if a.text != '1':
                href = a['href']
                assert 'sort' in href
                href_list.append(href)
        assert len(href_list) > 0

        # form the id list from page
        for url in href_list:
            # check info str on the other page
            response = c.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            id_list = id_list + get_page_item_id(response)

        # check order of ids
        db_list = [x.id for x in Content.objects.all().order_by("-id")]
        assert len(id_list) > 0
        assert len(id_list) == len(db_list)
        for i in range(0, len(id_list)):
            assert id_list[i] == db_list[i]

class DjNodeListFilterTest(TestCase):
    URL_NAME = 'content-list'

    def setUp(self):
        sample_data()

    def test_list_option_filter(self):
        """Test: Showing 1-20 of 150 results
        """
        c = Client()
        response = c.get(reverse(self.URL_NAME))
        soup = BeautifulSoup(response.content, "html.parser")
        option_filter_blocks = soup.findAll("div", { "class" : "filter"})

        assert option_filter_blocks != None

        for block in option_filter_blocks:
            print block.content
            options = block.findAll("li", { "class" : "filter-item"})
            assert len(options) > 0

            for option in options:
                link = option.find("a")
                assert link['href'] != None
                assert "oo_" in link['href']

    def test_list_selected_filter(self):
        """Test: Showing 1-20 of 150 results
        """
        def collect_ids(response):
            id_list = get_page_item_id(response)

            soup = BeautifulSoup(response.content, "html.parser")
            pagination = soup.find("ul", { "class" : "pagination" })
            pagination_li = pagination.findAll("li")

            # collect other pagination links
            href_list = []
            for li in pagination_li:
                a = li.find("a")
                if a.text != '1':
                    href = a['href']
                    href_list.append(href)

            for url in href_list:
                response = c.get(url)
                id_list = id_list + get_page_item_id(response)
            return id_list

        c = Client()
        response = c.get(reverse(self.URL_NAME))
        soup = BeautifulSoup(response.content, "html.parser")
        option_filter_blocks = soup.findAll("div", { "class" : "list-filter"})
        assert len(option_filter_blocks) == 1

        filter_links = []
        for block in option_filter_blocks:
            title = block.find("h3")
            assert title.text != None
            assert title.text != ""

            options = block.findAll("li", { "class" : "filter-item"})
            assert len(options) > 0

            links = []
            for option in options:
                link = option.find("a")
                assert link['href'] != None
                assert "oo_" in link['href']
                links.append(link['href'])
            filter_links.append(links)

        assert len(filter_links) > 0

        # test filter links
        for cat in filter_links:
            for filter_link in cat:
                response = c.get(filter_link)
                id_list = collect_ids(response)
                assert len(id_list) > 0

                soup = BeautifulSoup(response.content, "html.parser")
                selected_list = soup.findAll("li", { "class" : "selected-filter" })
                assert len(selected_list) > 0

                # check removed filter
                for selected in selected_list:
                    remove_link = selected.findAll("a")
                    response = c.get(remove_link[0]['href'])
                    soup = BeautifulSoup(response.content, "html.parser")
                    selected_list = soup.findAll("li", { "class" : "selected-filter" })
                    assert len(selected_list) == 0



class DjNodeItemNodeTest(TestCase):
    URL_NAME = 'content-item'

    def setUp(self):
        sample_data()

    def test_list(self):
        self.assertTrue(Content.objects.all().count() > 50 )

        c = Client()
        user_content = Content.objects.all().first()
        response = c.get(reverse(self.URL_NAME) +  '?id={}'.format(user_content.id))

        # check template
        assert str(user_content) in response.content


