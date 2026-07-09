# experiments/run_brute_force_test.py

import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from config.simulation_config import SIMULATION_PARAMS
from plasma.environment import PlasmaEnvironment
from controllers.baseline_controller import BaselineController
from controllers.brute_force_controller import BruteForceController


def run_open_loop():
    env = PlasmaEnvironment()
    history = []

    for _ in range(SIMULATION_PARAMS["T"]):
        s = env.state
        history.append((s.t, s.N, s.D, s.mode_amp, s.E, s.R1, s.R2, s.dD_dt, s.risk_zone, 0.0, s.collapsed))
        if s.collapsed:
            break
        env.step(0.0)

    return history, 0


def run_baseline():
    env = PlasmaEnvironment()
    controller = BaselineController()
    history = []

    for _ in range(SIMULATION_PARAMS["T"]):
        s = env.state
        u = controller.select_action(s)
        history.append((s.t, s.N, s.D, s.mode_amp, s.E, s.R1, s.R2, s.dD_dt, s.risk_zone, u, s.collapsed))
        if s.collapsed:
            break
        env.step(u)

    return history, 0


def run_brute_force():
    env = PlasmaEnvironment()
    controller = BruteForceController()
    history = []

    for _ in range(SIMULATION_PARAMS["T"]):
        s = env.state
        u = controller.select_action(env)
        history.append((s.t, s.N, s.D, s.mode_amp, s.E, s.R1, s.R2, s.dD_dt, s.risk_zone, u, s.collapsed))
        if s.collapsed:
            break
        env.step(u)

    return history, controller.num_evaluations


def print_tail(title, history, tail=12):
    print("\n" + title)
    print(
        f"{'t':>3} "
        f"{'N':>8} "
        f"{'D':>8} "
        f"{'mode':>8} "
        f"{'E':>8} "
        f"{'R1':>8} "
        f"{'R2':>8} "
        f"{'dD':>8} "
        f"{'zone':>14} "
        f"{'u':>6} "
        f"{'collapse':>10}"
    )
    print("-" * 108)

    for row in history[-tail:]:
        t, N, D, mode_amp, E, R1, R2, dD_dt, zone, u, collapsed = row
        print(
            f"{t:3d} "
            f"{N:8.3f} "
            f"{D:8.3f} "
            f"{mode_amp:8.3f} "
            f"{E:8.3f} "
            f"{R1:8.3f} "
            f"{R2:8.3f} "
            f"{dD_dt:8.3f} "
            f"{zone:>14} "
            f"{u:6.2f} "
            f"{str(collapsed):>10}"
        )


def summarize(label, history, evals):
    last = history[-1]
    collapsed = last[-1]
    final_t = last[0]
    total_control = sum(abs(row[9]) for row in history)
    max_R2 = max(row[6] for row in history)
    max_D = max(row[2] for row in history)
    min_N = min(row[1] for row in history)
    max_mode = max(row[3] for row in history)
    final_E = last[4]

    return {
        "label": label,
        "collapsed": collapsed,
        "final_t": final_t,
        "total_control": total_control,
        "max_R2": max_R2,
        "max_D": max_D,
        "min_N": min_N,
        "max_mode_amp": max_mode,
        "final_E": final_E,
        "evals": evals,
    }


def main():
    open_loop_history, open_loop_evals = run_open_loop()
    baseline_history, baseline_evals = run_baseline()
    brute_force_history, brute_force_evals = run_brute_force()

    print_tail("OPEN LOOP / NO CONTROL — last rows", open_loop_history)
    print_tail("BASELINE CONTROLLER — last rows", baseline_history)
    print_tail("BRUTE FORCE CONTROLLER — last rows", brute_force_history)

    summaries = [
        summarize("open_loop", open_loop_history, open_loop_evals),
        summarize("baseline", baseline_history, baseline_evals),
        summarize("brute_force", brute_force_history, brute_force_evals),
    ]

    print("\nSUMMARY")
    print("-" * 112)
    for item in summaries:
        print(
            f"{item['label']:>12} | "
            f"collapsed={str(item['collapsed']):>5} | "
            f"final_t={item['final_t']:>3} | "
            f"total_u={item['total_control']:>7.2f} | "
            f"final_E={item['final_E']:>6.3f} | "
            f"max_R2={item['max_R2']:>6.3f} | "
            f"max_D={item['max_D']:>6.3f} | "
            f"min_N={item['min_N']:>6.3f} | "
            f"max_mode={item['max_mode_amp']:>6.3f} | "
            f"evals={item['evals']:>5}"
        )


if __name__ == "__main__":
    main()
