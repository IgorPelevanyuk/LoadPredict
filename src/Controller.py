from ResourceUsage import ResourceUsage


class Controller(object):

    def __init__(self, clusters, storages, job_queue):
        self.clusters = clusters
        self.storages = storages
        self.job_queue = job_queue
        self.current_time = 0

    def match_jobs_to_clusters(self):
        for cluster in self.clusters:
            cluster.match_jobs(self.job_queue, 20)

    def do_step(self, time=1):
        if self.current_time % 60 == 0:
            self.match_jobs_to_clusters()

        for cluster in self.clusters:
            request = cluster.try_step(time=1)
            self.storage.add_request(cluster, request)



