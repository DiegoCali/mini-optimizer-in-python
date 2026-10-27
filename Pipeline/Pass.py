from abc import ABC
from IRepresentation import Program

class Pass(ABC):
    def __init__(self, name: str):
        self.name = name

    def process(self, program: Program) -> Program:
        raise NotImplementedError("Subclasses must implement the run method.")
    
    def __str__(self) -> str:
        return f"Pass(name={self.name})"