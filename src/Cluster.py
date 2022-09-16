from ResourceUsage import ResourceUsage
from Utils import Distributor
from Accounting import Accounting

import random


class Cluster(object):

    def __init__(self, worknodes, network, name, isAccounted=False):
        self.worknodes = worknodes
        self.network = network
        self.name = name
        self.requests = {}
        self.full_request = ResourceUsage()
        self.isAccounted = isAccounted
        if self.isAccounted:
            self.accounting = Accounting()

    def add_worknode(self, worknode):
        self.worknodes.append(worknode)

    def send_accounting(self):
        if self.isAccounted:
            self.accounting.add_data("running_slots", self.name, self.get_running_slots())

    def get_running_slots(self):
        count = 0
        for worknode in self.worknodes:
            count += worknode.count_jobs()
        return count

    def collect_requests(self, time):
        self.requests = {}
        for worknode in self.worknodes:
            request = worknode.try_step(time)
            self.requests[worknode] = request

    def form_consolidated_request(self):
        self.full_request = ResourceUsage()
        for worknode in self.requests:
            self.full_request = self.full_request + self.requests[worknode]

    def try_step(self, time=1):
        self.collect_requests(time)
        self.form_consolidated_request()
        # self.apply_constraints(time)
        # On upper levels CPU and RAM is irrelevant
        self.current_request = ResourceUsage({"network": min(self.network * time, self.full_request['network'])})
        return self.current_request

    def do_step(self, time=1, usage_response=ResourceUsage()):
        distributor = Distributor(usage_response['network'])
        for request in self.requests:
            distributor.add_request(request, self.requests[request]['network'])
        response = distributor.calculate_responses()
        for worknode in self.worknodes:
            worknode.do_step(time=time, usage_response=ResourceUsage({'network': response[worknode]}))
        self.send_accounting()

    def match_jobs(self, job_queue, amount=None):
        if amount is not None:
            submitted = 0
            # Consecutive job submit
            # for worknode in self.worknodes:
            #     for i in range(worknode.get_available_slots()):
            #         worknode.submit_job(job_queue.pop_job())
            #         submitted += 1
            #         if submitted == amount:
            #             return

            # Random job submit
            worknode_indexes = list(range(len(self.worknodes)))
            random.shuffle(worknode_indexes)
            for worknode_id in worknode_indexes:
                for i in range(self.worknodes[worknode_id].get_available_slots()):
                    self.worknodes[worknode_id].submit_job(job_queue.pop_job())
                    submitted += 1
                    if submitted == amount:
                        return

        # Consecutive job submit
        for worknode in self.worknodes:
            for i in range(worknode.get_available_slots()):
                worknode.submit_job(job_queue.pop_job())

        # Random job submit
        # worknode_indexes = list(range(len(self.worknodes)))
        # random.shuffle(worknode_indexes)
        # for worknode_id in worknode_indexes:
        #     for i in range(self.worknodes[worknode_id].get_available_slots()):
        #         self.worknodes[worknode_id].submit_job(job_queue.pop_job())


    def get_available_slots(self):
        free_slots = 0
        for worknode in self.worknodes:
            free_slots += worknode.get_available_slots()
        return free_slots

    def get_cpu_usage(self):
        usage = 0
        for worknode in self.worknodes:
            usage += worknode.get_cpu_usage()
        return usage

    def get_cpu_load(self):
        peak_load = 0
        for worknode in self.worknodes:
            peak_load += worknode.cores * worknode.db12
        return self.get_cpu_usage() / peak_load

    def get_network_usage(self):
        usage = 0
        for worknode in self.worknodes:
            usage += worknode.get_network_usage()
        return usage
