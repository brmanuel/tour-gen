from abc import ABC, abstractmethod

class Input(ABC):
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
    def get_tasks(self):
        """Returns the set of all tasks."""

    @abstractmethod
    def get_groups(self):
        """Returns the set of all groups in this input."""

    @abstractmethod
    def get_depot_resources(self, group):
        """Returns the resources at the start of the shift."""

    @abstractmethod
    def propagate_resources(self, left_resources, edge):
        """Compute the resources resulting from following edge when starting
        in a vertex with left_resources."""

    @abstractmethod
    def are_resources_valid_at_task(self, resources, task):
        """Check if a node with <task> and <resources> is valid w.r.t. the business rules."""

    @abstractmethod
    def are_resources_valid_at_edge(self, resources, edge):
        """Check if transitioning over <edge> given the <resources> is valid w.r.t. the business rules."""

    @staticmethod
    @abstractmethod
    def get_start_time_of_task(task):
        """Returns the starttime of the task in minutes after 1.1.1970."""
