from functools import reduce
from datarefinery.tuple.TupleDSL import compose



def sequential(*tuple_operations):
    def _no_operations(inp=None, err=None):
        return None, "No operations to perform"

    def _no_affect(inp, err=None):
        if inp is not None:
            i = copy.deepcopy(inp)
        else:
            i = None
        if err is not None:
            e = copy.deepcopy(err)
        else:
            e = None
        return i, e

    some_params = any(map(lambda x: x is not None, tuple_operations))
    if tuple_operations is not None and some_params:
        return compose(_no_affect, reduce(compose, tuple_operations))
    return _no_operations


def pipeline(models*):
  return sequential(models)
