import dataclasses


@dataclasses.dataclass
class Execution:
    execution_time: int
    input: str
    message: str
    status: int

    def __str__(self):
        pass
