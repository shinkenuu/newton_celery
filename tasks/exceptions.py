class CalculationError(Exception):
    pass


class CalculationNotFound(CalculationError):
    pass


class CalculationUpdateError(CalculationError):
    pass
