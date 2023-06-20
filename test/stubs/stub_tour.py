from src.model.tour import Tour
from src.model.tour_factory import TourFactory
from typing import List

class StubTour(Tour, TourFactory):
    def __init__(self, tasks : List["Task"]):
        self._tasks = tuple(tasks)
        
    def get_tasks(self):
        return self._tasks

    @staticmethod
    def create(group, tasks):
        return StubTour(tasks)

    def __eq__(self, other):
        if not isinstance(other, StubTour):
            return False
        return self.get_tasks() == other.get_tasks()

    def __hash__(self):
        return hash(self.get_tasks)
