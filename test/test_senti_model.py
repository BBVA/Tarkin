from Tarkin.core import pipeline
from Tarkin.models.sent_model import gen_model as gen_senti_model

from pprint import pprint


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
