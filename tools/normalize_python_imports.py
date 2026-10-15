"""Hoist and deduplicate module-level imports without changing final bindings."""

from __future__ import annotations

import ast
import sys
from collections import OrderedDict
from pathlib import Path


def _category(module: str) -> int:
    root = module.split(".", 1)[0]
    if root in sys.stdlib_module_names:
        return 0
    if root == "libs":
        return 2
    return 1


def _format_from_import(module: str, names: list[tuple[str, str | None]]) -> str:
    rendered = [name if alias is None else f"{name} as {alias}" for name, alias in names]
    one_line = f"from {module} import {', '.join(rendered)}"
    if len(one_line) <= 119 and "*" not in rendered:
        return one_line
    if rendered == ["*"]:
        return f"from {module} import *"
    body = "\n".join(f"    {name}," for name in rendered)
    return f"from {module} import (\n{body}\n)"


def normalize(path: Path) -> None:
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    import_nodes = [node for node in tree.body if isinstance(node, (ast.Import, ast.ImportFrom))]

    plain: dict[tuple[str, str | None], int] = {}
    from_imports: dict[tuple[str, str, str | None], int] = {}
    for node in import_nodes:
        if isinstance(node, ast.Import):
            for name in node.names:
                plain[(name.name, name.asname)] = node.lineno
        else:
            module = "." * node.level + (node.module or "")
            for name in node.names:
                from_imports[(module, name.name, name.asname)] = node.lineno

    grouped_from: dict[str, list[tuple[str, str | None, int]]] = OrderedDict()
    for (module, name, alias), line in sorted(from_imports.items(), key=lambda item: item[1]):
        grouped_from.setdefault(module, []).append((name, alias, line))

    statements: list[tuple[int, int, str]] = []
    for (module, alias), line in plain.items():
        text = f"import {module}" if alias is None else f"import {module} as {alias}"
        statements.append((_category(module), line, text))
    for module, names in grouped_from.items():
        last_line = max(line for _, _, line in names)
        statements.append(
            (_category(module), last_line, _format_from_import(module, [(name, alias) for name, alias, _ in names]))
        )
    statements.sort(key=lambda item: (item[0], item[1]))

    categories: list[str] = []
    for category in range(3):
        block = [text for item_category, _, text in statements if item_category == category]
        if block:
            categories.append("\n".join(block))
    import_block = "\n\n".join(categories)

    lines = source.splitlines()
    for node in sorted(import_nodes, key=lambda item: item.lineno, reverse=True):
        del lines[node.lineno - 1 : node.end_lineno]

    insertion_index = 0
    while insertion_index < len(lines) and lines[insertion_index].startswith("#"):
        insertion_index += 1
    while insertion_index < len(lines) and not lines[insertion_index].strip():
        del lines[insertion_index]

    normalized = lines[:insertion_index] + ["", import_block, ""] + lines[insertion_index:]
    path.write_text("\r\n".join(normalized).rstrip() + "\r\n", encoding="utf-8", newline="")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: normalize_python_imports.py <python-file>")
    normalize(Path(sys.argv[1]))
