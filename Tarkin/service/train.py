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
import sys
from collections import Counter
from pprint import pprint

from datarefinery.CombineOperations import sequential
from datarefinery.TupleOperations import append, keep, wrap
from datarefinery.tuple.Formats import csv_to_map

from models.Stats import Stats, read_letter_space, save_letter_space

LETTERSPACE_FILEPATH = "Tarkin/input-data/letterspace.pkl"


def etl():
    return sequential(
        csv_to_map([
            'date', 'file', 'date2', 'log', 'app', 'beat', 'front', 'is_log',
            'msg', 'offset', 'arch'
            ]),
        keep(["msg"]),
        append(['msg'], wrap(lambda x: dict(Counter(x.lower()))))
    )


def train():
    letter_space = read_letter_space(LETTERSPACE_FILEPATH)
    if letter_space is None:
        letter_space = {}
    operation = etl()

    for line in sys.stdin:
        (res, err) = operation(line)
        if res is not None:
            for letter, count in res.items():
                if letter not in letter_space:
                    stats = Stats()
                else:
                    stats = letter_space[letter]

                letter_space[letter] = stats.add_variable(count)

    save_letter_space(LETTERSPACE_FILEPATH, letter_space)
    pprint(letter_space)


if __name__ == '__main__':
    train()
