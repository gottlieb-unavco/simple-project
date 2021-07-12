from channels.generic.websocket import JsonWebsocketConsumer
from kafka_test.models import ExampleValue
from logging import getLogger
from kafka_test.kafka.producer import produce_example_message
from es_lib.utils import parse_iso8601, safe_json, parse_json

LOGGER = getLogger(__name__)


def clean_json(data):
    """
    JSON can be picky, so serialize safely then deserialize to get
    something safe for a picky parser
    """
    return parse_json(safe_json(data))


class ExampleConsumer(JsonWebsocketConsumer):
    """
    A websocket consumer for operations on the example topic
    """
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive_json(self, request):
        """
        Handle a message from the client
        """
        action = request.get('action')
        try:
            response = {}
            if action == 'send':
                # Send message
                response['result'] = self.action_send(request)
            elif action == 'list':
                # Updates since
                response['items'] = self.action_list_since(request)
            else:
                raise NotImplementedError("No action %s" % action)
            response['status'] = 'ok'
            self.send_json(response)
        except Exception as e:
            self.send_json({
                'status': 'error',
                'error': str(e),
            })

    def action_send(self, request):
        """
        Send a message on the kafka topic
        """
        value = request.get('value')
        produce_example_message(value)
        return value
    
    def action_list(self, request):
        """
        Return a list of items from the archive
        """
        qs = ExampleValue.objects.order_by('-created_date')
        since = request.get('since')
        if since:
            qs = qs.filter(created_date__gte=since)
        return clean_json(list(qs.values()[:20]))
