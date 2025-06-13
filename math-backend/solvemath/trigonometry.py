import sympy
from solvemath.base import SolveMath
from typing import Tuple
import re
from sympy import symbols, sin, cos, tan, sec, csc, cot, asin, acos, atan, Eq, solveset, S

class TrigonometrySolver(SolveMath):
    def solve(self, problem_text: str, variable: str = 'x') -> Tuple[str, sympy.Expr | None]:
        print(f"📐 TrigonometrySolver activated for: {problem_text}")
        text = problem_text.lower()
        steps = []
        x = symbols(variable)

        try:

            if any(fn in text for fn in ['sin', 'cos', 'tan', 'csc', 'sec', 'cot']):
                
                steps.append("📘 Trigonometric Equation Detected")
                
                expr = self._extract_equation(text, variable)
                if not expr:
                    return "❌ Could not parse equation. Try 'solve sin(x) = 0.5'.", None

                steps.append(f"  Equation: {expr} = 0")
                solutions = solveset(expr, x, domain=S.Reals)
                simplified_solutions = [sympy.simplify(s) for s in solutions]
                
                if not simplified_solutions:
                    steps.append("  No real solutions found.")
                else:
                    steps.append("  Solutions (general):")
                    for sol in simplified_solutions:
                        steps.append(f"    {variable} = {sol} + 2πn, n ∈ ℤ")
                
                return '\n'.join(steps), expr

           
            elif any(word in text for word in ['identity', 'verify', 'pythagorean']):
                steps.append("📘 Identity Verification Detected")
               
                expr = self._extract_identity(text)
                if not expr:
                    return "❌ Could not parse identity. Try 'verify sin²(x) + cos²(x) = 1'.", None
                
                lhs, rhs = expr.lhs, expr.rhs
                simplified_lhs = sympy.simplify(lhs)
                steps.append(f"  LHS: {lhs} → {simplified_lhs}")
                steps.append(f"  RHS: {rhs}")
                if simplified_lhs == rhs:
                    steps.append("✅ Identity is valid.")
                else:
                    steps.append("❌ Identity could not be verified.")
                return '\n'.join(steps), expr

          
            elif any(word in text for word in ['triangle', 'hypotenuse', 'angle of elevation']):
                steps.append("📘 Right Triangle Problem Detected")
                
                known_values = self._extract_triangle_values(text)
                if not known_values:
                    return "❌ Specify known values like 'opposite=3 angle=30°'.", None
                
             
                result = self._solve_triangle(known_values, steps)
                return '\n'.join(steps), None

           
            elif any(word in text for word in ['degrees to radians', 'radians to degrees']):
                steps.append("📘 Angle Conversion Detected")
               
                value = self._extract_number(text)
                if "degrees to radians" in text:
                    converted = sympy.rad(value)
                    steps.append(f"  {value}° → {converted} radians")
                else:
                    converted = sympy.deg(value)
                    steps.append(f"  {value} radians → {converted}°")
                return '\n'.join(steps), None

            return "❌ Could not identify trigonometry problem. Try: 'solve sin(x) = 0.5', 'verify identity', or 'find hypotenuse'.", None

        except Exception as e:
            print(f"❌ TrigonometrySolver Error: {e}")
            return f"❌ Error: {str(e)}", None


    def _extract_equation(self, text: str, variable: str) -> sympy.Expr | None:
        """Extract equation like 'sin(x) = 0.5'."""
        try:
          
            clean_text = re.sub(r'solve\s+', '', text)
          
            clean_text = re.sub(r'([a-z]+)([^a-z ])', r'\1(\2)', clean_text)
           
            clean_text = re.sub(r'([a-z]+)²', r'\1**2', clean_text)
            lhs, rhs = clean_text.split('=')
            return sympy.sympify(f"{lhs} - ({rhs})")
        except:
            return None

    def _extract_identity(self, text: str) -> sympy.Eq | None:
        """Extract identity like 'sin²(x) + cos²(x) = 1'."""
        try:
            clean_text = re.sub(r'verify\s+', '', text)
            lhs, rhs = clean_text.split('=')
            return Eq(sympy.sympify(lhs), sympy.sympify(rhs))
        except:
            return None

    def _extract_triangle_values(self, text: str) -> dict:
        """Extract key-value pairs like 'opposite=3 angle=30°'."""
        known = {}
       
        matches = re.finditer(r'(\w+)=([0-9.°]+)', text)
        for m in matches:
            key, val = m.groups()
            known[key] = float(val.replace('°', '')) if '°' in val else float(val)
        return known

    def _solve_triangle(self, known: dict, steps: list) -> dict:
        """Solve right triangle using SOH-CAH-TOA."""
      
        results = {}
        
        if 'angle' in known:
            theta = sympy.rad(known['angle'])
            steps.append(f"  Angle θ = {known['angle']}° → {theta:.2f} radians")
        
        
        if 'opposite' in known and 'angle' in known:
            hyp = known['opposite'] / sympy.sin(theta)
            results['hypotenuse'] = hyp
            steps.append(f"  sin(θ) = opposite/hypotenuse → hypotenuse = {hyp:.2f}")
        
       
        if 'adjacent' in known and 'hypotenuse' in known:
            theta = sympy.acos(known['adjacent'] / known['hypotenuse'])
            results['angle'] = sympy.deg(theta)
            steps.append(f"  cos(θ) = adjacent/hypotenuse → θ = {results['angle']:.2f}°")
        
       
        return results

    def _extract_number(self, text: str) -> float:
        """Extract the first number from text."""
        match = re.search(r'([0-9.]+)', text)
        return float(match.group(1)) if match else 0.0