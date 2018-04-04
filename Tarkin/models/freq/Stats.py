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
import pickle
import os
import math


class Stats:

    def __init__(self):
        self.K = 0.0
        self.n = 0.0
        self.Ex = 0.0
        self.Ex2 = 0.0
        self.max = 0
        self.min = 0

    def add_variable(self, x: float):
        if self.n == 0:
            self.K = x
        self.n += 1
        self.Ex += x - self.K
        self.Ex2 += (x - self.K) * (x - self.K)

        if x > self.max:
            self.max = x
        if x < self.min:
            self.min = x
        return self

    def remove_variable(self, x):
        self.n = self.n - 1
        self.Ex -= (x - self.K)
        self.Ex2 -= (x - self.K) * (x - self.K)
        return self

    def get_mean_value(self):
        if self.n > 0:
            return self.K + self.Ex / self.n
        return 0

    def get_variance(self):
        if self.n > 1:
            return (self.Ex2 - (self.Ex*self.Ex)/self.n) / (self.n-1)
        return 0

    def get_std(self):
        return math.sqrt(self.get_variance()**2)

    def is_in_std(self, x):
        (lower, higher) = (
            self.get_mean_value() - self.get_std(),
            self.get_mean_value() + self.get_std()
        )
        if lower <= x <= higher:
            return 0
        return 1

    def __repr__(self):
        return """count: {} mean: {} variance: {} max: {} min: {}""".format(
            self.n, self.get_mean_value(), self.get_variance(),
            self.max, self.min
        )


def save_letter_space(path: str, letter_space: dict):
    with open(path, 'wb+') as output:
        pickle.dump(letter_space, output, pickle.HIGHEST_PROTOCOL)


def read_letter_space(path: str):
    try:
        if os.path.isfile(path):
            with open(path, 'rb') as input_file:
                letter_space = pickle.load(input_file)
            return letter_space
    except:
        return None
