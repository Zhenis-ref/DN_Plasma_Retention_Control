from config.simulation_config import CONTROL_PARAMS, DN_CCE_PARAMS
from controllers.common import evaluate_action_loss


class DNCceController:
    def __init__(self):
        self.num_evaluations = 0

    def _clamp_u(self, u: float) -> float:
        return max(CONTROL_PARAMS["u_min"], min(CONTROL_PARAMS["u_max"], u))

    def _predicted_action(self, state) -> float:
        r2_pressure = max(0.0, state.R2 - 0.70)
        r1_pressure = max(0.0, state.R1 + 0.15)
        d_growth = max(0.0, state.dD_dt - 0.02)

        raw = 0.10 + 0.70 * r2_pressure + 0.45 * r1_pressure + 1.50 * d_growth

        if state.risk_zone == "pre_collapse":
            raw += 0.20
        elif state.risk_zone == "collapse_risk":
            raw += 0.40

        if state.E < 0.35:
            raw *= 0.65

        return self._clamp_u(raw)

    def _candidate_actions(self, state):
        candidates = set()

        for u in DN_CCE_PARAMS["anchors"]:
            candidates.add(round(self._clamp_u(u), 6))

        predicted = self._predicted_action(state)
        candidates.add(round(predicted, 6))

        span = DN_CCE_PARAMS["local_span"]
        points = DN_CCE_PARAMS["local_points"]

        if points <= 1:
            local_values = [predicted]
        else:
            local_values = [
                predicted - span + (2 * span) * i / (points - 1)
                for i in range(points)
            ]

        for u in local_values:
            candidates.add(round(self._clamp_u(u), 6))

        if state.R2 >= 0.75 or state.D >= 1.7:
            candidates.update([0.25, 0.40, 0.55])

        if state.R2 >= 0.95 or state.R1 >= -0.10:
            candidates.update([0.60, 0.70, 0.85])

        if state.E < 0.30:
            candidates.update([0.0, 0.15, 0.30])

        ordered = sorted(candidates)
        max_candidates = DN_CCE_PARAMS["max_candidates"]

        if len(ordered) <= max_candidates:
            return ordered

        ordered_by_predicted = sorted(ordered, key=lambda x: abs(x - predicted))
        compact = ordered_by_predicted[:max_candidates]

        for anchor in DN_CCE_PARAMS["anchors"]:
            anchor = self._clamp_u(anchor)
            if anchor not in compact:
                compact[-1] = anchor

        return sorted(set(compact))

    def select_action(self, env, observed_state=None) -> float:
        state = observed_state if observed_state is not None else env.state
        candidates = self._candidate_actions(state)

        best_u = 0.0
        best_loss = float("inf")

        for u in candidates:
            loss = evaluate_action_loss(env, u)
            self.num_evaluations += 1

            if loss < best_loss:
                best_loss = loss
                best_u = u

        return best_u
