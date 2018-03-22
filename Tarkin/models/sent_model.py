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

from typing import Callable

from datarefinery.CombineOperations import sequential
from datarefinery.TupleOperations import keep
from datarefinery.tuple.Formats import csv_to_map

from Tarkin.service.sentiment import load_sentiment_model

SENTI_DIC = "Tarkin/data/vocab/SentiWordNet_3.0.0_20130122.txt"


def gen_model(**kwargs):

    senti_file = kwargs.get('senti_file', SENTI_DIC)

    senti_model = load_sentiment_model(senti_file)

    def _app(*args):
        message = args[-1]
        return check(message, senti_model)

    return _app


# should probably have to be added as a parameter of gen_model or check
def etl():
    return sequential(
        csv_to_map([
            'date', 'file', 'date2', 'log', 'app', 'beat', 'front', 'is_log',
            'msg', 'offset', 'arch'
            ]),
        keep(["msg"])
    )


def check(message: str, sentiment_model: Callable):
    operation = etl()

    try:
        (res, err) = operation(message)
        msg = res['msg']

        sentiment_score = sentiment_model(msg)
    except:
        sentiment_score = -1

    return sentiment_score, message


__all__ = ["gen_model"]
