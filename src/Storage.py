from ResourceUsage import ResourceUsage


class Storage(object):

    def __init__(self, network):
        self.network = network

        self.requests = {}
        self.current_network_share = 0
        self.response = {}
        self.current_bandwidth = self.network

    def add_request(self, cluster, request):
        self.requests[cluster] = request

    def calculate_share(self):
        requested = sum([self.requests[cluster]['network'] for cluster in self.requests])
        full_response = min(requested, self.current_bandwidth)
        count_network_requests = sum([1 for cluster in self.requests if self.requests[cluster]['network'] != 0])
        self.current_network_share = full_response / count_network_requests

    def apply_current_network_share(self):
        is_bandwidth_changed = False
        for cluster in list(self.requests):
            if self.requests[cluster]['network'] < self.current_network_share:
                self.response[cluster] = ResourceUsage({'network': self.requests[cluster]['network']})
                self.current_bandwidth -= self.requests[cluster]['network']
                del self.requests[cluster]
                is_bandwidth_changed = True
        return is_bandwidth_changed

    def calculate_responses(self):
        self.response = {}
        self.current_bandwidth = self.network
        while len(self.requests) != 0:
            self.calculate_share()
            is_changed = self.apply_current_network_share()
            if not is_changed:
                for cluster in list(self.requests.keys()):
                    self.response[cluster] = ResourceUsage({'network': self.current_network_share})
                    del self.requests[cluster]
