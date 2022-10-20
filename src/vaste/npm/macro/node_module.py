from vaste.js.macro.program import ProgramJsMacro


class NodeModuleJsMacro(ProgramJsMacro):

    def __init__(self, name):
        object.__setattr__(self, "_filename", name)
        name = name.replace("-", "_")
        name = name.replace(".", "_")
        name = name.replace("/", "_")
        super().__init__(name, None, [])


    @property
    def filename(self):
        return object.__getattribute__(self, "_filename")
