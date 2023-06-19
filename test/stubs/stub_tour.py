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
