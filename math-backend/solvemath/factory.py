from solvemath.algebra_solver import AlgebraSolver
from solvemath.series_solver import SeriesSolver
from solvemath.trigonometry_solver import TrigonometrySolver

class SolverFactory:
    def get_solver_by_code(self, code):
        if code == 1:
            return AlgebraSolver()
        elif code == 2:
            return SeriesSolver()
        elif code == 3:
            return TrigonometrySolver()
        return None
