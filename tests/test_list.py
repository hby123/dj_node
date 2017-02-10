import math

from bs4 import BeautifulSoup
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test import Client
from django.test.client import RequestFactory

from dj_node.models import UserContent
from dj_node.nodes.list_info import ListInfo
from dj_node.nodes.user_content import UserContentListNode

my_email = "test@domain.com"
my_domain = "testserver"

class dj_nodeListNodeTest(TestCase):
    URL_NAME = 'user-content-list'

    def setUp(self):
        UserContent.dummy()

    def test_list(self):
        self.assertTrue(UserContent.objects.all().count() > 50)

        c = Client()
        response = c.get(reverse(self.URL_NAME))

        # check template
        assert "1-20" in response.content

    def test_full_list(self):
        """Test: Make sure all items are in list
        """
        def get_page_item_id(response, id_list):
            soup = BeautifulSoup(response.content, "html.parser")
            item_list = soup.find("ul", { "class" : "item-list" })
            item_group = item_list.findAll("li", { "class" : "item" })
            for li in item_group:
                id_str = li['class'][-1]
                id = id_str.split('-')[-1]
                id_list.append(int(id))
            return id_list

        id_list = [x.id for x in  UserContent.objects.all()]
        assert len(id_list) > 0

        c = Client()
        response = c.get(reverse(self.URL_NAME))

        soup = BeautifulSoup(response.content, "html.parser")
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
        item_list = []
        item_list = get_page_item_id(response, item_list )

        for url in href_list:
            response = c.get(url)
            item_list = get_page_item_id(response, item_list )

        assert len(id_list) == len(item_list)
        for id in id_list:
            if id not in item_list:
                raise Exception("Missing item in list ")

    def test_list_info(self):
        """Test: Showing 1-20 of 150 results
        """
        count = UserContent.objects.all().count()

        # getfirst page
        c = Client()
        response = c.get(reverse(self.URL_NAME))

        # pre-calc start and end items
        factory = RequestFactory()
        request = factory.get(reverse(self.URL_NAME))
        list_info = ListInfo(UserContentListNode, request)
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
            page = int(url.split("?")[-1].split("=")[-1])

            # pre-cal start and end number
            factory = RequestFactory()
            request = factory.get(reverse(self.URL_NAME))
            list_info = ListInfo(UserContentListNode, request)
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


class dj_nodeListPaginationTest(TestCase):
    URL_NAME = 'user-content-list'

    def setUp(self):
        UserContent.dummy()

    def test_pagination(self):
        count = UserContent.objects.all().count()
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
        list_info = ListInfo(UserContentListNode, request)
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


class dj_nodeListSortTest(TestCase):
    URL_NAME = 'user-content-list'

    def setUp(self):
        UserContent.dummy()

    def test_list_sort_asc(self):
        """Test: Showing 1-20 of 150 results
        """
        def get_page_item_id(response, id_list):
            soup = BeautifulSoup(response.content, "html.parser")
            item_list = soup.find("ul", { "class" : "item-list" })
            item_group = item_list.findAll("li", { "class" : "item" })
            for li in item_group:
                id_str = li['class'][-1]
                id = id_str.split('-')[-1]
                id_list.append(int(id))
            return id_list

        # getfirst page
        id_list = []
        c = Client()
        response = c.get(reverse(self.URL_NAME)+"?sort=id")
        id_list = get_page_item_id(response, id_list)

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
            id_list = get_page_item_id(response, id_list)

        # check order of ids
        db_list = [x.id for x in UserContent.objects.all().order_by("id")]
        assert len(id_list) > 0
        assert len(id_list) == len(db_list)
        for i in range(0, len(id_list)):
            assert id_list[i] == db_list[i]

    def test_list_sort_desc(self):
        """Test: Showing 1-20 of 150 results
        """
        def get_page_item_id(response, id_list):
            soup = BeautifulSoup(response.content, "html.parser")
            item_list = soup.find("ul", { "class" : "item-list" })
            item_group = item_list.findAll("li", { "class" : "item" })
            for li in item_group:
                id_str = li['class'][-1]
                id = id_str.split('-')[-1]
                id_list.append(int(id))
            return id_list

        # getfirst page
        id_list = []
        c = Client()
        response = c.get(reverse(self.URL_NAME)+"?sort=-id")
        id_list = get_page_item_id(response, id_list)

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
            id_list = get_page_item_id(response, id_list)

        # check order of ids
        db_list = [x.id for x in UserContent.objects.all().order_by("-id")]
        assert len(id_list) > 0
        assert len(id_list) == len(db_list)
        for i in range(0, len(id_list)):
            assert id_list[i] == db_list[i]

