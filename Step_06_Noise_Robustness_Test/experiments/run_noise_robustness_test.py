import csv
import os
import random
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

import matplotlib.pyplot as plt

from config.simulation_config import SIMULATION_PARAMS, NOISE_PARAMS
from plasma.environment import PlasmaEnvironment
from controllers.observed_state import make_observed_state
from controllers.baseline_controller import BaselineController
from controllers.brute_force_controller import BruteForceController
from controllers.dn_cce_controller import DNCceController


PLOTS_DIR = os.path.join(PROJECT_ROOT, "outputs", "plots")
TABLES_DIR = os.path.join(PROJECT_ROOT, "outputs", "tables")


def run_one(controller_name, noise_level, seed):
    rng = random.Random(seed)
    env = PlasmaEnvironment()

    if controller_name == "baseline":
        controller = BaselineController()
    elif controller_name == "brute_force":
        controller = BruteForceController()
    elif controller_name == "dn_cce":
        controller = DNCceController()
    else:
        raise ValueError(controller_name)

    history = []

    for _ in range(SIMULATION_PARAMS["T"]):
        true_state = env.state
        obs_state = make_observed_state(true_state, noise_level, rng)

        if controller_name == "baseline":
            u = controller.select_action(obs_state)
        elif controller_name == "brute_force":
            # Brute-force uses true env for lookahead, but action is selected from full grid.
            # This is the ideal reference under noisy observation setting.
            u = controller.select_action(env)
        else:
            u = controller.select_action(env, observed_state=obs_state)

        history.append({
            "controller": controller_name,
            "noise": noise_level,
            "seed": seed,
            "t": true_state.t,
            "N": true_state.N,
            "D": true_state.D,
            "mode_amp": true_state.mode_amp,
            "E": true_state.E,
            "R1": true_state.R1,
            "R2": true_state.R2,
            "u": u,
            "collapsed": true_state.collapsed,
        })

        if true_state.collapsed:
            break

        env.step(u)

    last = history[-1]
    return {
        "controller": controller_name,
        "noise": noise_level,
        "seed": seed,
        "collapsed": last["collapsed"],
        "final_t": last["t"],
        "total_u": sum(abs(row["u"]) for row in history),
        "final_E": last["E"],
        "max_R2": max(row["R2"] for row in history),
        "max_D": max(row["D"] for row in history),
        "min_N": min(row["N"] for row in history),
        "max_mode_amp": max(row["mode_amp"] for row in history),
        "evals": getattr(controller, "num_evaluations", 0),
    }


def aggregate(rows):
    grouped = {}
    for row in rows:
        key = (row["controller"], row["noise"])
        grouped.setdefault(key, []).append(row)

    out = []
    for (controller, noise), items in grouped.items():
        n = len(items)
        collapse_rate = sum(1 for x in items if x["collapsed"]) / n
        out.append({
            "controller": controller,
            "noise": noise,
            "runs": n,
            "collapse_rate": collapse_rate,
            "mean_total_u": sum(x["total_u"] for x in items) / n,
            "mean_final_E": sum(x["final_E"] for x in items) / n,
            "mean_max_R2": sum(x["max_R2"] for x in items) / n,
            "mean_max_D": sum(x["max_D"] for x in items) / n,
            "mean_min_N": sum(x["min_N"] for x in items) / n,
            "mean_max_mode_amp": sum(x["max_mode_amp"] for x in items) / n,
            "mean_evals": sum(x["evals"] for x in items) / n,
        })

    return sorted(out, key=lambda x: (x["noise"], x["controller"]))


def write_csv(path, rows, fieldnames):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def plot_aggregate(agg, metric, ylabel, filename):
    plt.figure(figsize=(10, 6))
    controllers = ["baseline", "brute_force", "dn_cce"]

    for controller in controllers:
        items = [x for x in agg if x["controller"] == controller]
        xs = [x["noise"] * 100 for x in items]
        ys = [x[metric] for x in items]
        plt.plot(xs, ys, marker="o", label=controller)

    plt.xlabel("measurement noise (%)")
    plt.ylabel(ylabel)
    plt.title(filename.replace("_", " ").replace(".png", ""))
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, filename), dpi=160)
    plt.close()


def main():
    os.makedirs(PLOTS_DIR, exist_ok=True)
    os.makedirs(TABLES_DIR, exist_ok=True)

    rows = []
    for noise in NOISE_PARAMS["levels"]:
        for seed in NOISE_PARAMS["seeds"]:
            for controller in ["baseline", "brute_force", "dn_cce"]:
                rows.append(run_one(controller, noise, seed))

    agg = aggregate(rows)

    write_csv(
        os.path.join(TABLES_DIR, "noise_runs.csv"),
        rows,
        [
            "controller", "noise", "seed", "collapsed", "final_t",
            "total_u", "final_E", "max_R2", "max_D", "min_N",
            "max_mode_amp", "evals"
        ],
    )

    write_csv(
        os.path.join(TABLES_DIR, "noise_summary.csv"),
        agg,
        [
            "controller", "noise", "runs", "collapse_rate",
            "mean_total_u", "mean_final_E", "mean_max_R2",
            "mean_max_D", "mean_min_N", "mean_max_mode_amp",
            "mean_evals"
        ],
    )

    plot_aggregate(agg, "collapse_rate", "collapse rate", "noise_collapse.png")
    plot_aggregate(agg, "mean_total_u", "mean total_u", "noise_total_u.png")
    plot_aggregate(agg, "mean_final_E", "mean final_E", "noise_final_E.png")
    plot_aggregate(agg, "mean_evals", "mean evals", "noise_evals.png")
    plot_aggregate(agg, "mean_max_R2", "mean max_R2", "noise_max_R2.png")

    print("STEP 06 NOISE ROBUSTNESS TEST GENERATED")
    print()
    print("AGGREGATED SUMMARY")
    print("-" * 120)
    for item in agg:
        print(
            f"{item['controller']:>12} | "
            f"noise={item['noise']*100:>5.1f}% | "
            f"runs={item['runs']:>2} | "
            f"collapse_rate={item['collapse_rate']:>5.2f} | "
            f"mean_total_u={item['mean_total_u']:>7.2f} | "
            f"mean_final_E={item['mean_final_E']:>6.3f} | "
            f"mean_max_R2={item['mean_max_R2']:>6.3f} | "
            f"mean_evals={item['mean_evals']:>7.1f}"
        )

    print()
    print("Saved:")
    print(os.path.join(TABLES_DIR, "noise_runs.csv"))
    print(os.path.join(TABLES_DIR, "noise_summary.csv"))
    for filename in sorted(os.listdir(PLOTS_DIR)):
        print(os.path.join(PLOTS_DIR, filename))


if __name__ == "__main__":
    main()
