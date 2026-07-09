# experiments/run_environment_test.py

import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from config.simulation_config import SIMULATION_PARAMS
from plasma.environment import PlasmaEnvironment


def main():
    env = PlasmaEnvironment()

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
        f"{'collapse':>10}"
    )

    print("-" * 100)

    for _ in range(SIMULATION_PARAMS["T"]):
        s = env.state

        print(
            f"{s.t:3d} "
            f"{s.N:8.3f} "
            f"{s.D:8.3f} "
            f"{s.mode_amp:8.3f} "
            f"{s.E:8.3f} "
            f"{s.R1:8.3f} "
            f"{s.R2:8.3f} "
            f"{s.dD_dt:8.3f} "
            f"{s.risk_zone:>14} "
            f"{str(s.collapsed):>10}"
        )

        if s.collapsed:
            print("\nCOLLAPSE DETECTED")
            break

        env.step(0.0)


if __name__ == "__main__":
    main()
