from src.training.position.results import ShortPositionResult


class ShortPositionTarget:

    @staticmethod
    def calculate_target(position_result: ShortPositionResult) -> int:
        """Target event: P&L is ge then expected take profit."""

        return position_result.pnl >= position_result.input_parameters.take_profit
