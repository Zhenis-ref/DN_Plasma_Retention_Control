# plasma/environment.py

import copy
from dataclasses import dataclass

from config.simulation_config import MODEL_PARAMS, SIMULATION_PARAMS
from plasma.risk import compute_R1, compute_R2, classify_risk_zone


@dataclass
class PlasmaState:
    t: int
    N: float
    D: float
    mode_amp: float
    E: float
    R1: float
    R2: float
    dD_dt: float
    risk_zone: str
    collapsed: bool = False


class PlasmaEnvironment:
    def __init__(self):
        self.eps = MODEL_PARAMS["epsilon"]
        self.reset()

    def clone(self):
        return copy.deepcopy(self)

    def reset(self):
        self.t = 0
        self.prev_D = SIMULATION_PARAMS["initial_D"]

        self.state = PlasmaState(
            t=0,
            N=SIMULATION_PARAMS["initial_N"],
            D=SIMULATION_PARAMS["initial_D"],
            mode_amp=SIMULATION_PARAMS["initial_mode_amp"],
            E=SIMULATION_PARAMS["initial_E"],
            R1=0.0,
            R2=0.0,
            dD_dt=0.0,
            risk_zone="stable",
            collapsed=False,
        )

        self._update_risk_terms()
        return self.state

    def _update_risk_terms(self):
        self.state.R1 = compute_R1(self.state.N, self.state.D)
        self.state.R2 = compute_R2(self.state.N, self.state.D, self.eps)
        self.state.dD_dt = self.state.D - self.prev_D
        self.state.risk_zone = classify_risk_zone(
            self.state.N,
            self.state.D,
            self.state.mode_amp,
            self.state.dD_dt,
            self.eps,
        )

    def step(self, u: float):
        u = max(-1.0, min(1.0, u))

        N = self.state.N
        D = self.state.D
        mode_amp = self.state.mode_amp
        E = self.state.E

        self.prev_D = D

        natural_N_decay = 0.035
        natural_D_growth = 0.030
        natural_mode_growth_from_D = 0.006 * max(0.0, D - 1.8)

        control_N_support = 0.080 * u * E
        control_D_suppression = 0.070 * u * E
        control_mode_suppression = 0.050 * u * E
        control_cost = 0.040 * abs(u)

        N_next = N - natural_N_decay + control_N_support
        D_next = D + natural_D_growth - control_D_suppression

        R1_next = compute_R1(N_next, D_next)
        R2_next = compute_R2(N_next, D_next, self.eps)

        risk_drive = max(0.0, R1_next) + max(0.0, R2_next - 1.0)

        mode_amp_next = (
            mode_amp
            + natural_mode_growth_from_D
            + 0.060 * risk_drive
            - control_mode_suppression
        )

        E_next = E - control_cost

        N_next = max(0.1, min(6.0, N_next))
        D_next = max(0.0, min(4.0, D_next))
        mode_amp_next = max(0.0, min(3.0, mode_amp_next))
        E_next = max(0.0, min(1.0, E_next))

        collapsed = (
            mode_amp_next >= MODEL_PARAMS["mode_amp_critical"]
            or N_next <= MODEL_PARAMS["N_critical"]
            or D_next >= MODEL_PARAMS["D_critical"]
            or R2_next >= 1.5
        )

        self.t += 1

        self.state = PlasmaState(
            t=self.t,
            N=N_next,
            D=D_next,
            mode_amp=mode_amp_next,
            E=E_next,
            R1=0.0,
            R2=0.0,
            dD_dt=0.0,
            risk_zone="stable",
            collapsed=collapsed,
        )

        self._update_risk_terms()
        return self.state
