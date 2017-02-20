from django.test import TestCase
from dj_node.nodes.utils import Utils

from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from django.test.client import RequestFactory

class dj_nodeUtilTest(TestCase):

    def test_is_login(self):
        factory = RequestFactory()
        request = factory.get("/")
        assert Utils.is_login(request) == False

    def test_set_session(self):
        factory = RequestFactory()
        request = factory.get("/")

        middleware = SessionMiddleware()
        middleware.process_request(request)

        Utils.set_session(request, "key", "value")
        Utils.del_session(request, "key")

    def test_set_msg(self):
        factory = RequestFactory()
        request = factory.get("/")

        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        Utils.set_msg(request, "my msg")

    def test_get_mojo_domain(self):
        factory = RequestFactory()
        request = factory.get("/")

        middleware = SessionMiddleware()
        middleware.process_request(request)

        request.session.save
        Utils.get_mojo_domain(request)

    def test_get_mojo_site(self):
        factory = RequestFactory()
        request = factory.get("/")

        middleware = SessionMiddleware()
        middleware.process_request(request)

        request.session.save
        Utils.get_mojo_site(request)
