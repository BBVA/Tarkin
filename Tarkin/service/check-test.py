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
from json import dumps

from service.check import surprise_model
from service.Stats import Stats, read_letter_space
from service.sentiment import load_sentiment_model

TEST_METRICS_FILE = "Tarkin/metrics/check-test-metrics.txt"

SENTI_DIC = "Tarkin/data/vocab/SentiWordNet_3.0.0_20130122.txt"
LETTER_SPACE = "Tarkin/input-data/letterspace.pkl"


def check_test():
    letter_space = read_letter_space(LETTER_SPACE)
    if letter_space is None:
        raise RuntimeError("A letterspace file is required and couldn't be found")

    surprise = surprise_model(letter_space)
    surprise_threshold = Stats()

    sentiment_model = load_sentiment_model(SENTI_DIC)

    for msg in sys.stdin:
        try:

            surprise_score = surprise(msg)

            surprise_max = surprise_threshold.max
            surprise_variance = surprise_threshold.get_std()
            if surprise_score > surprise_max - surprise_variance:
                sentiment_score = sentiment_model(msg)
                print(dumps({"surprise": surprise_score, "sentiment_score": sentiment_score}))

            surprise_threshold = surprise_threshold.add_variable(surprise_score)

        except:
            print(dumps({"surprise": 1, "sentiment_score": -1}))

        with open(TEST_METRICS_FILE, 'w') as metrics_output:
            print(surprise_threshold, file=metrics_output)


if __name__ == '__main__':
    check_test()
