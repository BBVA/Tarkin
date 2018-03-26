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


def gen_model(etl: Callable=lambda x: x, senti_file=SENTI_DIC) -> Callable:

    scoring_func = load_sentiment_model(senti_file)

    def _app(msg: str):
        return check(etl(msg), scoring_func)

    return _app


def check(message: str, sentiment_model: Callable):

    try:
        sentiment_score = sentiment_model(message)
    except:
        sentiment_score = -1

    return sentiment_score, message


__all__ = ["gen_model", "check"]
