from .default import *

from vaste.js.macro.macro import JsMacro

import inspect


def macro_map_module(module, path = []):
    return {
        **{
            (*path, k): getattr(module, k)
            for k in dir(module)
            if issubclass(type(getattr(module, k)), JsMacro)
        },
        **{
            mk: mv
            for k in dir(module)
            if inspect.ismodule(getattr(module, k))
            if k not in path
            if len(path) == 0 or "vaste" in module.__package__.split(".")
            for mk, mv in macro_map_module(getattr(module, k), [*path, k]).items()
        },
    }

def macro_map_frame(frame):
    return {
        **{
            (k,): v
            for k, v in frame.f_locals.items()
            if issubclass(type(v), JsMacro)
        },
        **macro_map_module(inspect.getmodule(frame)),
    }


class MacroExpansionTransformer(DefaultTransformer):

    def __init__(self, frame):
        self.macro_map = macro_map_frame(frame)

    def transform(self, py_ast):
        for path, macro in self.macro_map.items():
            if type(macro).match(macro, path, py_ast):
                return type(macro).transformer(
                    self=macro,
                    parent=self,
                    path=path,
                ).transform(py_ast)
        return DefaultTransformer.transform(self, py_ast)
