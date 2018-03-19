from functools import reduce
from typing import Callable, Any


def compose(*funcs):
    def _comp(a, b):
        def _app(*n):
            return b(*a(*n))

        return _app

    return reduce(_comp, funcs)


def sequential(*tuple_operations: Callable) -> Callable:
    def _no_operations(*x: Any) -> None:
        return None

    if tuple_operations is None:
        return _no_operations

    if len(tuple_operations) > 1:
        return reduce(compose, tuple_operations)
    elif len(tuple_operations) == 1:
        return tuple_operations[0]

    return _no_operations


def pipeline(*models: Callable) -> Callable:
    valid_models = list(filter(lambda x: x is not None, models))
    if len(valid_models) > 0:
        return sequential(*valid_models)
    return lambda *x: None
