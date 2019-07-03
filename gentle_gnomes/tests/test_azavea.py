from time import time


def test_request_data_exists(azavea):
    assert azavea.get_indicators()


def test_async_request_adds_to_pending(azavea):
    azavea.get_indicators(now=False)
    assert azavea.proxy._pending


def test_async_requests_perserve_order(azavea):
    indicators = azavea.get_indicators()
    scenarios = azavea.get_scenarios()

    azavea.get_indicators(now=False)
    azavea.get_scenarios(now=False)

    assert indicators, scenarios == azavea.proxy.collect()


def test_async_proxy_is_actually_doing_something(azavea):
    synct = time()
    azavea.get_indicators()
    azavea.get_indicators()
    azavea.get_indicators()
    synct = time() - synct

    asynct = time()
    azavea.get_indicators(now=False)
    azavea.get_indicators(now=False)
    azavea.get_indicators(now=False)
    azavea.proxy.collect()
    asynct = time() - asynct

    assert asynct < synct