class dj_nodeListFilterTest(TestCase):
    URL_NAME = 'user-content-list'

    def setUp(self):
        UserContent.dummy()

    def test_list_option_filter(self):
        """Test: Showing 1-20 of 150 results
        """
        c = Client()
        response = c.get(reverse(self.URL_NAME))
        soup = BeautifulSoup(response.content, "html.parser")
        option_filter_blocks = soup.findAll("div", { "class" : "option-filter-block"})
        assert len(option_filter_blocks) == 2

        for block in option_filter_blocks:
            title = block.find("h3")
            assert title.text != None
            assert title.text != ""

            options = block.findAll("li", { "class" : "option-item"})
            assert len(options) > 0

            for option in options:
                link = option.find("a")
                assert link['href'] != None
                assert "oo_" in link['href']

    def test_list_selected_filter(self):
        """Test: Showing 1-20 of 150 results
        """
        def check_selected_filters(response):
            soup = BeautifulSoup(response.content, "html.parser")
            selected_list = soup.findAll("li", { "class" : "selected-filter-item" })
            assert len(selected_list) > 0

        def get_page_item_id(response):
            id_list = []
            soup = BeautifulSoup(response.content, "html.parser")
            item_list = soup.find("ul", { "class" : "item-list" })
            item_group = item_list.findAll("li", { "class" : "item" })
            for li in item_group:
                id_str = li['class'][-1]
                id = id_str.split('-')[-1]
                id_list.append(int(id))
            return id_list

        def collect_ids(response):
            id_list = []
            new_ids = get_page_item_id(response)
            id_list = id_list + new_ids

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
            assert len(href_list) > 0

            for url in href_list:
                response = c.get(url)
                new_ids = get_page_item_id(response)
                id_list = id_list + new_ids
            return id_list

        c = Client()
        response = c.get(reverse(self.URL_NAME))
        soup = BeautifulSoup(response.content, "html.parser")
        option_filter_blocks = soup.findAll("div", { "class" : "option-filter-block"})
        assert len(option_filter_blocks) == 2

        filter_links = []
        for block in option_filter_blocks:
            title = block.find("h3")
            assert title.text != None
            assert title.text != ""

            options = block.findAll("li", { "class" : "option-item"})
            assert len(options) > 0

            links = []
            for option in options:
                link = option.find("a")
                assert link['href'] != None
                assert "oo_" in link['href']
                links.append(link['href'])
            filter_links.append(links)

        assert len(filter_links) == 2

        # test filter links
        for cat in filter_links:
            for filter_link in cat:
                response = c.get(filter_link)
                check_selected_filters(response)

                id_list = collect_ids(response)
                assert len(id_list) > 0

                filter_name = filter_link.split('?')[-1].split('=')[0].replace("oo_", '')
                filter_val = filter_link.split('?')[-1].split('=')[1]

                for id in id_list:
                    obj = UserContent.objects.get(id=id)
                    obj_filter_val = eval("obj.%s" % filter_name)
                    assert obj_filter_val == filter_val

                for obj in eval("UserContent.objects.filter(%s='%s')" % (filter_name, filter_val)):
                    assert obj.id in id_list

    def test_list_selected_filter_remove(self):
        c = Client()
        response = c.get(reverse(self.URL_NAME))
        soup = BeautifulSoup(response.content, "html.parser")
        option_filter_blocks = soup.findAll("div", { "class" : "option-filter-block"})

        filter_links = []
        for block in option_filter_blocks:
            title = block.find("h3")
            assert title.text != None
            assert title.text != ""

            options = block.findAll("li", { "class" : "option-item"})
            assert len(options) > 0

            links = []
            for option in options:
                link = option.find("a")
                assert link['href'] != None
                assert "oo_" in link['href']
                links.append(link['href'])
            filter_links.append(links)

        for cat in filter_links:
            for filter_link in cat:
                response = c.get(filter_link)
                soup = BeautifulSoup(response.content, "html.parser")
                selected = soup.find("li", { "class" : "selected-filter-item" })
                remove_link = selected.find("a")['href']

                assert remove_link != None
                assert remove_link != ""

                response = c.get(remove_link)
                soup = BeautifulSoup(response.content, "html.parser")
                selected_list = soup.findAll("li", { "class" : "selected-filter-item" })
                assert len(selected_list) == 0

class dj_nodeItemNodeTest(TestCase):
    URL_NAME = 'user-content-item'

    def setUp(self):
        UserContent.dummy()

    def test_list(self):
        self.assertTrue(UserContent.objects.all().count() > 50 )

        c = Client()
        user_content = UserContent.objects.all().first()
        response = c.get(reverse(self.URL_NAME, kwargs={'slug':user_content.slug, 'id':user_content.id}))

        # check template
        assert str(user_content) in response.content


class dj_nodeFormNodeTest(TestCase):
    URL_NAME = 'user-content-form'

    def setUp(self):
        UserContent.dummy()

    def test_form_get(self):
        self.assertTrue(UserContent.objects.all().count() > 50 )

        c = Client()
        user_content = UserContent.objects.all().first()
        response = c.get(reverse(self.URL_NAME))

        # check template

        # check field
        soup = BeautifulSoup(response.content, 'html.parser')
        name_field = soup.find('input', {'name':'name'})
        assert name_field != None

        submit_field = soup.find('button', {'type':'submit'})
        assert submit_field != None

    def test_form_post(self):
        self.assertTrue(UserContent.objects.all().count() > 50 )

        c = Client()
        user_content = UserContent.objects.all().first()
        response = c.post(reverse(self.URL_NAME), {'name': 'hi'}, follow=False)
        assert response.url == "http://testserver/"