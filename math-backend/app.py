from flask import Flask, request, jsonify
from solvemath.factory import SolverFactory

app = Flask(__name__)

@app.route('/solve', methods=['POST'])
def solve_api():
    data = request.get_json()
    solver_code = data.get("solver_code")
    expression = data.get("expression")

    factory = SolverFactory()
    solver = factory.get_solver_by_code(solver_code)

    if solver:
        result, steps = solver.solve(expression)
        return jsonify({"result": result, "steps": steps})

    return jsonify({"error": "Invalid solver code"}), 400

if __name__ == '__main__':
    app.run(debug=True)
