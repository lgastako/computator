import pytest

from computator import computate
from computator import get_defaults

class TestGetDefaults:

    @staticmethod
    def no_args():
        pass

    @staticmethod
    def no_defaults(a, b):
        pass

    @staticmethod
    def defaults(a, b, c=1, d=2):
        pass

    def test_no_args(self):
        assert get_defaults(self.no_args) == {}

    def test_no_defaults(self):
        assert get_defaults(self.no_defaults) == {}

    def test_defaults(self):
        assert get_defaults(self.defaults) == {"c": 1, "d": 2}

class TestComputateFunc:

    def test_missing_key(self):
        graph = {"a": lambda b: "c"}
        with pytest.raises(KeyError):
            computate(graph)

    def test_single_node_fulfillment(self):
        graph = {"a": lambda b: "c"}
        assert computate(graph, b=1) == {"a": "c"}

    def test_single_node_result(self):
        graph = {"a": lambda b: b * 3}
        assert computate(graph, b=2) == {"a": 6}
