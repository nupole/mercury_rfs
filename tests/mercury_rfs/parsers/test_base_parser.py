import abc

import pytest

from mercury_rfs.parsers.base_parser import BaseParser


class TestBaseParser:
    def test_is_abstract_base_class(self) -> None:
        assert issubclass(BaseParser, abc.ABC)

    def test_cannot_be_instantiated(self) -> None:
        with pytest.raises(TypeError):
            BaseParser()  # type: ignore[abstract]
