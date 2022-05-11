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

jobqueue = JobQueue([copy.deepcopy(default_job) for i in range(500)])

def test_cluster_create():
    global cluster
    cluster = Cluster(worknodes, 1000000)

def test_cluster_match_jobs():
    cluster.match_jobs(jobqueue)

