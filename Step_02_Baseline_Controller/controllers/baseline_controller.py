# controllers/baseline_controller.py

class BaselineController:
    """
    Simple reactive baseline controller.

    This controller does not use CCE, lookahead, brute force, or DN optimization.
    It reacts to visible risk indicators using fixed thresholds.
    """

    def select_action(self, state) -> float:
        # If resource is exhausted, no action is possible.
        if state.E <= 0.05:
            return 0.0

        # Emergency reaction.
        if state.R2 >= 1.20 or state.R1 >= 0.10 or state.D >= 2.20 or state.N <= 1.80:
            return 1.0

        # Strong warning reaction.
        if state.R2 >= 0.95 or state.R1 >= -0.10 or state.D >= 2.00 or state.N <= 2.30:
            return 0.7

        # Mild correction.
        if state.R2 >= 0.75 or state.D >= 1.70 or state.N <= 3.00:
            return 0.4

        return 0.0
