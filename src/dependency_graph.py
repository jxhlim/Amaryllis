from __future__ import annotations

import re
from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Iterable

CELL_RE = re.compile(r"(?:'([^']+)'|([A-Za-z_][\w ]*))?!?(\$?[A-Za-z]{1,3}\$?\d+)(?::(\$?[A-Za-z]{1,3}\$?\d+))?")


@dataclass(frozen=True)
class CellNode:
    sheet: str
    address: str

    @property
    def key(self) -> str:
        return f"{self.sheet}!{self.address}"


def _col_to_idx(col: str) -> int:
    total = 0
    for ch in col.upper():
        total = total * 26 + (ord(ch) - 64)
    return total


def _idx_to_col(idx: int) -> str:
    result = ""
    while idx:
        idx, rem = divmod(idx - 1, 26)
        result = chr(rem + 65) + result
    return result


def _split_address(address: str) -> tuple[str, int]:
    cleaned = address.replace("$", "").upper()
    m = re.fullmatch(r"([A-Z]{1,3})(\d+)", cleaned)
    if not m:
        raise ValueError(f"Invalid cell address: {address}")
    return m.group(1), int(m.group(2))


def normalize_cell(sheet: str, address: str) -> str:
    col, row = _split_address(address)
    return f"{sheet}!{col}{row}"


def expand_range(start: str, end: str) -> list[str]:
    start_col, start_row = _split_address(start)
    end_col, end_row = _split_address(end)
    cols = range(min(_col_to_idx(start_col), _col_to_idx(end_col)), max(_col_to_idx(start_col), _col_to_idx(end_col)) + 1)
    rows = range(min(start_row, end_row), max(start_row, end_row) + 1)
    return [f"{_idx_to_col(c)}{r}" for c in cols for r in rows]


def extract_references(formula: str, active_sheet: str) -> list[str]:
    refs: list[str] = []
    for match in CELL_RE.finditer(formula):
        quoted_sheet, plain_sheet, start, end = match.groups()
        sheet = (quoted_sheet or plain_sheet or active_sheet).strip()
        if end:
            refs.extend(normalize_cell(sheet, address) for address in expand_range(start, end))
        else:
            refs.append(normalize_cell(sheet, start))
    # remove duplicates while preserving order
    return list(dict.fromkeys(refs))


class DependencyGraph:
    def __init__(self, formulas: dict[str, str]) -> None:
        self.formulas = formulas
        self.forward: dict[str, set[str]] = defaultdict(set)
        self.reverse: dict[str, set[str]] = defaultdict(set)
        self._build()

    def _build(self) -> None:
        for cell_key, formula in self.formulas.items():
            sheet, _ = cell_key.split("!", 1)
            for ref in extract_references(formula, sheet):
                self.forward[cell_key].add(ref)
                self.reverse[ref].add(cell_key)

    def dependents(self, start: str, max_depth: int | None = None) -> list[str]:
        start_key = start
        seen: set[str] = {start_key}
        result: list[str] = []
        queue: deque[tuple[str, int]] = deque([(start_key, 0)])

        while queue:
            node, depth = queue.popleft()
            if max_depth is not None and depth >= max_depth:
                continue
            for dep in sorted(self.reverse.get(node, set())):
                if dep in seen:
                    continue
                seen.add(dep)
                result.append(dep)
                queue.append((dep, depth + 1))
        return result

    def tree(self, start: str, max_depth: int = 6) -> dict:
        def build(node: str, depth: int, lineage: set[str]) -> dict:
            if depth >= max_depth:
                return {"cell": node, "children": []}
            children = []
            for child in sorted(self.reverse.get(node, set())):
                if child in lineage:
                    children.append({"cell": child, "children": [], "cycle": True})
                    continue
                children.append(build(child, depth + 1, lineage | {child}))
            return {"cell": node, "children": children}

        return build(start, 0, {start})

    def subgraph_edges(self, start: str, max_depth: int = 4) -> list[tuple[str, str]]:
        edges: list[tuple[str, str]] = []
        queue: deque[tuple[str, int]] = deque([(start, 0)])
        visited: set[str] = {start}

        while queue:
            node, depth = queue.popleft()
            if depth >= max_depth:
                continue
            for dep in sorted(self.reverse.get(node, set())):
                edges.append((node, dep))
                if dep not in visited:
                    visited.add(dep)
                    queue.append((dep, depth + 1))
        return edges
