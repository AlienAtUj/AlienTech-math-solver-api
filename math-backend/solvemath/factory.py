from solvemath.AlgebraSolver import AlgebraSolver
from solvemath.trigonometry import TrigonometrySolver
from solvemath.SeriesSolver import SeriesSolver

class SolverFactory:
    def __init__(self):
        self.solvers = {
            "algebra": AlgebraSolver(),
            "trig"  : TrigonometrySolver(),
            "series" : SeriesSolver(), 
        }

    def get_solver(self, input_text: str):
        input_text = input_text.lower()
        if any(keyword in input_text for keyword in [
             "equation", 
            "factor", "simplify", "surd", "rational", "/", "<", ">", "≥", "≤"
        ]):
            return self.solvers["algebra"]
        elif any(keyword in input_text for keyword in ['sin', 'cos', 'tan', 'triangle', 'verify identity']):
            return self.solvers["trig"]
        return None
