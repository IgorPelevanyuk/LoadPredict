from ResourceUsage import ResourceUsage
from Task import ComputingTask
from Task import TransferTask
from Job import Job
from Worknode import Worknode
from Cluster import Cluster
from JobQueue import JobQueue
import copy

cluster = None

worknode = Worknode(2, 10, 16000, 1000000)
worknodes = [copy.deepcopy(worknode) for i in range(10)]

task1 = ComputingTask(100)
task2 = TransferTask(1000000)
default_job = Job([task1, task2])

jobqueue = JobQueue([copy.deepcopy(default_job) for i in range(100)])

def test_cluster_create():
    global cluster
    cluster = Cluster(worknodes, 1000000)

def test_cluster_match_jobs():
    assert jobqueue.get_size() == 100
    free_slots = 0
    for worknode in cluster.worknodes:
        free_slots += worknode.get_available_slots()
    assert free_slots == 20
    cluster.match_jobs(jobqueue)
    free_slots = 0
    for worknode in cluster.worknodes:
        free_slots += worknode.get_available_slots()
    assert free_slots == 0
    assert jobqueue.get_size() == 80

def test_cluster_do_step():
    iterations = 0
    while not (jobqueue.get_size() == 0 and cluster.get_available_slots() ==20):
        free_slots = cluster.get_available_slots()
        queue_size = jobqueue.get_size()
        if iterations == 119:
            x = 1
            pass
        request = cluster.try_step(time=1)
        cluster.do_step(time=1, usage_response = request)
        if cluster.get_available_slots() != 0:
            cluster.match_jobs(jobqueue)
        free_slots = cluster.get_available_slots()
        queue_size = jobqueue.get_size()
        iterations += 1
    assert iterations == 150
