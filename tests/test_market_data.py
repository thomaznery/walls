from market.MarketData import MarketData


def test_conntect_rt():
    md = MarketData()
    assert(isinstance(md.last("wdoq21"), str))
