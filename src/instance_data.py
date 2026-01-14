from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Tuple

# reuse JSPInstance from your parser.py

Op = Tuple[int, int]  # (job j, op index k)

@dataclass(frozen=True)
class JSPModelData:
    name: str
    n_jobs: int
    n_machines: int
    ops: List[Op]                              # all operations (j,k)
    machine_of: Dict[Op, int]                  # machine_of[(j,k)] = m
    ptime: Dict[Op, int]                       # ptime[(j,k)] = processing time
    job_succ: Dict[Op, Op]                     # successor op in same job (if any)
    ops_on_machine: Dict[int, List[Op]]        # ops_on_machine[m] = list of operations
    horizon: int                               # sum of all processing times (safe Big-M)


def build_model_data(inst) -> JSPModelData:
    ops: List[Op] = []
    machine_of: Dict[Op, int] = {}
    ptime: Dict[Op, int] = {}
    job_succ: Dict[Op, Op] = {}
    ops_on_machine: Dict[int, List[Op]] = {m: [] for m in range(inst.n_machines)}

    horizon = 0

    for j in range(inst.n_jobs):
        for k in range(inst.n_machines):
            op: Op = (j, k)
            m, p = inst.jobs[j][k]
            ops.append(op)
            machine_of[op] = m
            ptime[op] = p
            ops_on_machine[m].append(op)
            horizon += p

            # job precedence: (j,k) -> (j,k+1)
            if k < inst.n_machines - 1:
                job_succ[op] = (j, k + 1)

    return JSPModelData(
        name=inst.name,
        n_jobs=inst.n_jobs,
        n_machines=inst.n_machines,
        ops=ops,
        machine_of=machine_of,
        ptime=ptime,
        job_succ=job_succ,
        ops_on_machine=ops_on_machine,
        horizon=horizon,
    )
