import dataclasses
import enum

from mercury_rfs.nodes.node import Node


class RegisterAccess(enum.Enum):
    RW = "rw"
    RO = "ro"
    WO = "wo"


@dataclasses.dataclass
class RegisterField(Node):
    width: int = 1
    reset: int = 0
    sw_access: RegisterAccess = RegisterAccess.RW
    hw_access: RegisterAccess = RegisterAccess.RO

    @property
    def size(self) -> int:
        raise NotImplementedError


@dataclasses.dataclass
class Register(Node):
    fields: list[RegisterField] = dataclasses.field(default_factory=list)

    @property
    def size(self) -> int:
        return 4
