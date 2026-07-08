import abc
import os
from typing import Any

from mercury_rfs.nodes.register_file import RegisterFile
from mercury_rfs.nodes.register import RegisterAccess, RegisterField, Register


class BaseParser(abc.ABC):
    @abc.abstractmethod
    def load(self, path: str) -> dict[str, Any]: ...

    def parse_register_file(self, name: str, file_name: str) -> RegisterFile:
        path = os.path.abspath(file_name)
        dictionary = self.load(path)
        description = dictionary["description"]
        register_file = RegisterFile(
            name=name, description=description, file_name=file_name
        )
        for key, value in dictionary.items():
            if isinstance(value, dict):
                node_type = value["type"]
                if node_type == "register_file":
                    register_file.children.append(
                        self.parse_register_file(key, value["file_name"])
                    )
                elif node_type == "register":
                    register_file.children.append(
                        self._parse_register(key, value)
                    )
                else:
                    raise ValueError(
                        f"Unknown/missing type for {key}: {node_type!r}"
                    )
        return register_file

    def _parse_register(
        self, name: str, dictionary: dict[str, Any]
    ) -> Register:
        description = dictionary["description"]
        offset = dictionary.get("offset")
        if offset:
            offset = int(offset)
        register = Register(name=name, description=description, offset=offset)
        register_field_offset = 0
        for key, value in dictionary.items():
            if isinstance(value, dict):
                register_field = self._parse_register_field(
                    key, value, register_field_offset
                )
                if register_field_offset + register_field.width > 32:
                    raise ValueError(
                        f"Register {name}, field {key} overflows register width"
                    )
                register.fields.append(register_field)
                register_field_offset += register_field.width
        return register

    def _parse_register_field(
        self, name: str, dictionary: dict[str, Any], offset: int
    ) -> RegisterField:
        description = dictionary["description"]
        width = int(dictionary.get("width", 1))
        reset = int(dictionary.get("reset", 0))
        sw_access = RegisterAccess(dictionary.get("sw_access", "rw"))
        hw_access = RegisterAccess(dictionary.get("hw_access", "ro"))
        return RegisterField(
            name=name,
            description=description,
            width=width,
            offset=offset,
            reset=reset,
            sw_access=sw_access,
            hw_access=hw_access,
        )
