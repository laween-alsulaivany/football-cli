import ast
from pathlib import Path

from coverage import Coverage


# checks line coverage for the method used in assignment 3
source_file = Path(__file__).resolve().parents[1] / "config.py"
source_code = source_file.read_text(encoding="utf-8")
source_tree = ast.parse(source_code)

method = next(
    node
    for node in source_tree.body
    if isinstance(node, ast.FunctionDef) and node.name == "get_team"
)

coverage = Coverage(data_file=str(source_file.parent / ".coverage"))
coverage.load()
_, statements, _, missing, _ = coverage.analysis2(str(source_file))

method_lines = [
    line for line in statements
    if method.lineno <= line <= method.end_lineno
]
covered_lines = len(method_lines) - sum(line in missing for line in method_lines)
percentage = covered_lines / len(method_lines) * 100

print(f"get_team() line coverage: {percentage:.1f}% ({covered_lines}/{len(method_lines)} lines)")

if percentage <= 70:
    raise SystemExit("get_team() must have above 70% line coverage.")
