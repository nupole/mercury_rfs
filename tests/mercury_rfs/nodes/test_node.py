import abc

import pytest

from mercury_rfs.nodes.node import Node


class TestNode:
    def test_node_is_abstract_base_class(self) -> None:
        assert issubclass(Node, abc.ABC)

    def test_node_cannot_be_instantiated(self) -> None:
        with pytest.raises(TypeError):
            Node(name="node", description="description") # type: ignore[abstract]
