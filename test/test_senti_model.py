from pytest import raises

from Tarkin.core import pipeline, train, compose
from Tarkin.models.sent_model import gen_model as gen_senti_model

from datarefinery.CombineOperations import sequential
from datarefinery.TupleOperations import keep
from datarefinery.tuple.Formats import csv_to_map

from pprint import pprint


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

    return compose(proc, _just_msg)


def test_train_senti_model():
    etl = _etl()
    model = gen_senti_model(etl)
    op = train(model)

    with raises(TypeError, message="Expecting TypeError: Sentiment model doesn't provide a train(msg, state) function"):
        op('"2001-01-01T23:51:03.294Z","/var/log/resources-server.log","2001-01-01T23:51:01.873Z","resources-store","resource","{""hostname"":""198-51-100-15"",""name"":""198-51-100-15"",""address"":""198-51-100-15"",""version"":""1.7.0""}","backend-server","log","01/01/2001 18:51:00.934 [b3ef51b16eaabddb894bc93822a37d0e] INFO module-n - Content-Type: application/json;charset=UTF-8","666111222","gothic"')


def test_check_senti_model_basic():
    model = gen_senti_model()
    op = pipeline(model)

    res = op('"2001-01-01T23:51:03.294Z","/var/log/resources-server.log","2001-01-01T23:51:01.873Z","resources-store","resource","{""hostname"":""198-51-100-15"",""name"":""198-51-100-15"",""address"":""198-51-100-15"",""version"":""1.7.0""}","backend-server","log","01/01/2001 18:51:00.934 [b3ef51b16eaabddb894bc93822a37d0e] INFO module-n - Content-Type: application/json;charset=UTF-8","666111222","gothic"')
    pprint(res)
    assert res is not None
    assert res[0] == 0.75


def test_senti_model_double():
    model = gen_senti_model()
    op = pipeline(model)

    res = op(
        '"2001-01-01T23:51:03.294Z","/var/log/resources-server.log","2001-01-01T23:51:01.873Z","resources-store","resource","{""hostname"":""198-51-100-15"",""name"":""198-51-100-15"",""address"":""198-51-100-15"",""version"":""1.7.0""}","backend-server","log","01/01/2001 18:51:00.934 [b3ef51b16eaabddb894bc93822a37d0e] INFO module-n - Content-Type: application/json;charset=UTF-8","666111222","gothic"')
    pprint(res)
    assert res is not None
    assert res[0] == 0.75

    res = op('"2001-01-01T23:52:03.294Z","/var/log/resources-server.log","2001-01-01T23:51:01.873Z","resources-store","resource","{""hostname"":""198-51-100-15"",""name"":""198-51-100-15"",""address"":""198-51-100-15"",""version"":""1.7.0""}","backend-server","log","01/01/2001 18:51:00.934 [b3ef51b36eaabddb894bc93822a37d0e] INFO module-n2 - Content-Type: error application/json;charset=UTF-8","666111222","gothic"')
    pprint(res)
    assert res is not None
    assert res[0] == 0.46875
