from functools import cache, cached_property
import json


class NvidiaInput(input):

    SOURCE_DEPOT = "source-Depot"
    TARGET_DEPOT = "target-Depot"

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
        return 
    
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
        return set(self._group_map.values)
    
    def get_start_time_of_task(self, task):
        return task["startTime"]