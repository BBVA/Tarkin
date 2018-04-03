from Tarkin.core import pipeline
from Tarkin.models.freq_model import gen_model as gen_freq_model
from Tarkin.models.freq_model import check as check_freq_model
from Tarkin.models.sent_model import check as check_sent_model

from datarefinery.CombineOperations import sequential
from datarefinery.TupleOperations import keep
from datarefinery.tuple.Formats import csv_to_map


def test_empty():
    op = pipeline(None)
    assert op is not None
    assert op(None) is None

    op = pipeline()
    assert op is not None
    assert op() is None


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


def test_multiple_models():
    model1 = gen_freq_model(_etl())
    model2 = check_sent_model()
    op = pipeline(model1, model2)

    res = op(
        '"2001-01-01T23:51:03.294Z","/var/log/resources-server.log","2001-01-01T23:51:01.873Z","resources-store","resource","{""hostname"":""198-51-100-15"",""name"":""198-51-100-15"",""address"":""198-51-100-15"",""version"":""1.7.0""}","backend-server","log","01/01/2001 18:51:00.934 [b3ef51b16eaabddb894bc93822a37d0e] INFO module-n - Content-Type: application/json;charset=UTF-8","666111222","gothic"')
    print(res)
    assert res is not None


def test_multiple_models_three():
    etl = _etl()
    model1 = gen_freq_model(etl)
    model2 = check_sent_model(etl)
    op = pipeline(model1, model2, model1)

    res = op(
        '"2001-01-01T23:51:03.294Z","/var/log/resources-server.log","2001-01-01T23:51:01.873Z","resources-store","resource","{""hostname"":""198-51-100-15"",""name"":""198-51-100-15"",""address"":""198-51-100-15"",""version"":""1.7.0""}","backend-server","log","01/01/2001 18:51:00.934 [b3ef51b16eaabddb894bc93822a37d0e] INFO module-n - Content-Type: application/json;charset=UTF-8","666111222","gothic"')
    print(res)
    assert res is not None


def test_train_and_run():
    op = pipeline(gen_freq_model())

    st = op("ble ble")
    st = op("hello world", st)

    op2 = pipeline(check_freq_model())
    score = op2("ble ble", st)

    assert 0.555555 - score[0] < 0.0000001


def test_train_run_and_reduce():
    op = pipeline(gen_freq_model())

    st = op("ble ble")
    st = op("hello world", st)

    op2 = pipeline(check_freq_model(), reductor=lambda x: next(x))
    score = op2("ble ble", st)

    assert 0.555555 - score < 0.0000001


def test_train_run_reduce_several():
    def reduc(x):
        return sum(x)
    op = pipeline(gen_freq_model(), gen_freq_model())

    st = op("ble ble")
    st = op("hello world", st)

    op2 = pipeline(check_freq_model(), check_freq_model(), reductor=reduc)
    score = op2("ble ble", st)

    assert score > 1
