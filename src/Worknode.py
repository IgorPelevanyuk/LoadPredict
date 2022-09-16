from ResourceUsage import ResourceUsage
from Utils import Distributor
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
        self.requests = {}

        self.current_request = ResourceUsage()
        self.current_usage = ResourceUsage()

    def collect_requests(self, time):
        self.requests = {}
        for job in self.jobs:
            request = job.try_step(time)
            self.requests[job] = request

    def form_consolidated_request(self):
        self.full_request = ResourceUsage()
        for job in self.requests:
            self.full_request = self.full_request + self.requests[job]

    def apply_constraints(self, time):
        self.constrained_request['network'] = min(self.network * time, self.full_request['network'])
        self.constrained_request['ram'] = min(self.ram, self.full_request['ram'])
        self.constrained_request['cpu_usage'] = min(self.cores * self.db12 * time, self.full_request['cpu_usage'])

    def try_step(self, time=1):
        self.collect_requests(time)
        self.form_consolidated_request()
        # self.apply_constraints(time)
        # On upper levels CPU and RAM is irrelevant
        self.current_request = ResourceUsage({"network": min(self.network * time, self.full_request['network'])})
        return self.current_request

    def do_step(self, time=1, usage_response=ResourceUsage()):
        self.current_period = time
        self.current_usage = ResourceUsage()
        distributor = Distributor(usage_response['network'])
        for job in self.requests:
            distributor.add_request(job, self.requests[job]['network'])
        response = distributor.calculate_responses()
        for job in self.jobs:
            cpu_usage = min(self.db12 * time, job.current_request['cpu_usage'])
            network_usage = response[job]
            job_usage = ResourceUsage({
                "cpu_usage": cpu_usage,
                "network": network_usage,
            })
            job.do_step(job_usage)
            self.current_usage += job_usage
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

    def get_cpu_usage(self):
        return self.current_usage["cpu_usage"] / self.current_period

    def get_network_usage(self):
        return self.current_usage["network"] / self.current_period
