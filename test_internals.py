import pytest

from computator import computate
from computator import _get_defaults
from computator import Deadlock

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
        assert _get_defaults(self.no_args) == {}

    def test_no_defaults(self):
        assert _get_defaults(self.no_defaults) == {}

    def test_defaults(self):
        assert _get_defaults(self.defaults) == {"c": 1, "d": 2}

class TestExecuteComputation:

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

class TestComputate:

    def test_deadlock(self):
        graph = {"a": lambda b: 1, "b": lambda a: 2}
        with pytest.raises(Deadlock):
            computate(graph)
