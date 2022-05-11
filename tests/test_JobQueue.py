from Job import Job
from JobQueue import JobQueue
from Task import ComputingTask, TransferTask
import copy

task1 = ComputingTask(20)
task2 = TransferTask(1000000)
default_job = Job([task1, task2])

jobqueue = None

def test_job_queue_create():
    global jobqueue
    jobqueue = JobQueue([copy.deepcopy(default_job) for i in range(10)])
    assert jobqueue.get_size() == 10

def test_job_queue_get_1():
    for i in range(5):
        job = jobqueue.pop_job()
    assert jobqueue.get_size() == 5

def test_job_queue_get_2():
    for i in range(5):
        job = jobqueue.pop_job()
    assert jobqueue.get_size() == 0

def test_job_queue_get_empty():
    assert jobqueue.pop_job() == None

def test_job_add_job():
    jobqueue.add_job(copy.deepcopy(default_job))
    assert jobqueue.get_size() == 1

