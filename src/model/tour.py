
from abc import ABC, abstractmethod

class Tour(ABC):
    @abstractmethod
    def get_tasks(self):
        """Returns the list of all tasks in this tour."""

    @abstractmethod
    def get_group(self):
        """Return the group where this tour is planned."""
