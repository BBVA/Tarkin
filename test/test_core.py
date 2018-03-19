from Tarkin.core import pipeline
from Tarkin.models.stats_model import stats_model


def test_empty():
    op = pipeline(None)
    assert op is not None
    assert op(None) is None

    op = pipeline()
    assert op is not None
    assert op() is None


def test_stats_model():
    model = stats_model({})
    op = pipeline(model)

    res = op("ble ble")
    print(res)
    assert res is not None
    assert res is 0
