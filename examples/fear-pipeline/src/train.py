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
from pprint import pprint

from datarefinery.CombineOperations import sequential
from datarefinery.TupleOperations import keep
from datarefinery.tuple.Formats import csv_to_map

from Tarkin.models.freq.Stats import read_letter_space, save_letter_space
from Tarkin.models.freq.freq_model import gen_model
from Tarkin.core import pipeline

LETTERSPACE_FILEPATH = "input-data/letterspace.pkl"


def etl():
    proc = sequential(
        csv_to_map([
            'date', 'file', 'date2', 'log', 'app', 'beat', 'front', 'is_log',
            'msg', 'offset', 'arch'
            ], delimiter=";"),
        keep(["msg"])
    )

    def _just_msg(x):
        (res, err) = proc(x)
        if err is not None:
            print(x, err)
        return res['msg']

    return _just_msg


def train():
    letter_space = [read_letter_space(LETTERSPACE_FILEPATH)]
    op = pipeline(gen_model(etl()))

    for line in sys.stdin:
        letter_space = op(line, letter_space)

    save_letter_space(LETTERSPACE_FILEPATH, letter_space[0])
    pprint(letter_space)


if __name__ == '__main__':
    train()
