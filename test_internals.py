import pytest

from computator import computate

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
