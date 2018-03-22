from Tarkin.core import pipeline
from Tarkin.models.freq_model import gen_model as gen_freq_model
from Tarkin.models.sent_model import gen_model as gen_senti_model

from pprint import pprint

from Tarkin.service.Stats import Stats


def test_empty():
    op = pipeline(None)
    assert op is not None
    assert op(None) is None

    op = pipeline()
    assert op is not None
    assert op() is None


def test_stats_model_empty():
    model = gen_freq_model()
    op = pipeline(model)

    res = op("ble ble")
    print(res)
    assert res is not None
    assert isinstance(res[0], dict)
    assert res[0].keys().__len__() == 0

def test_stats_model_basic():
    model = gen_freq_model()
    op = pipeline(model)

    res = op('"2001-01-01T23:51:03.294Z","/var/log/resources-server.log","2001-01-01T23:51:01.873Z","resources-store","resource","{""hostname"":""198-51-100-15"",""name"":""198-51-100-15"",""address"":""198-51-100-15"",""version"":""1.7.0""}","backend-server","log","01/01/2001 18:51:00.934 [b3ef51b16eaabddb894bc93822a37d0e] INFO module-n - Content-Type: application/json;charset=UTF-8","666111222","gothic"')
    pprint(res)
    assert res is not None
    assert isinstance(res[0], dict)

def test_stats_model_basic_initialized():
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


def test_senti_model_basic():
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


def test_multiple_models():
    model1 = gen_freq_model()
    model2 = gen_senti_model()
    op = pipeline(model1, model2)

    res = op(
        '"2001-01-01T23:51:03.294Z","/var/log/resources-server.log","2001-01-01T23:51:01.873Z","resources-store","resource","{""hostname"":""198-51-100-15"",""name"":""198-51-100-15"",""address"":""198-51-100-15"",""version"":""1.7.0""}","backend-server","log","01/01/2001 18:51:00.934 [b3ef51b16eaabddb894bc93822a37d0e] INFO module-n - Content-Type: application/json;charset=UTF-8","666111222","gothic"')
    pprint(res)
    assert res is not None

def test_multiple_models_three():
    model1 = gen_freq_model()
    model2 = gen_senti_model()
    op = pipeline(model1, model2, model1)

    res = op(
        '"2001-01-01T23:51:03.294Z","/var/log/resources-server.log","2001-01-01T23:51:01.873Z","resources-store","resource","{""hostname"":""198-51-100-15"",""name"":""198-51-100-15"",""address"":""198-51-100-15"",""version"":""1.7.0""}","backend-server","log","01/01/2001 18:51:00.934 [b3ef51b16eaabddb894bc93822a37d0e] INFO module-n - Content-Type: application/json;charset=UTF-8","666111222","gothic"')
    pprint(res)
    assert res is not None
