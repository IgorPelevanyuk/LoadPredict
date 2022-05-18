class Distributor(object):

    def __init__(self, resource_amount):
        self.total_amount = resource_amount
        self.requests = {}
        self.response = {}
        self.current_amount = resource_amount
        self.current_share = 0

    def add_request(self, request_id, request):
        self.requests[request_id] = request

    def calculate_share(self):
        requested = sum([self.requests[request_id] for request_id in self.requests])
        full_response = min(requested, self.current_amount)
        count_requests = sum([1 for request_id in self.requests if self.requests[request_id] != 0])
        self.current_share = full_response / count_requests

    def apply_current_share(self):
        is_current_amount_changed = False
        for request_id in list(self.requests):
            if self.requests[request_id] < self.current_share:
                self.response[request_id] = self.requests[request_id]
                self.current_amount -= self.requests[request_id]
                del self.requests[request_id]
                is_current_amount_changed = True
        return is_current_amount_changed

    def calculate_responses(self):
        self.response = {}
        self.current_amount = self.total_amount
        while len(self.requests) != 0:
            self.calculate_share()
            is_changed = self.apply_current_share()
            if not is_changed:
                for request_id in list(self.requests.keys()):
                    self.response[request_id] = self.current_share
                    del self.requests[request_id]
        return self.response
