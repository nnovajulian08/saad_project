from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple


# ----------------------------
# Data structures
# ----------------------------
Op = Tuple[int, int]  # (job j, operation index k)


@dataclass(frozen=True)
class JSPModelData:
    name: str
    n_jobs: int
    n_machines: int
    jobs: List[List[Tuple[int, int]]]          # jobs[j] = [(machine, ptime), ...]
    ops: List[Op]                              # all operations (j,k)
    machine_of: Dict[Op, int]                  # machine_of[(j,k)] = m
    ptime: Dict[Op, int]                       # ptime[(j,k)] = processing time
    job_succ: Dict[Op, Op]                     # successor op in same job
    ops_on_machine: Dict[int, List[Op]]        # ops_on_machine[m] = list of ops
    horizon: int                               # sum of all ptimes (safe Big-M)


# ----------------------------
# Parser
# ----------------------------
def read_jsplib_instance(path: str | Path) -> JSPModelData:
    """
    Parse a JSPLIB/ORLIB Job Shop instance file.

    Expected format (ignoring comment lines starting with '#'):
      n m
      <n lines> each with 2*m integers: machine time machine time ...

    Machine ids can be 0-based (0..m-1) or 1-based (1..m). We auto-detect and normalize to 0-based.
    """
    path = Path(path)

    # 1) Read non-empty, non-comment lines
    lines: List[str] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        s = raw.strip()
        if not s or s.startswith("#"):
            continue
        lines.append(s)

    if len(lines) < 2:
        raise ValueError(f"{path}: not enough data after removing comments.")

    # 2) Dimensions
    n_jobs, n_machines = map(int, lines[0].split())
    if n_jobs <= 0 or n_machines <= 0:
        raise ValueError(f"{path}: invalid dimensions n={n_jobs}, m={n_machines}")

    if len(lines) < 1 + n_jobs:
        raise ValueError(f"{path}: expected {n_jobs} job lines, got {len(lines)-1}")

    # 3) Parse raw tokens for each job
    parsed_rows: List[List[int]] = []
    all_machine_ids: List[int] = []

    for j in range(n_jobs):
        tokens = list(map(int, lines[1 + j].split()))
        if len(tokens) != 2 * n_machines:
            raise ValueError(
                f"{path}: job {j} line has {len(tokens)} ints; expected {2*n_machines}"
            )
        parsed_rows.append(tokens)
        all_machine_ids.extend(tokens[0::2])

    # 4) Auto-detect indexing
    min_id, max_id = min(all_machine_ids), max(all_machine_ids)
    if min_id == 0 and max_id == n_machines - 1:
        one_based = False
    elif min_id == 1 and max_id == n_machines:
        one_based = True
    else:
        raise ValueError(
            f"{path}: cannot auto-detect machine indexing. "
            f"Observed machine ids in [{min_id}, {max_id}] but expected either "
            f"[0, {n_machines-1}] (0-based) or [1, {n_machines}] (1-based)."
        )

    # 5) Build jobs list normalized to 0-based machines
    jobs: List[List[Tuple[int, int]]] = []
    for j in range(n_jobs):
        tokens = parsed_rows[j]
        ops_for_job: List[Tuple[int, int]] = []
        for k in range(n_machines):
            m = tokens[2 * k]
            p = tokens[2 * k + 1]
            if one_based:
                m -= 1
            if p < 0:
                raise ValueError(f"{path}: negative ptime at job {j}, op {k}")
            ops_for_job.append((m, p))

        # Validate each job uses every machine once (classic JSP)
        machines = [m for m, _ in ops_for_job]
        if sorted(machines) != list(range(n_machines)):
            raise ValueError(
                f"{path}: job {j} machines are not a permutation of 0..{n_machines-1}: {machines}"
            )

        jobs.append(ops_for_job)

    # 6) Build model-ready structures
    ops: List[Op] = []
    machine_of: Dict[Op, int] = {}
    ptime: Dict[Op, int] = {}
    job_succ: Dict[Op, Op] = {}
    ops_on_machine: Dict[int, List[Op]] = {m: [] for m in range(n_machines)}
    horizon = 0

    for j in range(n_jobs):
        for k in range(n_machines):
            op: Op = (j, k)
            m, p = jobs[j][k]
            ops.append(op)
            machine_of[op] = m
            ptime[op] = p
            ops_on_machine[m].append(op)
            horizon += p
            if k < n_machines - 1:
                job_succ[op] = (j, k + 1)

    return JSPModelData(
        name=path.stem,
        n_jobs=n_jobs,
        n_machines=n_machines,
        jobs=jobs,
        ops=ops,
        machine_of=machine_of,
        ptime=ptime,
        job_succ=job_succ,
        ops_on_machine=ops_on_machine,
        horizon=horizon,
    )


# ----------------------------
# Quick test runner (optional)
# ----------------------------
def _smoke_test():
    data_dir = Path("data/instances")
    files = ["ft06.txt", "ft10.txt", "la01.txt", "la02.txt"]

    print("Project root:", Path(".").resolve())
    print("Looking in:", data_dir.resolve())
    print("Directory exists?", data_dir.exists())
    if data_dir.exists():
        print("Files found:", sorted([p.name for p in data_dir.iterdir() if p.is_file()]))

    for fname in files:
        path = data_dir / fname
        print("\n---")
        print("Trying:", path.resolve())
        print("Exists?", path.exists())

        md = read_jsplib_instance(path)
        print(f"{md.name}: n={md.n_jobs}, m={md.n_machines}, horizon={md.horizon}")
        print("job0:", md.jobs[0])
        print("ops_on_machine[0] (first 5):", md.ops_on_machine[0][:5])
        print("succ((0,0)):", md.job_succ.get((0, 0)))


if __name__ == "__main__":
    _smoke_test()
