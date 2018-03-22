from Tarkin.core import pipeline
from Tarkin.models.freq_model import gen_model as gen_freq_model

from Tarkin.service.Stats import Stats

from pprint import pprint


def test_freq_model_empty():
    model = gen_freq_model()
    op = pipeline(model)

    res = op("ble ble")
    print(res)
    assert res is not None
    assert isinstance(res[0], dict)
    assert res[0].keys().__len__() == 0


def test_freq_model_basic():
    model = gen_freq_model()
    op = pipeline(model)

    res = op('"2001-01-01T23:51:03.294Z","/var/log/resources-server.log","2001-01-01T23:51:01.873Z","resources-store","resource","{""hostname"":""198-51-100-15"",""name"":""198-51-100-15"",""address"":""198-51-100-15"",""version"":""1.7.0""}","backend-server","log","01/01/2001 18:51:00.934 [b3ef51b16eaabddb894bc93822a37d0e] INFO module-n - Content-Type: application/json;charset=UTF-8","666111222","gothic"')
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
