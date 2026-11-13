#!/usr/bin/env python3
"""Script d'exécution des expérimentations (Partie 6).

Lit sample.csv, dérive et exécute chaque variante (Python ou C)
plusieurs fois (3 runs) et sauvegarde les résultats dans results.csv.
"""

import argparse
import csv
import os
import platform
import subprocess
import sys
import tempfile
import time
from pathlib import Path
import numpy as np

REPS_MAP = {
    "N1000": 1000,
    "N10000": 10000,
    "N100000": 100000,
    "N1000000": 1000000,
}

DIR_PATH = Path(__file__).resolve().parent
RUNNER_C = DIR_PATH / "runner.c"
COMPILED_BINARIES = {}


def run_python(prop: str, prec: str, reps: int, dist: str, seed: int) -> float:
    """Exécute une variante Python avec NumPy vectorisé."""
    rng = np.random.default_rng(seed)
    dtype = np.float32 if prec == "SinglePrecision" else np.float64
    one = dtype(1.0)

    if dist == "Uniform01":
        x = rng.uniform(0.00001, 1.0, reps).astype(dtype)
        y = rng.uniform(0.00001, 1.0, reps).astype(dtype)
        z = rng.uniform(0.00001, 1.0, reps).astype(dtype)
    elif dist == "UniformNeg1Pos1":
        x = rng.uniform(-1.0, 1.0, reps).astype(dtype)
        y = rng.uniform(-1.0, 1.0, reps).astype(dtype)
        z = rng.uniform(-1.0, 1.0, reps).astype(dtype)
        x[x == 0.0] = dtype(0.00001)
    elif dist == "Gaussian":
        x = rng.normal(0.0, 1.0, reps).astype(dtype)
        y = rng.normal(0.0, 1.0, reps).astype(dtype)
        z = rng.normal(0.0, 1.0, reps).astype(dtype)
        x[x == 0.0] = dtype(0.00001)
    else:
        raise ValueError(f"Distribution inconnue : {dist}")

    if prop == "AssocAdd":
        holds = ((x + y) + z) == (x + (y + z))
    elif prop == "AssocMul":
        holds = ((x * y) * z) == (x * (y * z))
    elif prop == "Distributivity":
        holds = (x * (y + z)) == ((x * y) + (x * z))
    elif prop == "InverseMul":
        holds = (x * (one / x)) == one
    else:
        raise ValueError(f"Propriété inconnue : {prop}")

    return float(100.0 * np.count_nonzero(holds) / reps)


def get_c_binary(prec: str, opt: str, build_dir: Path) -> Path:
    """Compile runner.c avec les bons flags gcc si nécessaire."""
    key = (prec, opt)
    if key in COMPILED_BINARIES:
        return COMPILED_BINARIES[key]

    bin_path = build_dir / f"bin_{prec}_{opt or 'none'}"
    cmd = ["gcc"]
    if prec == "SinglePrecision":
        cmd.append("-DUSE_SINGLE")

    if opt == "O0":
        cmd.append("-O0")
    elif opt == "O2":
        cmd.append("-O2")
    elif opt == "O3":
        cmd.append("-O3")
    elif opt == "FastMath":
        cmd.extend(["-O3", "-ffast-math"])

    cmd.extend([str(RUNNER_C), "-lm", "-o", str(bin_path)])
    subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    COMPILED_BINARIES[key] = bin_path
    return bin_path


def run_c(
    prop: str, prec: str, reps: int, dist: str, opt: str, seed: int, build_dir: Path
) -> float:
    """Exécute une variante C en appelant le binaire compilé."""
    bin_path = get_c_binary(prec, opt, build_dir)
    prop_code = {
        "AssocAdd": 0,
        "AssocMul": 1,
        "Distributivity": 2,
        "InverseMul": 3,
    }[prop]
    dist_code = {"Uniform01": 0, "UniformNeg1Pos1": 1, "Gaussian": 2}[dist]

    cmd = [str(bin_path), str(prop_code), str(dist_code), str(reps), str(seed)]
    res = subprocess.check_output(cmd, text=True)
    return float(res.strip())


def main():
    parser = argparse.ArgumentParser(
        description="Exécute les variantes de sample.csv."
    )
    parser.add_argument(
        "--sample", default="../sample.csv", help="Chemin vers sample.csv"
    )
    parser.add_argument(
        "--output", default="results.csv", help="Fichier de sortie CSV"
    )
    parser.add_argument(
        "--runs", type=int, default=3, help="Nombre de runs par config"
    )
    parser.add_argument(
        "--seed", type=int, default=42, help="Graine initiale"
    )
    args = parser.parse_args()

    sample_path = Path(args.sample)
    if not sample_path.exists():
        sample_path = Path("tp3/sample.csv")
    if not sample_path.exists():
        sys.exit(f"Erreur : impossible de trouver {args.sample}")

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with sample_path.open() as f:
        configs = list(csv.DictReader(f))

    print(
        f"Exécution de {len(configs)} configurations ({args.runs} runs chacune)..."
    )

    host_arch = platform.machine()
    host_os = platform.system()
    py_ver = platform.python_version()

    build_dir = Path(tempfile.mkdtemp(prefix="rep_tp3_build_"))
    results = []
    t_start = time.time()

    for idx, cfg in enumerate(configs, start=1):
        cid = cfg["config_id"]
        prop = cfg["Property"]
        prec = cfg["Precision"]
        reps = REPS_MAP.get(cfg["Repetitions"], 10000)
        dist = cfg["Distribution"]
        lang = cfg["Language"]
        opt = cfg.get("Optimization", "").strip()

        for run_idx in range(1, args.runs + 1):
            seed = args.seed + (idx * 100) + run_idx
            t0 = time.perf_counter()

            if lang == "Python":
                pct = run_python(prop, prec, reps, dist, seed)
            else:
                pct = run_c(prop, prec, reps, dist, opt, seed, build_dir)

            duration_ms = (time.perf_counter() - t0) * 1000.0

            results.append({
                "run_id": f"{cid}_{run_idx}",
                "config_id": cid,
                "origin_of_config": cfg["origin_of_config"],
                "run_index": run_idx,
                "seed": seed,
                "Property": prop,
                "Precision": prec,
                "Repetitions": cfg["Repetitions"],
                "Distribution": dist,
                "Language": lang,
                "Architecture": cfg.get("Architecture", host_arch),
                "RuntimeVersion": cfg.get("RuntimeVersion", "RuntimeV1"),
                "Optimization": opt,
                "percentage": round(pct, 4),
                "execution_time_ms": round(duration_ms, 2),
                "host_arch": host_arch,
                "host_os": host_os,
                "runtime_info": py_ver if lang == "Python" else "gcc",
            })

    with output_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(results[0].keys()))
        writer.writeheader()
        writer.writerows(results)

    elapsed = time.time() - t_start
    print(
        f"Terminé : {len(results)} runs enregistrés dans {output_path} en {elapsed:.2f}s."
    )


if __name__ == "__main__":
    main()
