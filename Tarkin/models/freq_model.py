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

from collections import Counter
from statistics import mean
from typing import Optional, Callable, Any, Dict, TypeVar

from Tarkin.models.Stats import Stats


Etl_func = Callable[[Any], str]
Letter_space = Dict[str, Stats]


def gen_model(etl: Optional[Etl_func] = None) -> Callable[[str, Optional[Letter_space]], Letter_space]:
    """
     f(Optional[Callable]) -> f(msg, Optional[state]) -> state'
     :type etl: Optional[Callable]
    """
    return _base_model(_generate_state, etl)


def check(etl: Optional[Etl_func] = None) -> Callable[[str, Optional[Letter_space]], float]:
    """
     f(Optional[Callable]) -> f(msg, Optional[state]) -> x
     :type etl: Optional[Callable]
    """
    return _base_model(_score_message, etl)


A = TypeVar("A", Letter_space, float)


def _base_model(
        operation: Callable[[str, Optional[Letter_space]], A],
        etl: Optional[Etl_func] = None
) -> Callable[[str, Optional[Letter_space]], A]:
    """
     f(Optional[Callable]) -> f(msg, Optional[x]) -> y
     :type etl: Optional[Callable]
    """

    def no_etl(x):
        return x

    if etl is None:
        etl_op = no_etl
    else:
        etl_op = etl

    def _app(message, letter_space=None):
        if letter_space is None:
            letter_space = {}

        if isinstance(letter_space, dict):
            return operation(etl_op(message), letter_space)

        raise ValueError("Invalid letterspace")

    return _app


def _generate_state(message: str, letter_space: Optional[Letter_space]) -> Letter_space:
    res = dict(Counter(message.lower()))
    if res is not None:
        for letter, count in res.items():
            if letter not in letter_space:
                stats = Stats()
            else:
                stats = letter_space[letter]

            letter_space[letter] = stats.add_variable(count)

    return letter_space


def _score_message(message: str, letter_space: Letter_space) -> float:
    def char_count(m: str):
        return dict(Counter(m.lower()))

    chars = char_count(message)
    counts = [
        1 if k not in chars else v.is_in_std(chars[k])
        for k, v in letter_space.items()
    ]
    if len(counts) > 0:
        return mean(counts)
    return 1.0


__all__ = ["gen_model", "check"]
