def sum_(*args):
    """
    >>> sum_(10, -4, 1)
    7
    >>> sum_(1, 2, 3, 0)
    6
    """
    result = sum(args)
    return result


def subtract(*args):
    """
    >>> subtract(10, 2, 5)
    3
    >>> subtract(10, -2, 4)
    8
    """
    result = args[0] - sum(args[1:])
    return result


def multiply(*args):
    """
    >>> multiply(10, 5, 3)
    150
    >>> multiply(3, -4)
    -12
    >>> multiply(2, -4, -3)
    24
    >>> multiply(2, 0, 6)
    0
    """
    if 0 in args:
        return 0

    result = args[0]

    for arg in args[1:]:
        result *= arg

    return result


def divide(*args):
    """
    >>> divide(10, 2)
    5.0
    >>> divide(24, 4, 3)
    2.0
    >>> divide(0, 2, 4)
    0.0
    """
    result = args[0]

    for arg in args[1:]:
        result /= arg

    return result
