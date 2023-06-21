import json
from typing import Set

from src.model.solution import Solution
from src.model.tour import Tour
from src.input.nvidia_input import NvidiaInput

class NvidiaSolution(Solution):
    def __init__(self, tours : Set[Tour], input_file):
        self._tours = tours
        
        with open(input_file, "r", encoding="cp1252") as f:
            input = json.load(f)
        
        self._group_id_to_group = {
            gr["id"] : gr for gr in input["groups"]
        }
        self._node_id_to_node = {
            node["id"] : node for node in input["nodes"]
        }
        solution_group_map = {}
        for tour in self._tours:
            group_id = tour.get_group()
            if group_id not in solution_group_map:
                group = self._group_id_to_group[group_id]
                group["crewDiagrams"] = []
                solution_group_map[group_id] = group
            crewDiagram = [
                self._node_id_to_node[task_id]
                for task_id in tour.get_tasks()
            ]
            solution_group_map[group_id]["crewDiagrams"].append(crewDiagram)
        self._solution = list(solution_group_map.values())

    def get_solution(self):
        return self._solution

    def write(self, filename):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self._solution, f, indent=4)
                

        
        
