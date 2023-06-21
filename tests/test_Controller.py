from Task import ComputingTask
from Task import TransferTask
from Job import Job
from Worknode import Worknode
from Cluster import Cluster
from Storage import Storage
from JobQueue import JobQueue
from Controller import Controller
import copy
import random


clusters = []
# for i in range(3):
#     worknode_base = Worknode(40, 24, 16000, 100000000)  # 1 GB
#     worknodes = [copy.deepcopy(worknode_base) for i in range(20)]
#
#     cluster_base = Cluster(worknodes, 1000000000, "Govorun", isAccounted=True)  # 10 GB
#     cluster_base.name = "Cluster" + str(i)
#     clusters.append(cluster_base)

# Tier
worknode_base = Worknode(24, 24, 16000, 1000000000)  # 10 GB
worknodes = [copy.deepcopy(worknode_base) for i in range(30)]
for i in range(15):
    worknodes.append(Worknode(12, 13, 16000, 1000000000))

cluster_base = Cluster(worknodes, 10000000000, "Tier", isAccounted=True)  # 100 GB
cluster_base.name = "Tier"
clusters.append(cluster_base)

worknode_base = Worknode(5, 24, 16000, 1000000000)
worknodes = [copy.deepcopy(worknode_base) for i in range(20)]
cluster_base = Cluster(worknodes, 10000000000, "LHEP", isAccounted=True)  # 100 GB
cluster_base.name = "LHEP"
clusters.append(cluster_base)

storage = Storage(10000000000)  # 10 GB


job_queue = JobQueue()

#for i in range(100):
    #job_base = Job([TransferTask(40000000), ComputingTask(1050000)])
    #multiplier = 1 + 4 * random.random()
    #job_base = Job([TransferTask(int(multiplier * 1000)), ComputingTask(int(multiplier * 1000))])
    #job_queue.add_job(job_base)

controller = Controller(clusters, storage, job_queue)

def test_controller_basic():

    controller.accounting.add_data("config", "start_time", 1)

    period = 30
    count = 0
    total_jobs = 0
    #job_queue.add_job(Job([TransferTask(40000000000), ComputingTask(1260000), TransferTask(1600000000), TransferTask(1600000), ComputingTask(1260000), TransferTask(1600000)]))
    #job_queue.add_job(Job([TransferTask(40000000000), ComputingTask(1260000), TransferTask(1600000000)]))
    for i in range(50):
        job_queue.add_job(Job([TransferTask(15000000000), ComputingTask(55000), TransferTask(800000000)]))
        total_jobs += 1

    while controller.is_busy():
        if count % 90 == 0:
            #job_queue.add_job(Job([TransferTask(40000000), ComputingTask(1260000), TransferTask(1600000), TransferTask(1600000), ComputingTask(1260000), TransferTask(1600000)]))
            if total_jobs < 5000:
                for i in range(50):
                    job_queue.add_job(Job([TransferTask(15000000000), ComputingTask(55000), TransferTask(800000000)]))
                    total_jobs =+ 1

        controller.do_step(time = period)
        count += period
        controller.accounting.add_data("system", "running_slots", controller.get_running_slots())

        for cluster in controller.clusters:
            controller.accounting.add_data("cpu", cluster.name, cluster.get_cpu_usage())
            controller.accounting.add_data("cpu_load", cluster.name, cluster.get_cpu_load())
            controller.accounting.add_data("network", cluster.name, cluster.get_network_usage())
        if count % 600 == 0:
            controller.accounting.write_data()

    controller.accounting.write_data()
