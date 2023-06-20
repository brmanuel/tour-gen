from functools import cache, cached_property
import json
from typing import Set
from dataclasses import dataclass

from src.input.input import Input

@dataclass(frozen=True)
class NvidiaResource():
    group : str,
    shift_start : int,
    last_break : int
    

class NvidiaInput(Input):

    SOURCE_DEPOT = "source-Depot"
    TARGET_DEPOT = "target-Depot"
    D_SHIFT = 600 # at most 10h shifts
    D_BREAK = 270 # at most 4.5h without break

    def __init__(self, data):
        self._group_map = {
            group["id"]: group
            for group in data["groups"]
        }
        self._node_map = {
            node["id"]: node 
            for node in data["nodes"]
        }
        self._edge_map = {
            (edge["sourceNodeId"], edge["targetNodeId"]): edge
            for edge in data["arcs"]
        }

    @staticmethod
    def from_file(filename):
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            return NvidiaInput(data)
        
    
    def _get_edges_between_nodes(self, left_node_id, right_node_id):
        edge_key = (left_node_id, right_node_id)
        if edge_key not in self._edge_map:
            return set()
        return set([edge_key])
    
    def get_edges_between(self, left_task_id, right_task_id):
        return self._get_edges_between_nodes(left_task_id, right_task_id)
    
    def get_source_edges(self, group_id, task_id):
        group = self._group_map[group_id]
        source_node_id = group["startNodeId"]
        return self._get_edges_between_nodes(source_node_id, task_id)
    
    def get_target_edges(self, task_id, group_id):
        group = self._group_map[group_id]
        target_node_id = group.get("endNodeId")
        return self._get_edges_between_nodes(task_id, target_node_id)
    
    @staticmethod
    def _is_depot_node(node):
        return node["type"] in [
            NvidiaInput.SOURCE_DEPOT, NvidiaInput.TARGET_DEPOT
        ]
    
    @cached_property
    def _tasks(self):
        return {
            node["id"]: node
            for node in self._node_map.values()
            if not NvidiaInput._is_depot_node(node)
        }
    
    def _has_group_skills_for_task(self, group_id, task):
        group = self._group_map[group_id]
        return set(task["requiredSkills"]) <= set(group["skills"])

    @cache
    def get_tasks_for_group(self, group_id) -> Set[str]:
        all_tasks = self._tasks
        return set(
            task_id for task_id, task in all_tasks.items()
            if self._has_group_skills_for_task(group_id, task)
        )

    def get_tasks(self) -> Set[str]:
        return self._tasks
    
    @cache
    def get_groups(self) -> Set[str]:
        return set(self._group_map.keys())
    
    def get_start_time_of_task(self, task_id):
        task = self._node_map[task_id]
        return task["startTime"]
    
    def get_depot_resources(self, group_id):
        group = self._group_map[group_id]
        return NvidiaResource(group["id"], None, None)

    def _get_target_of_edge(self, edge):
        return self._node_map[edge["targetNodeId"]]

    def propagate_resources(self, left_resources, edge_id):
        arc = self._edge_map[edge_id]
        target = self._get_target_of_edge(arc)

        left_group = left_resources.group
        left_shift_start = left_resources.shift_start
        left_last_break = left_resources.last_break

        right_group = left_group

        if left_shift_start is not None:
            right_shift_start = left_shift_start 
        else:
            # shift starts with the target node
            right_shift_start = target["startTime"] - arc["duration"]

        if arc["isBreakPossible"]:
            # do break on edge
            right_last_break = target["startTime"]
        elif left_last_break is None:
            # shift starts with target node
            right_last_break = target["startTime"]
        else:
            # no change of break since last task
            right_last_break = left_last_break

        return NvidiaResource(right_group, right_shift_start, right_last_break}

    @staticmethod
    def _are_resources_valid_at_time(resources : NvidiaResource, time):
        if resources.shift_start is None and resources.last_break is None:
            # resources at depot start
            return True
        return time - resources.shift_start <= NvidiaInput.D_SHIFT and time - resources.last_break <= NvidiaInput.D_BREAK

    def are_resources_valid_at_task(self, resources : NvidiaResource, task_id):
        task = self._node_map[task_id]
        return NvidiaInput._are_resources_valid_at_time(resources, task["endTime"])

    def are_resources_valid_at_edge(self, resources : NvidiaResource, edge_id):
        arc = self._edge_map[edge_id]
        source = self._node_map[arc["sourceNodeId"]]
        return NvidiaInput._are_resources_valid_at_time(resources, source["endTime"] + arc["duration"])
