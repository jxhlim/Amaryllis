from __future__ import annotations

from src.dependency_graph import DependencyGraph, extract_references, expand_range


def test_expand_range_rectangular():
    assert expand_range("A1", "B2") == ["A1", "A2", "B1", "B2"]


def test_extract_references_with_sheet_and_range():
    refs = extract_references("=SUM(A1:A2,Sheet2!B3)", "Sheet1")
    assert refs == ["Sheet1!A1", "Sheet1!A2", "Sheet2!B3"]


def test_dependency_graph_dependents_traversal():
    formulas = {
        "Sheet1!B1": "=A1+1",
        "Sheet1!C1": "=B1+1",
        "Sheet1!D1": "=B1+C1",
    }
    graph = DependencyGraph(formulas)

    assert graph.dependents("Sheet1!A1") == ["Sheet1!B1", "Sheet1!C1", "Sheet1!D1"]


def test_tree_includes_nested_children():
    formulas = {
        "Sheet1!B1": "=A1",
        "Sheet1!C1": "=B1",
    }
    graph = DependencyGraph(formulas)
    tree = graph.tree("Sheet1!A1", max_depth=3)

    assert tree["cell"] == "Sheet1!A1"
    assert tree["children"][0]["cell"] == "Sheet1!B1"
    assert tree["children"][0]["children"][0]["cell"] == "Sheet1!C1"
