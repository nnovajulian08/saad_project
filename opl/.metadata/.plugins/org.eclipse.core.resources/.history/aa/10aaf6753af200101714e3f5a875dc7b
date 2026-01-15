// ================================
// Job Shop Scheduling (JSP) - MIP (MILP) in OPL
// Big-M disjunctive constraints
// Objective: minimize makespan (Cmax)
// ================================

using CPLEX;

// ----------- DATA -----------
int nJobs = ...;
int nMachines = ...;

range Jobs = 1..nJobs;
range Ops  = 1..nMachines;   // operation index within each job

int machine[Jobs][Ops]  = ...;   // machine in 1..nMachines
int duration[Jobs][Ops] = ...;   // processing times

// A safe Big-M: sum of all processing times (upper bound on schedule length)
int M = sum(j in Jobs, k in Ops) duration[j][k];

// ----------- INDEX SET OF CONFLICTING PAIRS (same machine) -----------
// We create a set of pairs of operations (j1,k1) and (j2,k2)
// that require the SAME machine, and we only keep one direction (j1,k1) < (j2,k2)
// to avoid duplicates.
tuple Pair {
  int j1;
  int k1;
  int j2;
  int k2;
}

{Pair} Pairs =
  { <j1,k1,j2,k2> |
      j1 in Jobs, k1 in Ops,
      j2 in Jobs, k2 in Ops :
        // unique ordering to avoid duplicates
        (j1 < j2 || (j1 == j2 && k1 < k2)) &&
        // same machine => conflict
        machine[j1][k1] == machine[j2][k2]
  };

// ----------- DECISION VARIABLES -----------
// Start time for each operation (keep as int if your times are all integers)
dvar int+ start[Jobs][Ops];

dvar int+ Cmax;

// y[p] = 1 means (j1,k1) is scheduled BEFORE (j2,k2) on that machine
dvar boolean y[Pairs];

// ----------- OBJECTIVE -----------
minimize Cmax;

// ----------- CONSTRAINTS -----------
subject to {

  // 1) Precedence within each job: op k before op k+1
  forall(j in Jobs, k in 1..nMachines-1)
    start[j][k+1] >= start[j][k] + duration[j][k];

  // 2) Machine capacity (disjunctive constraints)
  // For any two operations that use the same machine:
  // either A finishes before B starts OR B finishes before A starts.
  forall(p in Pairs) {
    // A before B
    start[p.j1][p.k1] + duration[p.j1][p.k1]
      <= start[p.j2][p.k2] + M*(1 - y[p]);

    // B before A
    start[p.j2][p.k2] + duration[p.j2][p.k2]
      <= start[p.j1][p.k1] + M*(y[p]);
  }

  // 3) Makespan definition: Cmax >= end of every operation
  forall(j in Jobs, k in Ops)
    Cmax >= start[j][k] + duration[j][k];
}

