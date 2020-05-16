from django.test import RequestFactory

PROTECTED_VARIABLES = [
    'consumer',
    'element',
    'selectors',
    'session',
    'url',
]


class Reflex:
    def __init__(self, consumer, url, element, selectors):
        self.consumer = consumer
        self.url = url
        self.element = element
        self.selectors = selectors
        self.session = consumer.scope['session']

    @property
    def request(self):
        factory = RequestFactory()
        request = factory.get(self.url)
        request.session = self.consumer.scope['session']
        request.user = self.consumer.scope['user']
        return request
