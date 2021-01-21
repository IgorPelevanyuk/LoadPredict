from ResourceUsage import ResourceUsage
from Task import ComputingTask
from Task import TransferTask


def test_computing_task_1():
    task = ComputingTask(1000)
    request = task.try_step()
    expected_request = ResourceUsage({'cpu_usage': 1000})
    assert request == expected_request


def test_computing_task_2():
    task = ComputingTask(1000)
    is_done = task.do_step(ResourceUsage({'cpu_usage': 20}))
    assert is_done is False
    assert task.computed == 20


def test_computing_task_3():
    task = ComputingTask(20)
    step_1 = task.do_step(ResourceUsage({'cpu_usage': 10}))
    step_2 = task.do_step(ResourceUsage({'cpu_usage': 10}))
    assert step_1 is False
    assert step_2 is True


def test_transfer_task_1():
    task = TransferTask(1000000)
    request = task.try_step()
    expected_request = ResourceUsage({'network': 1000000})
    assert request == expected_request


def test_transfer_task_2():
    task = TransferTask(1000000)
    is_done = task.do_step(ResourceUsage({'network': 500000}))
    assert is_done is False
    assert task.transferred == 500000
    is_done = task.do_step(ResourceUsage({'network': 500000}))
    assert is_done is True


def test_transfer_task_3():
    task = TransferTask(1000000)
    is_done = task.do_step(ResourceUsage({'cpu_usage': 10}))
    request = task.try_step()
    expected_request = ResourceUsage({'network': 1000000})
    assert request == expected_request

