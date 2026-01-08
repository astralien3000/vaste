import abc

from vaste import py
from vaste import js


class Transpiler(abc.ABC):
    @abc.abstractmethod
    def transpile(self, py_ast: py.ast.AST) -> js.ast.AST:
        ...
