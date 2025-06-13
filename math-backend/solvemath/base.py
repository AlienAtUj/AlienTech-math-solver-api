from abc import ABC, abstractmethod

class SolveMath(ABC):
    @abstractmethod
    def solve(self, equation: str) -> str:
        """Solve mathematical equations
        Args:
            equation: The equation to solve
        Returns:
            str: Formatted solution
        """
        pass