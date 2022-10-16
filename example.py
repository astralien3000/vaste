from vaste import js


@js.program
class Program1:
    js.bom.console.log("Hello, Console !")


@js.program
class Program2:
    def add(a, b):
        return a + b


@js.program
class Program3:
    color_list = [
        "red",
        "green",
        "blue",
    ]


@js.program
class Program4:
    test_dict = {
        "a": 5.0,
        "b": 3,
        "c": "lool",
        "d": [1,2,3],
        "e": {"f":None},
    }

    res = Program2.add(5, 2)


@js.program
class MainProgram:
    Program1
    js.bom.console.log(Program3.color_list)
    js.bom.console.log(Program4.test_dict)
    js.bom.console.log(Program4.res)


MainProgram.exec()
