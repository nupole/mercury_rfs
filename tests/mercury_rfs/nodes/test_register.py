import enum
import re

import pytest

from mercury_rfs.nodes.node import Node
from mercury_rfs.nodes.register import RegisterAccess, RegisterField, Register


class TestRegisterAccess:
    def test_register_access_is_enum(self) -> None:
        assert issubclass(RegisterAccess, enum.Enum)

    @pytest.mark.parametrize(
        "value, expected",
        [
            ("rw", RegisterAccess.RW),
            ("ro", RegisterAccess.RO),
            ("wo", RegisterAccess.WO),
        ],
    )
    def test_values(self, value: str, expected: RegisterAccess) -> None:
        assert RegisterAccess(value) is expected

    def test_invalid_value(self) -> None:
        with pytest.raises(ValueError):
            RegisterAccess("invalid_value")


class TestRegisterField:
    def test_register_field_is_node(self) -> None:
        assert issubclass(RegisterField, Node)

    def test_register_field_with_defaults(self) -> None:
        register_field = RegisterField(name="enable", description="Enable")
        assert register_field.name == "enable"
        assert register_field.description == "Enable"
        assert register_field.offset is None
        assert register_field.width == 1
        assert register_field.reset == 0
        assert register_field.sw_access is RegisterAccess.RW
        assert register_field.hw_access is RegisterAccess.RO

    def test_register_field_with_values(self) -> None:
        register_field = RegisterField(
            name="mode",
            description="Mode",
            offset=4,
            width=3,
            reset=2,
            sw_access=RegisterAccess.RO,
            hw_access=RegisterAccess.WO,
        )
        assert register_field.name == "mode"
        assert register_field.description == "Mode"
        assert register_field.offset == 4
        assert register_field.width == 3
        assert register_field.reset == 2
        assert register_field.sw_access is RegisterAccess.RO
        assert register_field.hw_access is RegisterAccess.WO

    def test_register_field_without_name(self) -> None:
        with pytest.raises(
            TypeError,
            match=re.escape(
                "RegisterField.__init__() missing 1 required positional argument: 'name'"
            ),
        ):
            RegisterField(description="field") # type: ignore[call-arg]

    def test_register_field_without_description(self) -> None:
        with pytest.raises(
            TypeError,
            match=re.escape(
                "RegisterField.__init__() missing 1 required positional argument: 'description'"
            ),
        ):
            RegisterField(name="field") # type: ignore[call-arg]

    def test_register_field_size_is_not_implemented(self) -> None:
        register_field = RegisterField(name="field", description="description")
        with pytest.raises(NotImplementedError):
            register_field.size


class TestRegister:
    def test_register_is_node(self) -> None:
        assert issubclass(Register, Node)

    def test_create_register_with_defaults(self) -> None:
        register = Register(name="register", description="Register")
        assert register.name == "register"
        assert register.description == "Register"
        assert register.offset is None
        assert register.fields == []

    def test_create_register_with_values(self) -> None:
        field = RegisterField(name="field", description="Field")
        register = Register(
            name="register", description="Register", offset=4, fields=[field]
        )
        assert register.name == "register"
        assert register.description == "Register"
        assert register.offset == 4
        assert register.fields == [field]

    def test_register_without_name(self) -> None:
        with pytest.raises(
            TypeError,
            match=re.escape(
                "Register.__init__() missing 1 required positional argument: 'name'"
            ),
        ):
            Register(description="field") # type: ignore[call-arg]

    def test_register_without_description(self) -> None:
        with pytest.raises(
            TypeError,
            match=re.escape(
                "Register.__init__() missing 1 required positional argument: 'description'"
            ),
        ):
            Register(name="field") # type: ignore[call-arg]

    def test_register_size(self) -> None:
        register = Register(name="register", description="Register")
        assert register.size == 4
