import abc
import collections.abc
import typing
import functools

from vaste import py
from vaste import js


TanspileFunction: typing.TypeAlias = collections.abc.Callable[[py.ast.AST], js.ast.AST]


class TranspilerMiddleware(abc.ABC):
    @abc.abstractmethod
    def __call__(
        self,
        py_ast: py.ast.AST,
        transpile: TanspileFunction,
        next: TanspileFunction,
    ) -> js.ast.AST:
        ...


def transpiler_middleware(func) -> TranspilerMiddleware:
    return functools.wraps(func)(
        type(
            func.__name__,
            (TranspilerMiddleware,),
            dict(__call__=staticmethod(func)),
        )()
    )
