import re

import pytest

from mercury_rfs.nodes.node import Node
from mercury_rfs.nodes.register_file import RegisterFile


class TestRegisterFile:
    def test_register_file_is_node(self) -> None:
        assert issubclass(RegisterFile, Node)

    def test_register_file_with_defaults(self) -> None:
        register_file = RegisterFile(name="top_level", description="Top-level")
        assert register_file.name == "top_level"
        assert register_file.description == "Top-level"
        assert register_file.offset is None
        assert register_file.file_name == ""
        assert register_file.children == []

    def test_register_file_with_values(self) -> None:
        child = RegisterFile(
            name="sub_level", description="Sub-level", file_name="file_name.ext"
        )
        register_file = RegisterFile(
            name="top_level",
            description="Top-level",
            offset=4,
            file_name="file_name.ext",
            children=[child],
        )
        assert register_file.name == "top_level"
        assert register_file.description == "Top-level"
        assert register_file.offset == 4
        assert register_file.file_name == "file_name.ext"
        assert register_file.children == [child]

    def test_register_file_without_name(self) -> None:
        with pytest.raises(
            TypeError,
            match=re.escape(
                "RegisterFile.__init__() missing 1 required positional argument: 'name'"
            ),
        ):
            RegisterFile(description="Top-level") # type: ignore[call-arg]

    def test_register_file_without_description(self) -> None:
        with pytest.raises(
            TypeError,
            match=re.escape(
                "RegisterFile.__init__() missing 1 required positional argument: 'description'"
            ),
        ):
            RegisterFile(name="top_level") # type: ignore[call-arg]

    def test_register_file_size(self) -> None:
        register_file = RegisterFile(name="top_level", description="Top-level")
        assert register_file.size == 0
