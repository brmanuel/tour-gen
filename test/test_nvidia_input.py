import pytest
from src.algorithm.prizing import Prizing
from src.input.nvidia_input import NvidiaInput


small_input = NvidiaInput.from_file("input_data/small_graph.json")

def test_get_edges_between():
    left_task = "Q723688_11_1787923452"
    right_task = "Q723688_11_1787923557"
    edges = small_input.get_edges_between(left_task, right_task)
    assert len(edges) == 1


def test_get_source_edges():
    group = "OL~Gruppe 1~Kondukteur"
    task = "Q723688_11_1787923452"
    edges = small_input.get_source_edges(group, task)
    assert len(edges) == 1
    

def test_get_target_edges():
    task = "Q723688_11_1787923557"
    group = "OL~Gruppe 1~Kondukteur"
    edges = small_input.get_target_edges(task, group)
    assert len(edges) == 1

def test_get_tasks_for_group():
    group = "OL~Gruppe 1~Kondukteur"
    tasks = small_input.get_tasks_for_group(group)
    assert len(tasks) == 5


def test_get_groups():
    groups = small_input.get_groups()
    assert len(groups) == 2

def test_get_depot_resources():
    group = "OL~Gruppe 1~Kondukteur"
    task = "Q723688_11_1787923557"
    resources = small_input.get_depot_resources(group)
    assert small_input.are_resources_valid_at_task(resources, task)

def test_propagate_resources_no_break():
    left_task = "Q723688_11_1787923557"
    right_task = "Q723688_11_1787923517"
    edges = small_input.get_edges_between(left_task, right_task)
    assert len(edges) == 1
    edge = edges.pop()
    left_resources = {
        "group": "OL~Gruppe 1~Kondukteur",
        "shift_start": 50,
        "last_break": 100
    }
    right_resources = small_input.propagate_resources(left_resources, edge)
    assert right_resources["group"] == left_resources["group"]
    assert right_resources["shift_start"] == left_resources["shift_start"]
    assert right_resources["last_break"] == left_resources["last_break"]

      
def test_propagate_resources_with_break():
    left_task = "Q723688_11_1787923452"
    right_task = "Q723688_11_1787923557"
    edges = small_input.get_edges_between(left_task, right_task)
    assert len(edges) == 1
    edge = edges.pop()
    left_resources = {
        "group": "OL~Gruppe 1~Kondukteur",
        "shift_start": 50,
        "last_break": 100
    }
    right_resources = small_input.propagate_resources(left_resources, edge)
    right_task_start = small_input.get_start_time_of_task(right_task)
    assert right_resources["group"] == left_resources["group"]
    assert right_resources["shift_start"] == left_resources["shift_start"]
    assert right_resources["last_break"] == right_task_start
