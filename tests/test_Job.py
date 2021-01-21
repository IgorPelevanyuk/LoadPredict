from ResourceUsage import ResourceUsage
from Task import ComputingTask
from Task import TransferTask
from Job import Job

def test_job_complex_1():
    task1 = ComputingTask(20)
    task2 = TransferTask(1000000)
    job = Job([task1, task2])
    request1 = job.try_step()
    assert request1 == ResourceUsage({'cpu_usage': 20})
    result = job.do_step(usage_response=ResourceUsage({'cpu_usage': 20}))
    assert result is False
    request2 = job.try_step()
    assert request2 == ResourceUsage({'network': 1000000})
    result = job.do_step(usage_response=ResourceUsage({'network': 1000000}))
    assert result is True
    request3 = job.try_step()
    assert request3 == ResourceUsage()

