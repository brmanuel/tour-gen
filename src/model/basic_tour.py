from src.model.tour import Tour
from src.model.tour_factory import TourFactory

class BasicTour(Tour, TourFactory):
    def __init__(self, group, tasks):
        self._group = group
        self._tasks = tasks

    def get_tasks(self):
        return self._tasks

    def get_group(self):
        return self._group

    def __hash__(self):
        hashstr = f"{self.get_group()}"
        for task in self.get_tasks():
            hashstr += f"~{task}"
        return hashstr.__hash__()
    
    @staticmethod
    def create(group, tasks):
        return BasicTour(group, tasks)
