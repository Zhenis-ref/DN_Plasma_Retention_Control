# plasma/risk.py

"""
HL-2A-informed risk functions.

N - external sustaining regime / confinement condition.
D - internal structural tension / MHD-like magnetic activity.
mode_amp - hidden dominant MHD mode amplitude.
"""


def compute_R1(N: float, D: float) -> float:
    """R1 = D - N."""
    return D - N


def compute_R2(N: float, D: float, epsilon: float = 0.01) -> float:
    """R2 = D / (N + epsilon)."""
    return D / (N + epsilon)


def compute_R3(mode_amp: float) -> float:
    """R3 = hidden dominant MHD mode amplitude."""
    return mode_amp


def compute_R4(dD_dt: float) -> float:
    """R4 = positive growth rate of internal structural tension."""
    return max(0.0, dD_dt)


def compute_total_risk(
    N: float,
    D: float,
    mode_amp: float,
    dD_dt: float,
    epsilon: float = 0.01,
) -> float:
    R1 = compute_R1(N, D)
    R2 = compute_R2(N, D, epsilon)
    R3 = compute_R3(mode_amp)
    R4 = compute_R4(dD_dt)

    R1_pos = max(0.0, R1)
    R2_excess = max(0.0, R2 - 1.0)

    return (
        1.00 * R1_pos
        + 1.20 * R2_excess
        + 1.50 * R3
        + 0.80 * R4
    )


def classify_risk_zone(
    N: float,
    D: float,
    mode_amp: float,
    dD_dt: float,
    epsilon: float = 0.01,
) -> str:
    R1 = compute_R1(N, D)
    R2 = compute_R2(N, D, epsilon)
    total_risk = compute_total_risk(N, D, mode_amp, dD_dt, epsilon)

    if mode_amp >= 1.0 or R2 >= 1.5:
        return "collapse_risk"

    if R1 > 0.0 or R2 > 1.0:
        return "pre_collapse"

    if total_risk > 0.5 or dD_dt > 0.02:
        return "warning"

    return "stable"
