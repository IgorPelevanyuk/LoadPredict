from ResourceUsage import ResourceUsage
from Accounting import Accounting

class Controller(object):

    def __init__(self, clusters, storage, job_queue):
        self.clusters = clusters
        self.storage = storage
        self.job_queue = job_queue
        self.current_time = 0
        self.accounting = Accounting()

    def match_jobs_to_clusters(self, amount=None):
        for cluster in self.clusters:
            cluster.match_jobs(self.job_queue, amount)

    def get_running_slots(self):
        count = 0
        for cluster in self.clusters:
            count += cluster.get_running_slots()
        return count

    def is_busy(self):
        if self.job_queue.get_size() > 0:
            return True
        else:
            if self.get_running_slots() > 0:
                return True
        return False

    def do_step(self, time=1):
        if self.current_time % 60 == 0:
            self.match_jobs_to_clusters()

        self.current_time += time
        self.accounting.set_time(self.current_time)
        self.accounting.add_data("job_queue", "size", self.job_queue.get_size())

        for cluster in self.clusters:
            request = cluster.try_step(time=time)
            self.storage.add_request(cluster, request)
        responses = self.storage.calculate_responses(time=time)

        for cluster in self.clusters:
            cluster.do_step(time=time, usage_response=responses[cluster])

    def get_jobqueue_size(self):
        return self.job_queue.get_size()



