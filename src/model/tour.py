
from abc import ABC, abstractmethod

class Tour(ABC):
    @abstractmethod
    def contains_tasks(self, task):
        """Check if the given task is included in this tour."""