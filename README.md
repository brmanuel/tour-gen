# tour-gen
Column generation approach to tour / shift creation

# Purpose
The purpose of this Repo is for me to experiment with column generation using an easy example.

# Approach
## Preliminaries
Consider the problem of creating work shifts for some company.
The company has a set of tasks $t \in T$ that need to be performed a set of employees.
We think of each task $t$ to have a fixed start- and end time and location.
A shift is a sequence of tasks $(t_1, \dots, t_n)$ that can be performed in this order by one employee.
Whether a sequence of task is a legal shift depends on two types of constraints:
- Local constraints: for each $i \in \{1, \dots, n-1\}$, the transition from $t_i$ to $t_{i+1}$ must be possible (enough time between the tasks, transition between end location of $t_i$ and the start location of $t_{i+1}$ possible etc.)
- Global constrains: the whole sequence must conform to labor rules such as maximal work time, break rules, etc.
Since the number of shifts corresponds to the number of employees that are required to perform all the tasks, a sensible goal is to find a minimum number of shifts that covers all tasks.

## Problem Formulation
Imagine for a moment that we can generate all possible legal shifts $P$.
In particular, for this example, $P$ contains all sequences $p$ of tasks respecting:
- The total duration of $p$ (i.e. end time of the last task minus the start time of the first task) is at most $D_\max$
- Continuous work time without a break does not exceed $D_\text{break}$
- The start location of the first task and the end location of the last task are the same (think of train drivers)
- All transitions between adjacent tasks are possible (space and time)

We could then formulate the following MILP problem:

$$
\begin{align}
\min &\sum_{p \in P} x_p \\
s.t. & \\
&\sum_{p \in P \land t \in p} x_p = 1 \qquad \forall \text{ tasks } t \\
&x_p \in \{0,1\}
\end{align}
$$

Every shift p has an associated choice-variable $x_p$ which is $1$ if shift $p$ is chosen and $0$ otherwise.
Then the above just means that we want to select the minimum number of shifts, such that every task occurs in exactly one selected shift.
We could of course extend the constraints and objective function in the above optimization problem.
Here we want to keep it as simple as possible.

The advantage of this approach is that the checking of tour-validity and the optimal selection of a set of tours are decoupled.
The disadvantage is that the size of set $P$ is usually prohibitively large.
Column generation to the rescue.

## Derivation of Algorithm
The idea of column generation is to work with a limited subset of all shifts $\tilde{P} \subset P$ and to add shifts to $\tilde{P}$ on demand.
Initially we start with a trivial set of shifts that allows covering all tasks: $\tilde{P}_0$ the set of shifts where every task is a separate shift.
We then solve the LP relaxation (drop the integrality constraint) of the above MILP problem (let's call it relaxed master problem RMP) using a standard LP solver.
Given the optimal solution to the RMP LP theory provides us with a way to find a shift $p \notin \tilde{P}_0$ that we should add to the pool of candidate shifts $\tilde{P}_1$ of the next iteration, in order to improve the objective.
Let's derive it first abstractly for a general LP problem:
Consider the general linear program

$$
\begin{align}
\min c^T \cdot x \\
s.t. & \\
&A \cdot x = b \\
&x \geq 0
\end{align}
$$

Where $A$ is an $n \times m$ matrix, meaning that there are $m$ variables and $n$ constraints.
Let $B$ be a set of $n$ columns of $A$.
We write $A_B$ to mean the $n \times n$ submatrix of these $n$ columns of $A$.
Similarly we write $x_B$ and $c_B$ to mean the subvectors of $x$ and $c$ corresponding to these columns.
It can be shown that every LP has an optimal solution $x^*$ 



## Column generation and LP theory resources

