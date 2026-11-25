"""Small helpers shared by the Lab 9 tests."""
import ast
from pathlib import Path

PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent


def parse_module(module_name: str) -> ast.Module:
    """Parse a project source file (e.g. 'order') into a syntax tree."""
    source = (PROJECT_ROOT / f"{module_name}.py").read_text()
    return ast.parse(source)


def read_source(module_name: str) -> str:
    return (PROJECT_ROOT / f"{module_name}.py").read_text()


def find_method(tree: ast.Module, class_name: str, method_name: str) -> ast.FunctionDef:
    """Return the syntax tree of one method of one class."""
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            for item in node.body:
                if isinstance(item, ast.FunctionDef) and item.name == method_name:
                    return item
    raise LookupError(f"{class_name}.{method_name} not found")


def called_names(tree: ast.AST) -> set[str]:
    """Names of every plain function/class called in the tree, e.g. Foo(...)."""
    return {
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }