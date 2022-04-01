from ResourceUsage import ResourceUsage


class Storage(object):
    network = 0

    requests = {}
    full_request = ResourceUsage()
    responses = {}

    def __init__(self, network):
        self.network = network

    def add_request(self, id, request):
        self.requests[id] = request

    def form_consolidated_request(self):
        self.full_request = ResourceUsage()
        for request_id in self.requests:
            self.full_request = self.full_request + self.requests[request_id]

    def do_step(self, time):
        network_share = self.network
        if self.network < self.full_request['network']:
            count_network_requests = sum([1 for request_id in self.requests if self.requests[request_id]['network'] != 0])
            network_share = self.network / count_network_requests
        for request_id in self.requests:
            network_usage = min(network_share, self.requests[request_id]['network'])
            cluster_usage = ResourceUsage({
                "network": network_usage,
            })
            self.responses[request_id] = cluster_usage
