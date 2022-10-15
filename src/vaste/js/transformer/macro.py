from operator import attrgetter
from .default import *

from vaste import js


class MacroTransformer(DefaultTransformer):

    def __init__(self, macro_map):
        self.macro_map = macro_map

    def transform(self, py_ast):
        for path, macro in self.macro_map.items():
            if type(macro).match(macro, path, py_ast):
                return type(macro).transform(macro, path, py_ast)
        return DefaultTransformer.transform(self, py_ast)
