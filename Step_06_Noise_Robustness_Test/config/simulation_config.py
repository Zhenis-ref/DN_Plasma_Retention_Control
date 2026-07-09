MODEL_PARAMS = {
    "epsilon": 0.01,
    "N_safe": 4.5,
    "D_safe": 0.7,
    "N_critical": 1.4,
    "D_critical": 2.5,
    "mode_amp_critical": 1.0,
}

SIMULATION_PARAMS = {
    "T": 80,
    "dt": 1.0,
    "initial_E": 1.0,
    "initial_mode_amp": 0.2,
    "initial_N": 4.5,
    "initial_D": 0.7,
}

CONTROL_PARAMS = {
    "u_min": -1.0,
    "u_max": 1.0,
    "num_actions": 61,
}

BRUTE_FORCE_PARAMS = {
    "lookahead_depth": 1,
    "risk_weight": 1.0,
    "control_cost_weight": 0.20,
    "energy_depletion_weight": 0.50,
    "collapse_penalty": 1000.0,
}

DN_CCE_PARAMS = {
    "max_candidates": 15,
    "anchors": [-1.0, 0.0, 1.0],
    "local_span": 0.20,
    "local_points": 9,
}

NOISE_PARAMS = {
    "levels": [0.0, 0.05, 0.10, 0.20],
    "seeds": [101, 202, 303, 404, 505, 606, 707, 808, 909, 1001],
}
