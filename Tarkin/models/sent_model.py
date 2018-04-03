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

from typing import Callable, Tuple

from spacy import load as spacy_load


def check(etl: Callable = None):
    """
    f(etl) -> f(msg, state) -> float

    :param etl: A Callable instance of a transformation function for the message
    :return: A Callable instance of the scoring function
    """

    if etl is None:
        etl = lambda x: x

    nlp = spacy_load('en')

    def _tokenize(msg):
        return [
            token.lower_ for token in nlp(msg)
            if not token.is_punct | token.is_space
        ]

    def _check_word(word, neg, pos):
        if word in neg:
            neg_score = neg[word]
        else:
            neg_score = 0

        if word in pos:
            pos_score = pos[word]
        else:
            pos_score = 0

        return pos_score + neg_score

    def _check_msg(msg, neg, pos):
        msg_scores = [_check_word(w, neg, pos) for w in _tokenize(msg)]
        return sum(msg_scores)

    def _app(message: str, model_state: Tuple[dict, dict] = None):
        """
        :param message: The message to be scored
        :return: The score given by the sentiment model to the received message
        """
        if model_state is None:
            (neg, pos) = ({}, {})
        else:
            (neg, pos) = model_state

        try:
            sentiment_score = _check_msg(etl(message), neg, pos)
        except:
            sentiment_score = -1

        return sentiment_score

    return _app


__all__ = ["check"]
