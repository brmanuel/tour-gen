
from abc import ABC, abstractmethod

@ABC
class Tour:
    @abstractmethod
    def contains_tasks(self, task):
        """Check if the given task is included in this tour."""