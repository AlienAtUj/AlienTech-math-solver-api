from .base import SolveMath
import math
import re

class GeometrySolver(SolveMath):
    def solve(self, equation: str) -> str:
        try:
            if "area of circle" in equation.lower():
                radius = float(re.findall(r'\d+', equation)[0])
                area = math.pi * radius ** 2
                return f"Area: {round(area, 2)}"
            return "Unsupported geometry problem."
        except Exception as e:
            return f"Error: {str(e)}"