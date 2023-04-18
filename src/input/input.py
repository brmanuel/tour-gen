from abc import ABC, abstractmethod

@ABC
class Input:
    @abstractmethod
    def get_edges_between(self, left_task, right_task):
        """Get the set of transitions from left_task to right_task.
        If no transition exists, the empty set is returned."""

    @abstractmethod    
    def get_source_edges(self, group, task):
        """Get the set of transitions from source_depot of group to task.
        If no transition exists, the empty set is returned."""

    @abstractmethod
    def get_target_edges(self, task, group):
        """Get the set of transitions from task to target_depot of group.
        If no transition exists, the empty set is returned."""

    @abstractmethod
    def get_tasks_for_group(self, group):
        """Returns the set of all tasks that can be performed by group 
        (depending on skills)."""

    @abstractmethod
    def get_groups(self):
        """Returns the set of all groups in this input."""

    @abstractmethod
    def propagate_resources(self, left_resources, edge):
        """Compute the resources resulting from following edge when starting
        in a vertex with left_resources."""

    @abstractmethod
    def are_resources_valid(self, resources):
        """Check if a node with <resources> is valid w.r.t. the business rules."""

    @abstractmethod
    @staticmethod
    def get_start_time_of_task(task):
        """Returns the starttime of the task in minutes after 1.1.1970."""
