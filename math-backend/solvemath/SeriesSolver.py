import sympy
from solvemath.base import SolveMath
from typing import Tuple

class SeriesSolver(SolveMath):
    def solve(self, problem_text: str, variable: str = 'n') -> Tuple[str, sympy.Expr | None]:
        print(f"🔢 SeriesSolver activated for: {problem_text}")
        text = problem_text.lower()
        steps = []

        try:
           
            if any(keyword in text for keyword in ['arithmetic', 'common difference', 'aₙ']):
                steps.append("📘 Arithmetic Sequence Detected")

                terms = self._extract_sequence(text)
                if len(terms) >= 2:
                    a1 = terms[0]
                    d = terms[1] - terms[0]
                    steps.append(f"  First term (a₁) = {a1}")
                    steps.append(f"  Common difference (d) = {d}")
                    
                    # Find nth term or specific term
                    if "term" in text:
                        n = self._extract_integer_before_keyword(text, "term") or variable
                        nth_term = a1 + (n - 1) * d
                        steps.append(f"  {n}th term: aₙ = a₁ + (n-1)d = {nth_term}")
                        return '\n'.join(steps), sympy.sympify(f"{a1} + ({n}-1)*{d}")
                    
                    # Sum of terms
                    if "sum" in text:
                        n = self._extract_integer_before_keyword(text, "sum") or variable
                        total = (n / 2) * (2 * a1 + (n - 1) * d)
                        steps.append(f"  Sum of first {n} terms: Sₙ = n/2 * (2a₁ + (n-1)d) = {total}")
                        return '\n'.join(steps), sympy.sympify(f"({n}/2)*(2*{a1} + ({n}-1)*{d})")

            # --- Geometric Sequence ---
            elif any(keyword in text for keyword in ['geometric', 'common ratio', 'gₙ']):
                steps.append("📘 Geometric Sequence Detected")
                # Example: "Find the sum of 2 + 6 + 18 + ... up to 5 terms"
                terms = self._extract_sequence(text)
                if len(terms) >= 2:
                    a1 = terms[0]
                    r = terms[1] / terms[0]
                    steps.append(f"  First term (a₁) = {a1}")
                    steps.append(f"  Common ratio (r) = {r}")
                    
                    # Nth term
                    if "term" in text:
                        n = self._extract_integer_before_keyword(text, "term") or variable
                        nth_term = a1 * (r ** (n - 1))
                        steps.append(f"  {n}th term: gₙ = a₁ * r^(n-1) = {nth_term}")
                        return '\n'.join(steps), sympy.sympify(f"{a1}*({r}^({n}-1))")
                    
                    # Sum of terms
                    if "sum" in text:
                        n = self._extract_integer_before_keyword(text, "sum") or variable
                        if r == 1:
                            total = n * a1
                        else:
                            total = a1 * (1 - r**n) / (1 - r)
                        steps.append(f"  Sum of first {n} terms: Sₙ = a₁(1-rⁿ)/(1-r) = {total}")
                        return '\n'.join(steps), sympy.sympify(f"{a1}*(1-{r}^{n})/(1-{r})")

            # --- Summation (Σ) ---
            elif "sum" in text or "sigma" in text:
                steps.append("📘 Summation (Σ) Detected")
                # Example: "Sum of 1 + 2 + 3 + ... + 100"
                if "..." in text:
                    start, end = self._extract_range(text)
                    if start == 1 and "n" not in text:
                        total = end * (end + 1) // 2  # Triangular numbers
                        steps.append(f"  Sum of 1 to {end}: S = n(n+1)/2 = {total}")
                        return '\n'.join(steps), sympy.sympify(f"{end}*({end}+1)/2")
                # Handle symbolic sums like Σ(n^2, n=1 to k)
                elif "sigma" in text or "sum" in text:
                    expr = self._extract_summation_expression(text)
                    if expr:
                        n = sympy.Symbol(variable)
                        total = sympy.Sum(expr, (n, 1, variable)).doit()
                        steps.append(f"  Summation: Σ({expr}) = {total}")
                        return '\n'.join(steps), total

            # --- Convergence Tests (Advanced) ---
            elif any(word in text for word in ['converge', 'diverge', 'infinite series']):
                steps.append("📘 Convergence Test Detected")
                expr = self._extract_series_expression(text)
                if expr:
                    n = sympy.Symbol(variable)
                    convergence = sympy.limit(expr, n, sympy.oo)
                    if convergence == 0:
                        steps.append(f"  Series may converge (terms → 0). Further tests needed.")
                    else:
                        steps.append(f"  Series diverges (terms → {convergence}).")
                    return '\n'.join(steps), None

            return "❌ Could not identify series type. Try phrases like '10th term of 2,5,8,...' or 'sum of 1+2+3+...+100'.", None

        except Exception as e:
            print(f"❌ SeriesSolver Error: {e}")
            return f"❌ Error: {str(e)}", None

    # --- Helper Methods ---
    def _extract_sequence(self, text: str) -> list[float]:
        """Extract numbers from phrases like '3, 7, 11' or '2 + 6 + 18'."""
        numbers = []
        # Match commas or '+' separated numbers
        parts = [p.strip() for p in text.replace('+', ',').split(',') if p.strip().replace('.', '').isdigit()]
        for p in parts:
            try:
                numbers.append(float(p))
            except ValueError:
                continue
        return numbers

    def _extract_integer_before_keyword(self, text: str, keyword: str) -> int | None:
        """Extract '10' from phrases like '10th term'."""
        words = text.split()
        for i, word in enumerate(words):
            if keyword in word:
                if i > 0 and words[i-1].isdigit():
                    return int(words[i-1])
        return None

    def _extract_range(self, text: str) -> Tuple[int, int]:
        """Extract range from '1 + 2 + ... + 100'."""
        parts = text.split('...')
        start = int(parts[0].split()[-1]) if parts[0].split() else 1
        end = int(parts[1].split()[0]) if parts[1].split() else start
        return start, end

    def _extract_summation_expression(self, text: str) -> sympy.Expr | None:
        """Extract Σ(n^2, n=1 to k) or similar."""
        try:
            # Simple case: "sum of n^2 from n=1 to k"
            expr_part = text.split('sum of')[-1].split('from')[0].strip()
            return sympy.sympify(expr_part)
        except:
            return None