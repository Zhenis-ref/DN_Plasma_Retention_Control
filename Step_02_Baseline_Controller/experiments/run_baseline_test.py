# experiments/run_baseline_test.py

import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from config.simulation_config import SIMULATION_PARAMS
from plasma.environment import PlasmaEnvironment
from controllers.baseline_controller import BaselineController


def run_open_loop():
    env = PlasmaEnvironment()
    history = []

    for _ in range(SIMULATION_PARAMS["T"]):
        s = env.state
        history.append((s.t, s.N, s.D, s.mode_amp, s.E, s.R1, s.R2, s.dD_dt, s.risk_zone, 0.0, s.collapsed))
        if s.collapsed:
            break
        env.step(0.0)

    return history


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

    return history


def print_history(title, history):
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

    for row in history:
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


def summarize(label, history):
    last = history[-1]
    collapsed = last[-1]
    final_t = last[0]
    total_control = sum(abs(row[9]) for row in history)
    max_R2 = max(row[6] for row in history)
    max_D = max(row[2] for row in history)
    min_N = min(row[1] for row in history)
    max_mode = max(row[3] for row in history)

    return {
        "label": label,
        "collapsed": collapsed,
        "final_t": final_t,
        "total_control": total_control,
        "max_R2": max_R2,
        "max_D": max_D,
        "min_N": min_N,
        "max_mode_amp": max_mode,
    }


def main():
    open_loop_history = run_open_loop()
    baseline_history = run_baseline()

    print_history("OPEN LOOP / NO CONTROL", open_loop_history)
    print_history("BASELINE CONTROLLER", baseline_history)

    summaries = [
        summarize("open_loop", open_loop_history),
        summarize("baseline", baseline_history),
    ]

    print("\nSUMMARY")
    print("-" * 80)
    for item in summaries:
        print(
            f"{item['label']:>10} | "
            f"collapsed={str(item['collapsed']):>5} | "
            f"final_t={item['final_t']:>3} | "
            f"total_u={item['total_control']:>7.2f} | "
            f"max_R2={item['max_R2']:>6.3f} | "
            f"max_D={item['max_D']:>6.3f} | "
            f"min_N={item['min_N']:>6.3f} | "
            f"max_mode={item['max_mode_amp']:>6.3f}"
        )


if __name__ == "__main__":
    main()
