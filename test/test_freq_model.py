from Tarkin.core import pipeline, train
from Tarkin.models.freq_model import gen_model as gen_freq_model
from Tarkin.models.freq_model import check as check_freq_model

from Tarkin.service.Stats import Stats

from datarefinery.CombineOperations import sequential
from datarefinery.TupleOperations import keep
from datarefinery.tuple.Formats import csv_to_map
from datarefinery.tuple.TupleDSL import compose

from pprint import pprint


def test_freq_train_model_empty():
    op = train()
    assert op is not None

    res = op("ble ble")
    assert res is None


def test_freq_run_model_empty():
    op = check_freq_model(None)
    assert op is not None

    res = op("ble ble")
    assert res is None


def _gen_letter_space(init):
    def _create_stats(l):
        s = Stats()
        for item in l:
            s.add_variable(item)
        return s
    return {k: _create_stats(v) for k, v in init.items()}


def test_freq_train_model():
    model = gen_freq_model()
    op = train(model)

    res = op("ble ble")
    assert res is not None
    letter_space = res[0]
    assert isinstance(letter_space, dict)

    expected_letter_space = _gen_letter_space({
        ' ': [1],
        'b': [2],
        'l': [2],
        'e': [2]
    })
    assert len(set(expected_letter_space) ^ set(letter_space)) == 0


def test_freq_run_model():
    letter_space = _gen_letter_space({
        ' ': [1],
        'b': [2],
        'l': [2],
        'e': [2]
    })

    model = check_freq_model(letter_space)
    op = pipeline(model)

    res = op("ble ble")
    assert res is not None
    assert res == 0


def _etl():
    proc = sequential(
        csv_to_map([
            'date', 'file', 'date2', 'log', 'app', 'beat', 'front', 'is_log',
            'msg', 'offset', 'arch'
        ]),
        keep(["msg"])
    )
    return compose(proc, lambda x, err: x['msg'])


def test_freq_model_basic():
    etl = _etl()
    model = gen_freq_model()
    op = train(model)

    # compose the model with their ETL better
    res = op(etl('"2001-01-01T23:51:03.294Z","/var/log/resources-server.log","2001-01-01T23:51:01.873Z","resources-store","resource","{""hostname"":""198-51-100-15"",""name"":""198-51-100-15"",""address"":""198-51-100-15"",""version"":""1.7.0""}","backend-server","log","01/01/2001 18:51:00.934 [b3ef51b16eaabddb894bc93822a37d0e] INFO module-n - Content-Type: application/json;charset=UTF-8","666111222","gothic"'))
    pprint(res)
    assert res is not None
    assert isinstance(res[0], dict)


def test_freq_model_basic_initialized():
    test_letter_stats = Stats()
    model = gen_freq_model(initial_letter_space={'0': test_letter_stats.add_variable(127)})

    op = pipeline(model)
    res = op('"2001-01-01T23:51:03.294Z","/var/log/resources-server.log","2001-01-01T23:51:01.873Z","resources-store","resource","{""hostname"":""198-51-100-15"",""name"":""198-51-100-15"",""address"":""198-51-100-15"",""version"":""1.7.0""}","backend-server","log","01/01/2001 18:51:00.934 [b3ef51b16eaabddb894bc93822a37d0e] INFO module-n - Content-Type: application/json;charset=UTF-8","666111222","gothic"')
    pprint(res)
    assert res is not None
    assert isinstance(res[0], dict)
    assert res[0].get('0').get_variance() == 7200


def test_freq_model_double_uninitialized():
    model = gen_freq_model()
    op = pipeline(model)

    res1 = op('"2001-01-01T23:51:03.294Z","/var/log/resources-server.log","2001-01-01T23:51:01.873Z","resources-store","resource","{""hostname"":""198-51-100-15"",""name"":""198-51-100-15"",""address"":""198-51-100-15"",""version"":""1.7.0""}","backend-server","log","01/01/2001 18:51:00.934 [b3ef51b16eaabddb894bc93822a37d0e] INFO module-n - Content-Type: application/json;charset=UTF-8","666111222","gothic"')
    print ("-----")
    res = op('"2001-01-01T23:52:03.294Z","/var/log/resources-server.log","2001-01-01T23:51:01.873Z","resources-store","resource","{""hostname"":""198-51-100-15"",""name"":""198-51-100-15"",""address"":""198-51-100-15"",""version"":""1.7.0""}","backend-server","log","01/01/2001 18:51:00.934 [b3ef51b36eaabddb894bc93822a37d0e] INFO module-n2 - Content-Type: application/json;charset=UTF-8","666111222","gothic"')

    pprint(res)
    assert res is not None
    assert isinstance(res[0], dict)


def test_freq_model_second_initialized():
    model = gen_freq_model()
    op = pipeline(model)

    res1 = op('"2001-01-01T23:51:03.294Z","/var/log/resources-server.log","2001-01-01T23:51:01.873Z","resources-store","resource","{""hostname"":""198-51-100-15"",""name"":""198-51-100-15"",""address"":""198-51-100-15"",""version"":""1.7.0""}","backend-server","log","01/01/2001 18:51:00.934 [b3ef51b16eaabddb894bc93822a37d0e] INFO module-n - Content-Type: application/json;charset=UTF-8","666111222","gothic"')
    pprint(res1)
    print ("-----")
    res = op('"2001-01-01T23:52:03.294Z","/var/log/resources-server.log","2001-01-01T23:51:01.873Z","resources-store","resource","{""hostname"":""198-51-100-15"",""name"":""198-51-100-15"",""address"":""198-51-100-15"",""version"":""1.7.0""}","backend-server","log","01/01/2001 18:51:00.934 [b3ef51b36eaabddb894bc93822a37d0e] INFO module-n2 - Content-Type: application/json;charset=UTF-8","666111222","gothic"'
             , initial_letter_space=res1[0])
    pprint(res)
    assert res is not None
    assert isinstance(res[0], dict)
    assert res[0].get('1').get_variance() == 0.5
    assert res[0].get('2').get_variance() == 0.5
    assert res[0].get('3').get_variance() == 0.5
