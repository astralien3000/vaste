import inspect

from vaste.js.macro.program import ProgramJsMacro
from vaste import py


def dependency_map(module, path = []):
    return {
        **{
            (*path, k): getattr(module, k)
            for k in dir(module)
            if issubclass(type(getattr(module, k)), ProgramJsMacro)
        },
        **{
            mk: mv
            for k in dir(module)
            if inspect.ismodule(getattr(module, k))
            if k not in path
            if len(path) == 0 or "vaste" in module.__package__.split(".")
            for mk, mv in dependency_map(getattr(module, k), [*path, k]).items()
        },
    }


class DependencyVisitor(py.ast.NodeVisitor):

    def __init__(self, cls):
        self.dependency_map = dependency_map(inspect.getmodule(cls))
        self.cache = set()

    def visit(self, py_ast):
        py.ast.NodeVisitor.visit(self, py_ast)
        return self.cache

    def generic_visit(self, py_ast):
        py.ast.NodeVisitor.generic_visit(self, py_ast)
        for path, macro in self.dependency_map.items():
            if type(macro).match(macro, path, py_ast):
                self.cache.add(macro)
