# Job Shop Scheduling: MIP vs CP Comparison

This project studies the **Job Shop Scheduling Problem (JSP)** using two different
optimization models implemented in **IBM ILOG CPLEX Optimization Studio**:

- **Mixed-Integer Programming (MIP)** with Big-M disjunctive constraints  
- **Constraint Programming (CP)** with interval variables and global constraints  

The objective is to **minimize the makespan** and compare the performance,
modeling complexity, and solver behavior of both approaches on benchmark
instances.

---

## Problem Description

The Job Shop Scheduling Problem consists of:
- A set of jobs, each composed of a fixed sequence of operations
- A set of machines, where each operation requires exactly one machine
- No machine can process more than one operation at a time
- Operations within a job must respect precedence constraints. Meaning operation 1 must occur before operation 2

The goal is to find a feasible schedule that **minimizes the makespan**
(total time to complete all jobs).

---

## Modeling Approaches

### Mixed-Integer Programming (MIP)
- Start-time formulation
- Binary sequencing variables for conflicting operations
- Big-M linearization for machine disjunctions
- Solved using **CPLEX MIP Solver**

### Constraint Programming (CP)
- Interval variables for operations
- Global constraints:
  - `endBeforeStart` for job precedence
  - `noOverlap` for machine capacity
- Solved using **CP Optimizer**

---

## Project Structure

```
├── main.tex # LaTeX report
├── results/
│ ├── ft06_schedule_MIP.csv
│ ├── ft06_schedule_CP.csv
├── gantt_ft06_CP.png
├── kpi_ft06_makespan.png
├── kpi_ft06_solve_time.png
├── kpi_ft06_model_size.png
├── models/
│ ├── jsp_mip.mod # MIP model (OPL)
│ ├── jsp_cp.mod # CP model (OPL)
├── data/
│ └── ft06.dat # Benchmark instance
└── README.md

```

---

##  Experimental Setup

- **Benchmark**: Fisher and Thompson datasets (`ft06` and `ft10`)
- **Solvers**:
  - CPLEX MIP Solver
  - CP Optimizer
- **KPIs evaluated**:
  - Optimal makespan
  - Total solve time
  - Time to first feasible solution
  - Search effort (nodes / branches)
- **Visualization**:
  - Gantt charts generated from solver output
  - KPI plots for performance comparison

---
### Note on MIP Scalability (ft10)

The MIP formulation could not be executed for the `ft10` instance using the
CPLEX Community Edition due to model size limitations
(`CPLEX Error 1016: Problem size limits exceeded`).  
The Big-M MIP model introduces binary sequencing variables and disjunctive
constraints for each pair of conflicting operations, causing the model size to
grow rapidly with the instance size.

In contrast, the CP formulation remains solvable for `ft10` thanks to its use of
interval variables and global constraints (`noOverlap`), which provide a more
compact representation and better scalability under limited solver resources.

---
## Key Results (ft06)

| Metric | MIP | CP |
|------|-----|----|
| Makespan | 61 | 61 |
| Solve Time (s) | 0.23 | 0.07 |
| Time to First Feasible (s) | 0.11 | 0.06 |
| Nodes / Branches | 184 | 140,983 |

**Observation:**  
Both approaches reach the optimal solution. CP converges faster and finds feasible
solutions earlier, while MIP explores a smaller search tree but incurs higher
modeling and branching overhead.

---

## Schedule Visualization

The project includes **Gantt charts** illustrating the machine schedule over time. These
confirm:
- No machine conflicts
- Correct job precedence
- Efficient utilization of resources

---

## Requirements

- IBM ILOG CPLEX Optimization Studio
- Python (for KPI plots and Gantt chart generation)
  - `pandas`
  - `matplotlib`
  - `seaborn`
- LaTeX (Overleaf compatible)

---

## How to Run

1. Open the `.mod` and `.dat` files in **CPLEX Studio**
2. Solve using:
   - MIP model with CPLEX
   - CP model with CP Optimizer
3. Export schedules to CSV
4. Generate gantt charts using Python script (gantt.py): 
   - Change the `instance` and `method` variable values as desired.
5. Generate KPI plots using Python script (kpis.py)

---

## References

- https://github.com/tamy0612/JSPLIB
- IBM ILOG CPLEX Optimization Studio Documentation

---

## Authors

**[Julian Nunez Nova, Kirill Savin, Tamzim Hossain]**  
Job Shop Scheduling — Optimization Methods Comparison  
Academic / Course Project
