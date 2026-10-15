"""Generate the ordered GlobalCase pytest method-name list."""

from __future__ import annotations

import ast
import sys
from pathlib import Path


def collect_test_names(source_path: Path) -> list[str]:
    tree = ast.parse(source_path.read_text(encoding="utf-8-sig"), filename=str(source_path))
    names: list[str] = []
    seen: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if not node.name.startswith("test_EMS1_") or node.name in seen:
            continue
        names.append(node.name)
        seen.add(node.name)
    names.sort(key=lambda name: _line_number(tree, name))
    return names


def _line_number(tree: ast.AST, target_name: str) -> int:
    return min(
        node.lineno
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == target_name
    )


def generate(source_path: Path, output_path: Path) -> None:
    names = collect_test_names(source_path)
    output_path.write_text("\r\n".join(names) + "\r\n", encoding="utf-8", newline="")
    print(f"Generated {len(names)} case names in {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(
            "usage: generate_global_case_test_names.py <GlobalCase.py> <output.list>"
        )
    generate(Path(sys.argv[1]), Path(sys.argv[2]))
