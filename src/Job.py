from ResourceUsage import ResourceUsage

class Job():
    tasks = []
    current_task = 0
    current_request = None
    isDone = False

    def __init__(self, tasks=[]):
        self.tasks = tasks

    def try_step(self, time=1):
        if self.isDone:
            return ResourceUsage()
        usage_requests = self.tasks[self.current_task].try_step(time)
        self.current_request = usage_requests
        return usage_requests

    def do_step(self, usage_response=ResourceUsage()):
        if self.isDone:
            return True
        is_task_done = self.tasks[self.current_task].do_step(usage_response)
        if is_task_done:
            print('task is done')
            self.current_task += 1
            if self.current_task >= len(self.tasks):
                self.isDone = True
        return self.isDone

    def __repr__(self):
        return str({"current_task": self.current_task, "task": repr(self.tasks[self.current_task])})