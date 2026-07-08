import dataclasses

from mercury_rfs.nodes.node import Node


@dataclasses.dataclass
class RegisterFile(Node):
    file_name: str = ""
    children: list[Node] = dataclasses.field(default_factory=list)

    @property
    def size(self) -> int:
        return 0
