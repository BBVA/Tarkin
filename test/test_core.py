from Tarkin.core import pipeline
from Tarkin.models.freq_model import gen_model as gen_freq_model
from Tarkin.models.sent_model import gen_model as gen_senti_model

from pprint import pprint


def test_empty():
    op = pipeline(None)
    assert op is not None
    assert op(None) is None

    op = pipeline()
    assert op is not None
    assert op() is None


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
