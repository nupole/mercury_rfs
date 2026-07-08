import abc
import dataclasses


@dataclasses.dataclass
class Node(abc.ABC):
    name: str
    description: str
    offset: int | None = None

    @property
    @abc.abstractmethod
    def size(self) -> int:
        ...
