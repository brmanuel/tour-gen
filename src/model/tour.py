
from abc import ABC, abstractmethod

class Tour(ABC):
    @abstractmethod
    def get_tasks(self):
        """Returns the list of all tasks in this tour."""
