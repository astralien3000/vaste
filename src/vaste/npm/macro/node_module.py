from vaste.js.macro.program import ProgramJsMacro
from vaste import js


class NodeModuleJsMacro(ProgramJsMacro):

    def __init__(self, name, extra_files = []):
        self._filename = name
        self._extra_files = extra_files
        name = name.replace("-", "_")
        name = name.replace(".", "_")
        name = name.replace("/", "_")
        super().__init__(name, None, [])


    @property
    def filename(self):
        return object.__getattribute__(self, "_filename")

    def save(self):
        pass

    @property
    def import_list(self):
        return [
            js.ast.ImportDeclaration(
                specifiers=[
                    js.ast.ImportNamespaceSpecifier(
                        js.ast.Identifier(self.name)
                    ),
                ],
                source=js.ast.Literal(self.filename),
            ),
            *[
                js.ast.ImportDeclaration(
                    specifiers=[],
                    source=js.ast.Literal(f),
                )
                for f in self._extra_files
            ]
        ]
