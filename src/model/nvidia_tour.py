

class NvidiaTour(Tour):
    def __init__(self, group, tasks):
        self._group = group
        self._tasks = tasks

    def contains_task(self, task):
        return task in self._tasks
