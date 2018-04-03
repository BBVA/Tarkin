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
from statistics import mean
from json import dumps as json_dumps

from datarefinery.CombineOperations import sequential
from datarefinery.TupleOperations import keep
from datarefinery.tuple.Formats import csv_to_map

from models.Stats import Stats, read_letter_space
from Tarkin.service.sentiment import load_sentiment_model


CHECK_METRICS_FILE = "Tarkin/metrics/check-metrics.txt"

SENTI_DIC = "Tarkin/data/vocab/SentiWordNet_3.0.0_20130122.txt"
LETTER_SPACE = "Tarkin/input-data/letterspace.pkl"


def etl():
    return sequential(
        csv_to_map([
            'date', 'file', 'date2', 'log', 'app', 'beat', 'front', 'is_log',
            'msg', 'offset', 'arch'
            ]),
        keep(["msg"])
    )


def surprise_model(letter_space):
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


def check():

    letter_space = read_letter_space(LETTER_SPACE)
    if letter_space is None:
        raise RuntimeError("A letterspace file is required and couldn't be found")
    operation = etl()
    surprise = surprise_model(letter_space)
    surprise_threshold = Stats()

    sentiment_model = load_sentiment_model(SENTI_DIC)

    for line in sys.stdin:
        try:
            (res, err) = operation(line)
            msg = res['msg']
            surprise_score = surprise(msg)

            surprise_max = surprise_threshold.max
            surprise_variance = surprise_threshold.get_std()
            if surprise_score > surprise_max - surprise_variance:
                sentiment_score = sentiment_model(msg)
                if sentiment_score <= 0:
                    print(json_dumps({"surprise": surprise_score, "sentiment_score": sentiment_score}))
            surprise_threshold = surprise_threshold.add_variable(surprise_score)

        except:
            print(json_dumps({"surprise": 1, "sentiment_score": -1}))

    with open(CHECK_METRICS_FILE, 'w') as metrics_output:
        print(surprise_threshold, file=metrics_output)


if __name__ == '__main__':
    check()
