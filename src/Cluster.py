from ResourceUsage import ResourceUsage


class Cluster(object):
    network = 0

    worknodes = []
    requests = []
    full_request = ResourceUsage()

    def __init__(self, network):
        self.network = network

    def add_worknode(self, worknode):
        self.worknodes.append(worknode)

    def collect_requests(self, time):
        self.requests = []
        for worknode in self.worknodes:
            request = worknode.try_step(time)
            self.requests.append(request)

    def form_consolidated_request(self):
        self.full_request = ResourceUsage()
        for request in self.requests:
            self.full_request = self.full_request + request

    def try_step(self, time=1):
        self.collect_requests(time)
        self.form_consolidated_request()
        # self.apply_constraints(time)
        # On upper levels CPU and RAM is irrelevant
        return ResourceUsage({"network": min(self.network, self.full_request['network'])})

    def do_step(self, time=1, usage_response=ResourceUsage()):
        network_share = self.network
        if usage_response['network'] < self.full_request['network']:
            count_network_requests = sum([1 for worknode in self.worknodes if worknode.current_request['network'] != 0])
            network_share = usage_response['network'] / count_network_requests
        for worknode in self.worknodes:
            network_usage = min(network_share, worknode.current_request['network'])
            worknode_usage = ResourceUsage({
                "network": network_usage,
            })
            worknode.do_step(worknode_usage)