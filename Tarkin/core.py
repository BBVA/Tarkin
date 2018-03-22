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
from typing import Callable, Any


def compose(*funcs):
    def _comp(a, b):
        def _app(*n):
            # uncomment, modify the signature of the models to receive a *params list and process only the last one
            return b(*a(*n))
            # n_ = a(*n)
            # return n_[0], b(n_[1])

        return _app

    return reduce(_comp, funcs)


def sequential(*operations_tuple: Callable) -> Callable:
    def _no_operations(*x: Any) -> None:
        return None

    if operations_tuple is None:
        return _no_operations

    if len(operations_tuple) > 1:
        return reduce(compose, operations_tuple)
    elif len(operations_tuple) == 1:
        return operations_tuple[0]

    return _no_operations


def pipeline(*models: Callable) -> Callable:
    valid_models = list(filter(lambda x: x is not None, models))
    if len(valid_models) > 0:
        return sequential(*valid_models)
    return lambda *x: None
