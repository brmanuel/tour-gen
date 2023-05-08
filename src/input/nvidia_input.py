from functools import cache, cached_property
import json

from src.input.input import Input


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
        
    
    def _get_edges_between_nodes(self, left_node, right_node):
        edge = self._edge_map.get((left_node["id"], right_node["id"]))
        if edge is None:
            return set()
        return set([edge])
    
    def get_edges_between(self, left_task, right_task):
        return self._get_edges_between_nodes(left_task, right_task)
    
    def get_source_edges(self, group, task):
        source_node_id = group["sourceNodeId"]
        source_node = self._node_map[source_node_id]
        return self._get_edges_between_nodes(source_node, task)
    
    def get_target_edges(self, task, group):
        target_node_id = group["targetNodeId"]
        target_node = self._node_map[target_node_id]
        return self._get_edges_between_nodes(task, target_node)
    
    @staticmethod
    def _is_depot_node(node):
        return node["type"] in [SOURCE_DEPOT, TARGET_DEPOT]
    
    @cached_property
    def _tasks(self):
        return set(
            node for node in self._node_map.values()
            if not NvidiaInput._is_depot_node(node)
        )
    
    @staticmethod
    def _has_group_skills_for_task(group, task):
        return set(task["requiredSkills"]) <= set(group["skills"])

    @cache
    def get_tasks_for_group(self, group):
        all_tasks = self._tasks
        return set(
            task for task in all_tasks
            if NvidiaInput._has_group_skills_for_task(group, task)
        )
        
    
    @cache
    def get_groups(self):
        return set(self._group_map.values())
    
    def get_start_time_of_task(self, task):
        return task["startTime"]

    
    def get_depot_resources(self, group):
        return {"group": group["id"], "shift_start": None, "last_break": None}

    def _get_target_of_edge(self, edge):
        return self._node_map[edge[1]]

    def _get_source_of_edge(self, edge):
        return self._node_map[edge[0]]

    def propagate_resources(self, left_resources, edge):
        target = _get_target_of_edge(edge)
        arc = self._edge_map[edge]

        left_group = left_resources["group"]
        left_shift_start = left_resources["shift_start"]
        left_last_break = left_resources["last_break"]

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

        return {"group": right_group, "shift_start": right_shift_start, "last_break": right_last_break}

    def _are_resources_valid_at_time(self, resources, time):
        return time - resources["shift_start"] <= D_SHIFT and time - resources["last_break"] <= D_BREAK

    def are_resources_valid_at_task(self, resources, task):
        return _are_resources_valid_at_time(resources, task["endTime"])

    def are_resources_valid_at_edge(self, resources, edge):
        arc = self._edge_map[edge]
        source = self._node_map[arc["sourceNodeId"]]
        return _are_resources_valid_at_time(resources, source["endTime"] + arc["duration"])