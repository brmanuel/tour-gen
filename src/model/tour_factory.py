
from abc import ABC, abstractmethod

class TourFactory(ABC):
    @staticmethod
    @abstractmethod
    def create(group, tasks):
        """Returns a Tour."""
