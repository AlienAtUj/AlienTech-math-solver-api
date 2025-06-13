import sympy
import re
from solvemath.base import SolveMath
from solvemath.utils import extract_equations
from solvemath.utils import extract_equations_from_text
from sympy.solvers.inequalities import solve_univariate_inequality

class AlgebraSolver(SolveMath):
    def solve(self, equation_text: str, variable: str = 'x') -> tuple[str, sympy.Expr | None]:
        print("✅ AlgebraSolver is active")  
        text = equation_text.lower()
        text = re.sub(r'\bsolve\b|\bequation\b', '', text)
        eq_strings = extract_equations(text)
        sym = sympy.Symbol(variable)

        try:

            
            if any(op in text for op in ['<', '>', '≤', '≥']):
                print(f"⚖️ Detected inequality: {text}")  
                text = extract_equations_from_text(text)
                print(f"✅Extracted the final text : {text}")
                steps = []
                cleaned_text = text.replace('≤', '<=').replace('≥', '>=')
                steps.append(f"📘 Step 1: Original inequality → {text}")
                steps.append(f"📘 Step 2: Convert symbols → {cleaned_text}")
                expr = sympy.sympify(cleaned_text)
                result = solve_univariate_inequality(expr, sym)
                steps.append(f"📘 Step 3: Solve inequality → {result}")
                return '\n'.join(steps), None

            if 'factor' in text:
                print(f"🔍 Detected factorization request: {text}")  
                text= extract_equations_from_text(text)
                print(f"✅Extracted the final text : {text}")
                expr = sympy.sympify(eq_strings[0] if eq_strings else text)
                factored = sympy.factor(expr)
                return f"Factored: {factored}", expr

            if any(word in text for word in ['simplify', 'surd', 'exponent']):
                print(f"🔬 Detected simplification request: {text}")  
                print(f"✅Extracted the final text : {text}")
                text= extract_equations_from_text(text)
                expr = sympy.sympify(eq_strings[0] if eq_strings else text)
                simplified = sympy.simplify(expr)
                return f"Simplified: {simplified}", expr

            if '/' in text or 'rational' in text:
                print(f"🧮 Detected rational expression: {text}")  
                text= extract_equations_from_text(text)
                print(f"✅Extracted the final text : {text}")
                expr = sympy.sympify(eq_strings[0] if eq_strings else text)
                simplified = sympy.cancel(expr)
                return f"Simplified Rational Expression: {simplified}", expr

           
            is_system = 'simultaneous' in text or len(eq_strings) > 1
            if is_system:
                print(f"🧩 Detected system of equations: {eq_strings}")  
                steps = []
                exprs = []
                vars_set = set()
                steps.append("📘 Step 1: Received system of equations:")
                for i, eq in enumerate(eq_strings):
                    steps.append(f"  Eq{i+1}: {eq}")
                    if '=' not in eq:
                        print(f"❌ Invalid equation format in system: {eq}")  
                        return "❌ Error: Invalid equation format in system. Expected '=' sign.", None
                    lhs, rhs = eq.split('=')

                   
                    lhs = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', lhs)
                    rhs = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', rhs)

                    lhs_expr = sympy.sympify(lhs)
                    rhs_expr = sympy.sympify(rhs)
                    expr = lhs_expr - rhs_expr
                    exprs.append(expr)
                    vars_set.update(expr.free_symbols)

                vars = sorted(vars_set, key=lambda s: s.name)
                steps.append(f"📘 Step 2: Variables to solve for: {', '.join(map(str, vars))}")
                steps.append("📘 Step 3: Converted to system of expressions:")
                for i, expr in enumerate(exprs):
                    steps.append(f"  Expr{i+1}: {expr} = 0")

                print(f"📐 Solving for variables: {vars}")  
                sol = sympy.solve(exprs, vars, dict=True)
                if not sol:
                    print("❌ No solution for system.")  
                    steps.append("❌ No solution found.")
                    return '\n'.join(steps), None

                steps.append("📘 Step 4: Solutions found:")
                for sd in sol:
                    for v in vars:
                        steps.append(f"  {v} = {sd[v]}")

                return '\n'.join(steps), None

           
            eq = eq_strings[0] if eq_strings else text
            print(f"🧮 Solving single equation: {eq}")  

            eq = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', eq)
            eq = eq.replace('^', '**')

            steps = []

            if '=' in eq:
                lhs, rhs = eq.split('=')
                steps.append(f"📘 Step 1: Original equation → {lhs} = {rhs}")
                expr = sympy.sympify(lhs) - sympy.sympify(rhs)
                steps.append(f"📘 Step 2: Move all terms to one side → {lhs} - ({rhs}) = 0")
            else:
                expr = sympy.sympify(eq)
                steps.append(f"📘 Step 1: Expression to solve → {eq}")

            simplified_expr = sympy.simplify(expr)
            steps.append(f"📘 Step 3: Simplify expression → {simplified_expr}")

            factored_expr = sympy.factor(simplified_expr)
            if factored_expr != simplified_expr:
                steps.append(f"📘 Step 4: Factor the expression → {factored_expr}")
            else:
                steps.append(f"📘 Step 4: Cannot factor further → {simplified_expr}")

            sol = sympy.solve(expr, sym)
            if not sol:
                print("❌ No solution.")  
                steps.append("❌ No solution found.")
                return '\n'.join(steps), expr

            sol = [sympy.simplify(s) for s in sol]

            if any(s.has(sympy.I) for s in sol):
                print("⚠️ Imaginary result detected.")  
                steps.append("⚠️ Error: Imaginary result encountered.")
                return '\n'.join(steps), None

            if len(sol) == 1:
                steps.append(f"📘 Step 5: Final solution → {sym} = {sol[0]}")
            else:
                steps.append("📘 Step 5: Final solutions:")
                for s in sol:
                    steps.append(f"  {sym} = {s}")

            return '\n'.join(steps), expr

        except Exception as e:
            print(f"❌ Exception occurred: {e}")  
            return f"❌ Error: {e}", None
