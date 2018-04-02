"""
Copyright 2018 Banco Bilbao Vizcaya Argentaria, S.A.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from functools import reduce
from itertools import repeat
from typing import Callable, Any


# def compose(*funcs):
#     def _comp(a, b):
#         def _app(n):
#             return b(a(n))
#
#         return _app
#
#     return reduce(_comp, funcs)
#
#
# def sequential(*operations_tuple: Callable) -> Callable:
#     def _no_operations(*x: Any) -> None:
#         return None
#
#     if operations_tuple is None:
#         return _no_operations
#
#     if len(operations_tuple) > 1:
#         return reduce(compose, operations_tuple)
#     elif len(operations_tuple) == 1:
#         return operations_tuple[0]
#
#     return _no_operations


def pipeline(*models):
    """
     f(models) -> f(msg, Optional[states]) -> states
    """
    valid_models = list(filter(lambda x: x is not None, models))
    size_valid_models = len(valid_models)
    if size_valid_models <= 0:
        return lambda *x: None

    def _apply_model(x):
        (model, msg, state) = x
        return model(msg, state)

    def _initialize_states_tuple(states):
        if states is not None and len(states) > 0:
            return states
        return repeat(None, size_valid_models)

    def _app(msg, states=None):
        to_iter = zip(valid_models, repeat(msg), _initialize_states_tuple(states))
        return list(map(_apply_model, to_iter))

    return _app
