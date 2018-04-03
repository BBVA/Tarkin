from Tarkin.core import pipeline
from Tarkin.models.freq_model import gen_model as gen_freq_model
from Tarkin.models.freq_model import check as check_freq_model

from models.Stats import Stats

from datarefinery.CombineOperations import sequential
from datarefinery.TupleOperations import keep
from datarefinery.tuple.Formats import csv_to_map


def test_freq_run_model_empty():
    # You can check a model without etl
    op = check_freq_model(None)
    # but will return a function
    assert op is not None

    # You can check with empty letterspace
    res = op("ble ble", None)
    # But is always strange
    assert res == 1.0


def _gen_letter_space(init):
    """
    Create an letter space based on the stats of the elements passed in init.
    :param init:
    :return:
    """
    def _create_stats(l):
        s = Stats()
        for item in l:
            s.add_variable(item)
        return s
    return {k: _create_stats(v) for k, v in init.items()}


def test_freq_train_model():
    model = gen_freq_model(lambda x: x)
    op = pipeline(model)

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


def test_freq_model_run():
    letter_space = _gen_letter_space({
        ' ': [1],
        'b': [2],
        'l': [2],
        'e': [2]
    })

    model = check_freq_model(lambda x: x)
    op = pipeline(model)

    res = op("ble ble", [letter_space])
    assert res is not None
    assert res == [0]


def _etl():
    """
    Provide an etl function for this example.
    :return:
    """
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


def test_freq_model_no_initial_state():
    etl = _etl()
    model = gen_freq_model(etl)
    op = pipeline(model)

    res = op('"2001-01-01T23:51:03.294Z","/var/log/resources-server.log","2001-01-01T23:51:01.873Z","resources-store","resource","{""hostname"":""198-51-100-15"",""name"":""198-51-100-15"",""address"":""198-51-100-15"",""version"":""1.7.0""}","backend-server","log","01/01/2001 18:51:00.934 [b3ef51b16eaabddb894bc93822a37d0e] INFO module-n - Content-Type: application/json;charset=UTF-8","666111222","gothic"')

    assert res is not None
    assert isinstance(res[0], dict)


def test_freq_model_initial_state_and_etl():
    letter_space = _gen_letter_space({
        ' ': [1],
        'b': [2],
        'l': [2],
        'e': [2]
    })
    etl = _etl()
    model = gen_freq_model(etl)
    op = pipeline(model)

    msg = '"2001-01-01T23:51:03.294Z","/var/log/resources-server.log","2001-01-01T23:51:01.873Z","resources-store","resource","{""hostname"":""198-51-100-15"",""name"":""198-51-100-15"",""address"":""198-51-100-15"",""version"":""1.7.0""}","backend-server","log","01/01/2001 18:51:00.934 [b3ef51b16eaabddb894bc93822a37d0e] INFO module-n - Content-Type: application/json;charset=UTF-8","666111222","gothic"'
    res = op(msg, [letter_space])
    print(res)
    assert res is not None
    assert isinstance(res[0], dict)


def test_freq_model_initial_state():
    initial_letter_space = _gen_letter_space({
        ' ': [1],
        'b': [2],
        'l': [2],
        'e': [2]
    })
    model = gen_freq_model(lambda x: x)
    op = pipeline(model)

    msg = 'hi world'
    res = op(msg, [initial_letter_space])

    expected_letter_space = _gen_letter_space({
        ' ': [1, 1],
        'b': [2],
        'l': [2, 1],
        'e': [2],
        'h': [1],
        'i': [1],
        'w': [1],
        'o': [1],
        'r': [1],
        'd': [1]
    })

    assert res is not None
    assert isinstance(res[0], dict)

    assert len(set(expected_letter_space) ^ set(res[0])) == 0


def test_freq_model_two_steps_train():
    expected_letter_space = _gen_letter_space({
        ' ': [1, 1],
        'b': [2],
        'l': [2, 1],
        'e': [2],
        'h': [1],
        'i': [1],
        'w': [1],
        'o': [1],
        'r': [1],
        'd': [1]
    })

    model = gen_freq_model(lambda x: x)
    op = pipeline(model)

    re1 = op('ble ble')
    res = op('hi world', re1)

    assert res is not None
    assert isinstance(res[0], dict)

    assert len(set(expected_letter_space) ^ set(res[0])) == 0
