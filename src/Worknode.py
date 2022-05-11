from ResourceUsage import ResourceUsage
import copy

class Worknode(object):
    #jobs = []
    #requests = []
    #full_request = ResourceUsage()
    #constrained_request = ResourceUsage()

    def __init__(self, cores, db12, ram, network):
        self.cores = cores
        self.db12 = db12
        self.ram = ram
        self.network = network

        self.jobs = []
        self.requests = []

    def collect_requests(self, time):
        self.requests = []
        for job in self.jobs:
            request = job.try_step(time)
            self.requests.append(request)

    def form_consolidated_request(self):
        self.full_request = ResourceUsage()
        for request in self.requests:
            self.full_request = self.full_request + request

    def apply_constraints(self, time):
        self.constrained_request['network'] = min(self.network * time, self.full_request['network'])
        self.constrained_request['ram'] = min(self.ram, self.full_request['ram'])
        self.constrained_request['cpu_usage'] = min(self.cores * self.db12 * time, self.full_request['cpu_usage'])

    def try_step(self, time=1):
        self.collect_requests(time)
        self.form_consolidated_request()
        # self.apply_constraints(time)
        # On upper levels CPU and RAM is irrelevant
        return ResourceUsage({"network": min(self.network, self.full_request['network'])})

    def do_step(self, time=1, usage_response=ResourceUsage()):
        network_share = self.network
        if usage_response['network'] < self.full_request['network']:
            count_network_requests = sum([1 for job in self.jobs if job.current_request['network'] != 0])
            network_share = usage_response['network'] / count_network_requests
        for job in self.jobs:
            if job.current_request['network'] < network_share:
                job.do_step(ResourceUsage({"network": job.current_request['network']}))
            cpu_usage = min(self.db12 * time, job.current_request['cpu_usage'])
            # ram usage - think about incremental requests and static requests
            network_usage = min(network_share, job.current_request['network'])
            job_usage = ResourceUsage({
                "cpu_usage": cpu_usage,
                "network": network_usage,
            })
            job.do_step(job_usage)
        self.jobs = [job for job in self.jobs if not job.isDone]

    def submit_job(self, job):
        if job is not None:
            self.jobs.append(job)

    def count_jobs(self):
        return len(self.jobs)

    def get_slots(self):
        return self.cores

    def get_available_slots(self):
        return self.get_slots() - self.count_jobs()
