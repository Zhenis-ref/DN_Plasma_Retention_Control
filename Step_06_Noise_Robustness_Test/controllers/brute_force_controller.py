from config.simulation_config import CONTROL_PARAMS
from controllers.common import evaluate_action_loss


class BruteForceController:
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

    def select_action(self, env) -> float:
        best_u = 0.0
        best_loss = float("inf")

        for u in self._action_grid():
            loss = evaluate_action_loss(env, u)
            self.num_evaluations += 1

            if loss < best_loss:
                best_loss = loss
                best_u = u

        return best_u
