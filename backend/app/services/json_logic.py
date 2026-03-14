"""Minimal JSON Logic evaluator.

Supports the subset of http://jsonlogic.com needed by G.A.R.D.:
var, and, or, not, !, >, >=, <, <=, ==, !=, if, in, starts_with, ends_with, length
"""

from typing import Any


def json_logic(rule: Any, data: dict | None = None) -> Any:
    """Evaluate a JSON Logic rule against data."""
    if data is None:
        data = {}

    # Primitives pass through
    if not isinstance(rule, dict):
        return rule

    # A JSON Logic rule is a dict with exactly one key (the operator)
    op = next(iter(rule))
    values = rule[op]

    # Ensure values is a list
    if not isinstance(values, list):
        values = [values]

    # Variable access
    if op == "var":
        path = str(values[0]) if values else ""
        default = values[1] if len(values) > 1 else None
        return _get_var(data, path, default)

    # Boolean
    if op == "and":
        result = True
        for v in values:
            result = json_logic(v, data)
            if not result:
                return result
        return result

    if op == "or":
        result = False
        for v in values:
            result = json_logic(v, data)
            if result:
                return result
        return result

    if op in ("not", "!"):
        return not json_logic(values[0], data)

    # Comparison
    if op == ">":
        a, b = _resolve_args(values, data, 2)
        return a > b

    if op == ">=":
        a, b = _resolve_args(values, data, 2)
        return a >= b

    if op == "<":
        args = _resolve_args(values, data, len(values))
        if len(args) == 3:
            return args[0] < args[1] < args[2]
        return args[0] < args[1]

    if op == "<=":
        args = _resolve_args(values, data, len(values))
        if len(args) == 3:
            return args[0] <= args[1] <= args[2]
        return args[0] <= args[1]

    if op == "==":
        a, b = _resolve_args(values, data, 2)
        return a == b

    if op == "!=":
        a, b = _resolve_args(values, data, 2)
        return a != b

    # Conditional
    if op == "if":
        resolved = [json_logic(v, data) for v in values]
        i = 0
        while i < len(resolved) - 1:
            if resolved[i]:
                return resolved[i + 1]
            i += 2
        # Else clause
        if i < len(resolved):
            return resolved[i]
        return None

    # Membership
    if op == "in":
        a, b = _resolve_args(values, data, 2)
        return a in b

    # String operations
    if op == "starts_with":
        a, b = _resolve_args(values, data, 2)
        return str(a).startswith(str(b))

    if op == "ends_with":
        a, b = _resolve_args(values, data, 2)
        return str(a).endswith(str(b))

    if op == "length":
        a = json_logic(values[0], data)
        return len(a)

    raise ValueError(f"Unsupported JSON Logic operator: {op}")


def _resolve_args(values: list, data: dict, count: int) -> list:
    return [json_logic(v, data) for v in values[:count]]


def _get_var(data: dict, path: str, default: Any = None) -> Any:
    if path == "" or path is None:
        return data
    keys = str(path).split(".")
    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        elif isinstance(current, list):
            try:
                current = current[int(key)]
            except (ValueError, IndexError):
                return default
        else:
            return default
    return current
