from dataclasses import dataclass
from plasma.risk import compute_R1, compute_R2, classify_risk_zone


@dataclass
class ObservedState:
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


def make_observed_state(true_state, noise_level: float, rng, epsilon: float = 0.01):
    def noisy_positive(x):
        if noise_level <= 0.0:
            return x
        factor = 1.0 + rng.uniform(-noise_level, noise_level)
        return max(0.0, x * factor)

    N_obs = max(0.1, noisy_positive(true_state.N))
    D_obs = noisy_positive(true_state.D)
    mode_obs = noisy_positive(true_state.mode_amp)
    E_obs = max(0.0, min(1.0, noisy_positive(true_state.E)))
    dD_obs = true_state.dD_dt
    if noise_level > 0.0:
        dD_obs = true_state.dD_dt * (1.0 + rng.uniform(-noise_level, noise_level))

    R1_obs = compute_R1(N_obs, D_obs)
    R2_obs = compute_R2(N_obs, D_obs, epsilon)
    zone_obs = classify_risk_zone(N_obs, D_obs, mode_obs, dD_obs, epsilon)

    return ObservedState(
        t=true_state.t,
        N=N_obs,
        D=D_obs,
        mode_amp=mode_obs,
        E=E_obs,
        R1=R1_obs,
        R2=R2_obs,
        dD_dt=dD_obs,
        risk_zone=zone_obs,
        collapsed=true_state.collapsed,
    )
