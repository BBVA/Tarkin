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

from itertools import repeat
from typing import Callable, Optional


def pipeline(*models, reductor: Optional[Callable] = None):
    """
    if you use it for training:

     f(models) -> f(msg, Optional[states]) -> states

     if you use it for inference:

     f(models) -> f(msg, Optional[states]) -> result
    """
    valid_models = list(filter(lambda x: x is not None, models))
    size_valid_models = len(valid_models)
    if size_valid_models <= 0:
        return lambda *x: None

    def as_list(gen):
        return list(gen)

    if reductor is None:
        reduc_op = as_list
    else:
        reduc_op = reductor

    def _apply_model(x):
        (model, msg, state) = x
        return model(msg, state)

    def _initialize_states_tuple(states):
        if states is not None and len(states) > 0:
            return states
        return repeat(None, size_valid_models)

    def _app(msg, states=None):
        to_iter = zip(valid_models, repeat(msg), _initialize_states_tuple(states))
        return reduc_op(map(_apply_model, to_iter))

    return _app
