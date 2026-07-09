# config/simulation_config.py

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
