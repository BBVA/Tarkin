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

from collections import Counter, Callable
from statistics import mean

from ..service.Stats import Stats


def gen_model(etl: Callable) -> Callable:
    """
     f(etl) -> f(msg, Optional[state]) -> state'
     :type etl: Callable
    """
    def _app(msg, letter_space=None):
        if letter_space is None:
            letter_space = {}

        if isinstance(letter_space, dict):
            return train(etl(msg), letter_space)

        raise ValueError("Invalid letterspace")

    return _app


def train(message: str, letter_space: dict) -> dict:
    """
     f(message, state) -> state'

     :type message: str
     :param letter_space: dict
    """
    res = dict(Counter(message.lower()))
    if res is not None:
        for letter, count in res.items():
            if letter not in letter_space:
                stats = Stats()
            else:
                stats = letter_space[letter]

            letter_space[letter] = stats.add_variable(count)

    return letter_space


def check(letter_space: dict) -> Callable:
    """
     f(state) -> f(msg) -> float

     :type letter_space: dict
    """
    if letter_space is None:
        return lambda *x: None

    def char_count(msg):
        return dict(Counter(msg.lower()))

    def _app(msg):
        chars = char_count(msg)
        counts = [
            1 if k not in chars else v.is_in_std(chars[k])
            for k, v in letter_space.items()
        ]
        return mean(counts)
    return _app


__all__ = ["gen_model", "check"]
