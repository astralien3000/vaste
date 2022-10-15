from vaste import js

a = "python variable"

@js.program
class MyProgram:
    # js.bom.alert("Hello, Alert !")
    js.bom.console.log("Hello, Console !")
    js.lang.inject_ast(js.ast.Literal(a))

    def add(a, b):
        return a + b

    color_list = [
        "red",
        "green",
        "blue",
    ]

    test_dict = {
        "a": 5.0,
        "b": 3,
        "c": "lool",
        "d": [1,2,3],
        "e": {"f":None},
    }

    res = add(5, 2)


print(MyProgram)
print(MyProgram.unparse())


@js.program
class MySecondProgram:
    js.bom.console.log(MyProgram.color_list)


print(MySecondProgram)
print(MySecondProgram.unparse())

with open(f"{MyProgram.name}.mjs", "w") as file:
    file.write(MyProgram.unparse())

with open(f"{MySecondProgram.name}.mjs", "w") as file:
    file.write(MySecondProgram.unparse())
