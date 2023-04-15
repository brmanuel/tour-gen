
# Business Rules
Note, this is a toy project, thus the business rules are intentionally simple.
Moreover, some of the business rules are assumed to be presented to us with the input, i.e. it is pre-computed somehow.

## Input data format

```json
{
  "groups": [{
    "id": "String",
    "skills": [ "String" ], // skills possessed by all personnel in this group.
    "startNodeId": "String", // Tours for this group must start from the node startNodeId.
    "endNodeId": "String" // Tours for this group must end at the node endNodeId.
  }],
  "nodes": [
    "id": "String",
    "startTime": "Integer", // Start of activity in minutes since 1.1.1970.
    "endTime": "Integer", // End of activity in minutes since 1.1.1970.
    "requiredSkills": [ "String" ], // Skills required to perform this task.
    // Additional metainfo describing the task
    "type": "String", 
    "fromLocation": "String",
    "toLocation": "String"
  ],
  "arcs": [
    "sourceNodeId": "String",
    "targetNodeId": "String",
    "duration": "Integer", // Duration of transition in minutes.
    "isBreakPossible": "Boolean" // Indicates whether a break can be performed between source and dest Activity.
  ]
}
```

Additionally, a set of parameters control the solution:
- D_SHIFT: maximum duration of a shift
- D_BREAK: maximum duration of work without a break

## Rule set
It follows the set of rules for the optimization problem we are solving. Indicated next to each rule / objective is the way it is implemented.

- Minimize the total number of shifts (MILP objective)
- A shift is assigned to exactly one group. A shift of group X needs to start at the source node of X and end at the target node of X. (Candidate shift search in graph)
- Every task needs to be covered by exactly one shift from a group which has (at least) the required skill set of the task. (MILP constraint)
- Each shift needs to be a continuous path through the directed graph specified by the input, meaning that the shift is geographically feasible and temporally consistent. (Candidate shift search in graph)
- Shifts cannot be longer than D_SHIFT (Resources of nodes in graph)
- Continuous work time between breaks is at most D_SHIFT (Resources of nodes in graph)

## Implementation of business rules in graph

Design decision: We search candidate shifts by solving a resource constrained shortest path problem in a graph. Every shift-candidate is a path through the graph of tasks. Every task in the graph has an associated set of resources that represent "the different ways in which this task can be reached". In particular, a node can have many different sets of resources, corresponding to all possible ways of reaching it in the graph, i.e. conceptually for every path from the source node to node X, X has a set of resources "summarizing" this path. We consider the following resources:

- Group: this resource indicates group of employees covering the task. This resource is set initially with the choice of the group performing this shift and then stays constant along a path in the graph.
- Shift start: this resource indicates the start time of the first activity along the path.
- Continuous work time: this resource indicates the time of the last break, or the start time of the first activity along the path if there is no break.

