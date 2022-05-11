class JobQueue():
    jobs = []

    def __init__(self, jobs):
        self.jobs = jobs

    def pop_job(self):
        if len(self.jobs) > 0:
            return self.jobs.pop()
        else:
            return None

    def add_job(self, job):
        self.jobs.append(job)

    def get_size(self):
        return len(self.jobs)