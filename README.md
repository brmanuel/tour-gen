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

### Abstract Column Generation
Consider the general linear program

$$
\begin{align}
\min\ &c^T \cdot x \\
s.t. & \\
&A \cdot x = b \\
&x \geq 0
\end{align}
$$

Where $A$ is an $n \times m$ matrix, meaning that there are $m$ variables and $n$ constraints.
Let $B$ be a set of $n$ columns of $A$ and $N := \{ 1,\dots,m \} \setminus B$ the remaining columns.
We write $A_B$ to mean the $n \times n$ submatrix of these $n$ columns of $A$.
Similarly we write $x_B$ and $c_B$ to mean the subvectors of $x$ and $c$ corresponding to these columns.
If the columns of $A_B$ are linearly independent, then $A_B$ is a basis of $\mathbb{R}^n$ and the value of $x_B$ can be computed from
$$\left[A_B, A_N\right] \cdot \left[x_B \atop x_N\right] = b$$
as
$$x_B = A_B^{-1} \cdot (b - A_N x_N)$$
The solution $x_B$ obtained from this expression by setting $x_N$ to zero is called the basic solution of basis $B$.
It can be shown that every LP for which an optimal solution exists, there exists a basic solution $x_B$ obtaining the optimal objective value.

Given some basic solution $x_B$ we can check whether it is optimal by expressing the objective function at $x_B$ in terms of the non-basic variables (using the above expression for $x_B$:

$$
c^T \cdot x = \left[c_B, c_N\right] \cdot \left[x_B \atop x_N\right] = c_B^T \cdot A_B^{-1} b - c_B^T \cdot A_B^{-1} A_N x_N + c_N \cdot x_N
$$

The coefficient of the non-basic variable $x_j$ in this expression is

$$
d_j := -c_B^T \cdot A_B^{-1} A_j + c_j
$$

$d_j$ is referred to as the reduced cost of non-basic variable $x_j$ at basis $B$.
If $d_j$ is negative, increasing $x_j$ slightly will decrease the objective, if $d_j$ is positive, increasing $x_j$ slightly will increase the objective.
In a minimization problem, basic solution $x_B$ is thus optimal, if all non-basic variables have positive reduced cost.

In column generation, we use the expression for the reduced cost, to check if there are additional candidate variables (shifts, in our case), that are currently outside of the pool of variables $\tilde{P}$, that could be added in order to improve the objective.
For this we need a way of computing the shift-candidate with the smallest reduced cost.
If this reduced cost is positive, we know that the current solution is already optimal, otherwise we add the shift to $\tilde{P}_{i+1}$ and re-solve the LP.

The expression we need to minimize is a bit unwieldy.
LP duality theory provides us with a nice way to avoid having to compute matrix inverses.
The following LP is called the dual of the above generic LP (we call it the primal):

$$
\begin{align}
\max\ &b^T \cdot y \\
s.t. & \\
&A^T \cdot y + w = c \\
&w \geq 0
\end{align}
$$

Duality theory provides many interesting results about the relationship between an LP and its dual.
Here we need the following two facts:
- Complementary slackness / KKT conditions: If $x$ is the optimal solution of the primal and $y$, $w$ is the optimal solution of the dual, then holds $x^T \cdot w = 0$
- Given an optimal solution to the primal, we can easily get an optimal solution to the dual. In particular, standard solvers allow accessing the dual solution after having computed the optimal primal solution.

Using the definition of the dual above and the first fact, we can simplify the expression for $d_j$:

Let $B$ be the optimal basis of the primal and let $y,w$ be optimal dual variables.
Then holds 
$$A^T \cdot y + w = c$$ 
because $y,w$ are feasible. Only considering the rows $B$ of $A$, $w$ and $c$ this means 
$$A_B^T \cdot y + w_B = c_B$$
Assuming non-degeneracy and from the first fact above we know that $w_B = 0$, so we get 
$$A_B^T \cdot y = c_B$$
By multiplying $A_B^{-T}$ (the transpose of $A_B^{-1}$) from the left we get 
$$A_B^{-T} (A_B^T \cdot y) = A_B^{-T} \cdot c_B$$
Which reduces to 
$$y = c_B^T \cdot A_B^{-1}$$

Thus we get the simpler expression for the reduced cost of non-basic variable $x_j$
$$d_j = y^T \cdot A_j + c_j$$
where $y$ is the vector of optimal dual variables.

### Column generation for shift planning

## Column generation and LP theory resources

