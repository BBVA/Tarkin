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


def gen_model(etl: Callable=lambda x: x) -> Callable:
    """
    f(etl) -> f(Optional[state]) -> state'

    :param etl: A Callable instance of a transformation function for the message
    :return:
    """

    def _app(scoring_dict: str=SENTI_DIC):

        scoring_func = load_sentiment_model(scoring_dict)

        return check(etl, scoring_func)

    return _app


def check(etl: Callable, sentiment_model: Callable):
    """
    f(etl, state) -> f(msg) -> (float, msg)

    #TODO Passing a Callable with state like sentiment_model feels wrong

    :param etl: A Callable instance of a transformation function for the message
    :param sentiment_model: A Callable instance of the scoring model
    :return: A Callable instance of the scoring function
    """

    def _app(message: str):
        """

        :param message: The message to be scored
        :return: The score given by the sentiment model to the received message
        """

        if sentiment_model is None:
            return lambda *x: None, message

        try:
            sentiment_score = sentiment_model(etl(message))
        except:
            sentiment_score = -1

        return sentiment_score

    return _app


__all__ = ["gen_model"]
