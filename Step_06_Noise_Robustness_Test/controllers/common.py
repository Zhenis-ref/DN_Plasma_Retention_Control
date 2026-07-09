from config.simulation_config import BRUTE_FORCE_PARAMS, MODEL_PARAMS
from plasma.risk import compute_total_risk


def evaluate_action_loss(env, u: float) -> float:
    test_env = env.clone()
    state_before = test_env.state
    E_before = state_before.E

    next_state = test_env.step(u)

    risk = compute_total_risk(
        next_state.N,
        next_state.D,
        next_state.mode_amp,
        next_state.dD_dt,
        MODEL_PARAMS["epsilon"],
    )

    control_cost = abs(u)
    energy_used = max(0.0, E_before - next_state.E)

    loss = (
        BRUTE_FORCE_PARAMS["risk_weight"] * risk
        + BRUTE_FORCE_PARAMS["control_cost_weight"] * control_cost
        + BRUTE_FORCE_PARAMS["energy_depletion_weight"] * energy_used
    )

    if next_state.collapsed:
        loss += BRUTE_FORCE_PARAMS["collapse_penalty"]

    return loss
