from ResourceUsage import ResourceUsage
from Task import ComputingTask
from Task import TransferTask
from Job import Job
from Worknode import Worknode
from Cluster import Cluster
from Storage import Storage
from JobQueue import JobQueue
import copy

worknode = Worknode(1, 10, 16000, 10000000)  # 1 GB
cluster_temp = Cluster([worknode], 10000000)  # 10 GB
clusters = [copy.deepcopy(cluster_temp) for i in range(5)]

storage = Storage(10000000)  # 10 GB

job_1_1 = Job([TransferTask(1000000)])
job_1_2 = Job([TransferTask(1000000)])
job_2   = Job([TransferTask(2000000)])
job_3   = Job([TransferTask(3000000)])
job_5   = Job([TransferTask(5000000)])

jobqueue = JobQueue([job_1_1, job_1_2, job_2, job_3, job_5])


def test_storage():
    for cluster in clusters:
        cluster.match_jobs(jobqueue, 1)
    assert jobqueue.get_size() == 0

    for cluster in clusters:
        storage.add_request(cluster, cluster.try_step(time=1))
    storage.calculate_responses()
    network_requests = []
    for cluster in storage.response:
        network_requests.append(storage.response[cluster]['network'])
    network_requests.sort()
    assert network_requests == [1000000, 1000000, 2000000, 3000000, 3000000]


