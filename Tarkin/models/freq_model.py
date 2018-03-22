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

from datarefinery.CombineOperations import sequential
from datarefinery.TupleOperations import append, keep, wrap
from datarefinery.tuple.Formats import csv_to_map

from ..service.Stats import Stats


def gen_model(initial_letter_space: dict = {}):

    # def _app0(message: str, init_letterspace={}):
    #     return train(message, init_letterspace)

    # def _app(message: str, **kwargs):
    #
    #     letter_space = kwargs.get('initial_letter_space', initial_letter_space)
    #
    #     if isinstance(letter_space, dict):
    #         return train(message, letter_space)
    #
    #     raise ValueError("Invalid letterspace")

    def _app(*args, **kwargs):

        letter_space = kwargs.get('initial_letter_space', initial_letter_space)

        message = args[-1]

        if isinstance(letter_space, dict):
            return train(message, letter_space)

        raise ValueError("Invalid letterspace")


    return _app


# should probably be added as the first chained operation at the pipeline
def etl():
    return sequential(
        csv_to_map([
            'date', 'file', 'date2', 'log', 'app', 'beat', 'front', 'is_log',
            'msg', 'offset', 'arch'
        ]),
        keep(["msg"]),
        append(['msg'], wrap(lambda x: dict(Counter(x.lower()))))
    )


def train(message, init_letter_space):
    operation = etl()

    letter_space = init_letter_space.copy()

    (res, err) = operation(message)
    if res is not None:
        for letter, count in res.items():
            if letter not in letter_space:
                stats = Stats()
            else:
                stats = letter_space[letter]

            letter_space[letter] = stats.add_variable(count)

    return letter_space, message


def check(message: str):
    pass


__all__ = ["gen_model"]
