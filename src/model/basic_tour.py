from src.model.tour import Tour
from src.model.tour_factory import TourFactory

class BasicTour(Tour, TourFactory):
    def __init__(self, group, tasks):
        self._group = group
        self._tasks = tasks

    def get_tasks(self):
        return self._tasks

    @staticmethod
    def create(group, tasks):
        return BasicTour(group, tasks)
