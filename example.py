from vaste import js

a = "python variable"

@js.program
class MyProgram:
    test = js.lang.import_from("test")
    js.bom.alert("Hello, Alert !")
    js.bom.console.log("Hello, Console !")
    js.lang.inject_ast(js.ast.Literal(a))


print(MyProgram)
print(MyProgram.unparse())
