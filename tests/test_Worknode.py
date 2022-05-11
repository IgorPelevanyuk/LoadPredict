from ResourceUsage import ResourceUsage
from Task import ComputingTask
from Task import TransferTask
from Job import Job
from Worknode import Worknode

job1 = Job([
    TransferTask(1000000),
    ComputingTask(20),
    TransferTask(500000)
])

job2 = Job([
    TransferTask(500000),
    ComputingTask(100),
    TransferTask(500000)
])

job3 = Job([
    ComputingTask(200)
])

job4 = Job([
    TransferTask(10000000)
])

def test_worknode_complex():
    wn = Worknode(4, 10, 16000, 2000000)
    wn.submit_job(job1)
    wn.submit_job(job2)
    wn.submit_job(job3)
    wn.submit_job(job4)
    request1 = wn.try_step(time=1)
    assert request1 == ResourceUsage({'network': 2000000})
    wn.do_step(time=1, usage_response=request1)
    assert wn.jobs[0].current_task == 0
    assert wn.jobs[1].current_task == 1

    request2 = wn.try_step(time=1)
    wn.do_step(time=1, usage_response=request2)

    request3 = wn.try_step(time=1)
    wn.do_step(time=1, usage_response=request3)
    assert wn.jobs[0].current_task == 1
    assert wn.jobs[1].current_task == 1

def test_worknode_available_slots():
    wn = Worknode(4, 10, 16000, 2000000)
    assert wn.get_available_slots() == 4
    wn.submit_job(job1)
    wn.submit_job(job2)
    assert wn.get_available_slots() == 2
    wn.submit_job(job3)
    assert wn.get_available_slots() == 1
    for i in range(100):
        request = wn.try_step(time=1)
        wn.do_step(time=1, usage_response=request)
    assert wn.get_available_slots() == 4
