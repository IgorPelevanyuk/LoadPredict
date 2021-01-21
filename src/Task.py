from ResourceUsage import ResourceUsage

class Task():
    completion_percent = 0

    def __init__(self):
        self.completion_percent = 0

class ComputingTask(Task):
    compute_amount = 0
    computed = 0

    def __init__(self, compute_amount):
        super().__init__()
        self.compute_amount = compute_amount

    def try_step(self, time=1):
        to_compute = max(0, self.compute_amount - self.computed)
        usage_request = ResourceUsage({'cpu_usage': to_compute})
        return usage_request

    def do_step(self, usage_response):
        self.computed += usage_response.resource_usage['cpu_usage']
        if self.computed >= self.compute_amount:
            return True
        return False

    def __repr__(self):
        return str({"compute_amount": self.compute_amount, "computed": self.computed})


class TransferTask(Task):
    transfer_amount = 0
    transferred = 0

    def __init__(self, transfer_amount):
        super().__init__()
        self.transfer_amount = transfer_amount

    def try_step(self, time=1):
        usage_request = ResourceUsage({'network': self.transfer_amount - self.transferred})
        return usage_request

    def do_step(self, usage_response):
        self.transferred += usage_response.resource_usage['network']
        if self.transferred >= self.transfer_amount:
            return True
        return False

    def __repr__(self):
        return str({"transfer_amount": self.transfer_amount, "transferred": self.transferred})
