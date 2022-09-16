from ResourceUsage import ResourceUsage
from Utils import Distributor
from Accounting import Accounting


class Storage(object):

    def __init__(self, network):
        self.network = network

        self.requests = {}
        self.current_network_share = 0
        self.response = {}
        self.current_bandwidth = self.network

        self.accounting = Accounting()

    def add_request(self, cluster, request):
        self.requests[cluster] = request

    def calculate_responses(self, time=1):
        self.response = {}
        total_network_response = 0
        distributor = Distributor(self.network * time)
        for request in self.requests:
            distributor.add_request(request, self.requests[request]['network'])
        response = distributor.calculate_responses()
        for response_id in response:
            self.response[response_id] = ResourceUsage({'network': response[response_id]})
            total_network_response += response[response_id]
        self.requests = {}
        self.accounting.add_data("storage", "load", total_network_response / time)
        return self.response
