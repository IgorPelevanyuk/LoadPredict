from ResourceUsage import ResourceUsage
from Utils import Distributor


class Storage(object):

    def __init__(self, network):
        self.network = network

        self.requests = {}
        self.current_network_share = 0
        self.response = {}
        self.current_bandwidth = self.network

    def add_request(self, cluster, request):
        self.requests[cluster] = request

    def calculate_responses(self):
        self.response = {}
        distributor = Distributor(self.network)
        for request in self.requests:
            distributor.add_request(request, self.requests[request]['network'])
        response = distributor.calculate_responses()
        for response_id in response:
            self.response[response_id] = ResourceUsage({'network': response[response_id]})
