import pytest

from computator import computate

class TestPlumbingDocExamples:
    STATS_GRAPH = {
        "n": lambda xs: len(xs),
        "m": lambda xs, n: sum(xs) / n,
        "m2": lambda xs, n: sum([x * x for x in xs]) / float(n),
        "v": lambda m, m2: m2 - (m * m)
    }

    def test_stats(self):
        results = computate(self.STATS_GRAPH, xs=[1, 2, 3, 6])

        assert results == {
            "xs" : [1, 2, 3, 6],
            "m2" : 12.5,
            "m"  : 3,
            "n"  : 4
        }

    def test_missing_key(self):
        with pytest.raises(KeyError):
            computate(self.STATS_GRAPH, ys=[1, 2, 3])
