from math import sqrt

import pytest

from computator import computate
from computator import input_schema
from computator import output_schema

class TestStatsExamples:
    STATS_GRAPH = {
        "n": lambda xs: len(xs),
        "m": lambda xs, n: sum(xs) / n,
        "m2": lambda xs, n: sum([x * x for x in xs]) / float(n),
        "v": lambda m, m2: m2 - (m * m)
    }

    def test_sg_input_schema(self):
        assert input_schema(self.STATS_GRAPH) == {"xs": True}

    def test_sg_output_schema(self):
        assert output_schema(self.STATS_GRAPH) == {'m': True, 'm2': True, 'n': True, 'v': True}

    def test_stats(self):
        results = computate(self.STATS_GRAPH, xs=[1, 2, 3, 6])

        assert results == {
            "m2" : 12.5,
            "m"  : 3,
            "n"  : 4,
            "v"  : 3.5
        }

    def test_missing_key(self):
        with pytest.raises(KeyError):
            computate(self.STATS_GRAPH, ys=[1, 2, 3])

    def test_extend_stats_graph(self):
        extended = self.STATS_GRAPH.copy()
        extended["sd"] = lambda v: sqrt(v)

        results = computate(extended, xs=[1, 2, 3, 6])

        assert results == {
            "m2" : 12.5,
            "m"  : 3,
            "n"  : 4,
            "v"  : 3.5,
            "sd" : 1.8708286933869707
        }

class TestDefnkExamples:

    @staticmethod
    def simple_fnk(a, b, c):
        return a + b + c

    @staticmethod
    def simple_opt_fnk(a, b, c=1):
        return a + b + c

    def test_simple_fnk(self):
        assert computate(self.simple_fnk, **{"a": 1, "b": 2, "c": 3}) == 6

    def test_defnk_missing_key(self):
        with pytest.raises(KeyError):
            computate(self.simple_fnk, **{"a": 1, "b": 2})

    def test_defnk_optional_default(self):
        assert computate(self.simple_opt_fnk, **{"a": 1, "b": 2}) == 4

    def test_defnk_optional_default_overridden(self):
        assert computate(self.simple_opt_fnk, **{"a": 1, "b": 2, "c": 2}) == 5
