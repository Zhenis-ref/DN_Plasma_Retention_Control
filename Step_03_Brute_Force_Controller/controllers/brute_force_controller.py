# controllers/brute_force_controller.py

from config.simulation_config import CONTROL_PARAMS, BRUTE_FORCE_PARAMS, MODEL_PARAMS
from plasma.risk import compute_total_risk


class BruteForceController:
    """
    Full action-grid controller.

    This is the Step 03 reference controller:
    it evaluates all possible actions and selects the action with minimal loss.
    """

    def __init__(self):
        self.num_evaluations = 0

    def _action_grid(self):
        u_min = CONTROL_PARAMS["u_min"]
        u_max = CONTROL_PARAMS["u_max"]
        n = CONTROL_PARAMS["num_actions"]

        if n <= 1:
            return [0.0]

        step = (u_max - u_min) / (n - 1)
        return [u_min + i * step for i in range(n)]

    def _loss(self, env, u: float) -> float:
        test_env = env.clone()

        state_before = test_env.state
        E_before = state_before.E

        next_state = test_env.step(u)

        self.num_evaluations += 1

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

    def select_action(self, env) -> float:
        best_u = 0.0
        best_loss = float("inf")

        for u in self._action_grid():
            loss = self._loss(env, u)

            if loss < best_loss:
                best_loss = loss
                best_u = u

        return best_u
