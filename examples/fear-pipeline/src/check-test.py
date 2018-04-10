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
import os
import sys
from json import dumps as json_dumps

from datarefinery.CombineOperations import sequential
from datarefinery.TupleOperations import keep
from datarefinery.tuple.Formats import csv_to_map

from Tarkin.core import pipeline
from Tarkin.models.freq.Stats import Stats, read_letter_space
from Tarkin.models.freq.freq_model import check as check_freq
from Tarkin.models.sent_model import check as check_sent

from sentiment import load_sentiment_model


CHECK_METRICS_FILE = os.getenv('CHECK_METRICS_FILE', "metrics/check-metrics.txt")
SENTI_DIC = os.getenv('SENTI_DIC', "./data/vocab/SentiWordNet_3.0.0_20130122.txt")
LETTER_SPACE = os.getenv('LETTERSPACE_FILENAME', "./input-data/letterspace.pkl")


def _etl():
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


def _check_model_result():
    surprise_threshold = Stats()

    def _app(models):
        nonlocal surprise_threshold
        result = None
        try:
            surprise = next(models)

            surprise_max = surprise_threshold.max
            surprise_variance = surprise_threshold.get_std()
            if surprise > surprise_max - surprise_variance:
                sentiment = next(models)
                if sentiment <= 0:
                    result = {"surprise": surprise, "sentiment_score": sentiment}
            surprise_threshold = surprise_threshold.add_variable(surprise)
        except:
            return {"surprise": 1, "sentiment_score": -1}

        try:
            with open(CHECK_METRICS_FILE, 'a') as metrics_output:
                print(surprise_threshold, file=metrics_output)
        except:
            print(surprise_threshold, file=sys.stderr)
        return result

    return _app


def check():
    letter_space = read_letter_space(LETTER_SPACE)
    if letter_space is None:
        raise RuntimeError("A letterspace file is required and couldn't be found")

    sentiment_dict = load_sentiment_model(SENTI_DIC)
    if sentiment_dict is None:
        raise RuntimeError("A sentiment dict file is required and couldn't be found")

    s = [letter_space, sentiment_dict]

    surprise = check_freq()

    sentiment = check_sent()

    model_check = pipeline(surprise, sentiment, reductor=_check_model_result())

    for line in sys.stdin:
        res = model_check(line, s)
        if res is not None:
            res['msg'] = line
            print(json_dumps(res))


if __name__ == '__main__':
    check()
