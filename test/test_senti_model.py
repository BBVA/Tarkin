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
from Tarkin.core import pipeline
from Tarkin.models.sent_model import check as check_senti_model

from datarefinery.CombineOperations import sequential
from datarefinery.TupleOperations import keep
from datarefinery.tuple.Formats import csv_to_map


def _etl():
    proc = sequential(
        csv_to_map([
            'date', 'file', 'date2', 'log', 'app', 'beat', 'front', 'is_log',
            'msg', 'offset', 'arch'
            ]),
        keep(["msg"])
    )

    def _just_msg(x):
        (res, err) = x
        return res['msg']

    return lambda x: _just_msg(proc(x))


def test_senti_model_run():
    model = check_senti_model(_etl())
    op = pipeline(model)

    neg = {"error": 0.28125}
    pos = {"info": 0.75}

    res = op(
        '"2001-01-01T23:51:03.294Z","/var/log/resources-server.log","2001-01-01T23:51:01.873Z","resources-store","resource","{""hostname"":""198-51-100-15"",""name"":""198-51-100-15"",""address"":""198-51-100-15"",""version"":""1.7.0""}","backend-server","log","01/01/2001 18:51:00.934 [b3ef51b16eaabddb894bc93822a37d0e] INFO module-n - Content-Type: application/json;charset=UTF-8","666111222","gothic"',
        [(neg, pos)]
    )

    assert res is not None
    assert 0.75 == res[0]


def test_senti_model_twice():
    model = check_senti_model()
    op = pipeline(model)

    neg = {"error": -0.28125}
    pos = {"info": 0.75}

    res = op(
        '"2001-01-01T23:51:03.294Z","/var/log/resources-server.log","2001-01-01T23:51:01.873Z","resources-store","resource","{""hostname"":""198-51-100-15"",""name"":""198-51-100-15"",""address"":""198-51-100-15"",""version"":""1.7.0""}","backend-server","log","01/01/2001 18:51:00.934 [b3ef51b16eaabddb894bc93822a37d0e] INFO module-n - Content-Type: application/json;charset=UTF-8","666111222","gothic"',
        [(neg, pos)]
    )
    print(res)
    assert res is not None
    assert res[0] == 0.75

    res = op(
        '"2001-01-01T23:52:03.294Z","/var/log/resources-server.log","2001-01-01T23:51:01.873Z","resources-store","resource","{""hostname"":""198-51-100-15"",""name"":""198-51-100-15"",""address"":""198-51-100-15"",""version"":""1.7.0""}","backend-server","log","01/01/2001 18:51:00.934 [b3ef51b36eaabddb894bc93822a37d0e] INFO module-n2 - Content-Type: error application/json;charset=UTF-8","666111222","gothic"',
        [(neg, pos)]
    )
    print(res)
    assert res is not None
    assert res[0] == 0.46875
