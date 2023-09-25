from rich import print
from rich.table import Table


def isOp(c):
    op = ["+", "/", "*", "-", "^", "(", ")"]
    return c in op


def opVal(op: str):
    match op:
        case "+" | "-": return 0
        case "*" | "/": return 1
        case "^": return 2


def listprint(l: list):
    for e in l:
        print(e, end="")


def listToStr(l: list):
    s = ""
    for e in l:
        s += str(e)
    return s


def infixToPostfix(n: str):
    result = []
    aux = []

    fullNum = False
    cTemp = ""

    table = Table("Step", "Input", "Operator", "Result",
                  title="Infix To Postfix",
                  title_justify="center",
                  caption_justify="center",)
    step = 0
    for i, c in enumerate(n):
        if c == " ":
            continue
        if isOp(c):
            if cTemp != "":
                result.append(cTemp)
                result.append(" ")
                step += 1
                table.add_row(str(step), cTemp, listToStr(
                    aux), listToStr(result))
                table.add_section()
                cTemp = ""
        if not isOp(c):
            cTemp += c
            if i == len(n) - 1:
                result.append(cTemp)
                result.append(" ")
                step += 1
                table.add_row(str(step), cTemp, listToStr(
                    aux), listToStr(result))
                table.add_section()
            continue
        elif c == '(':
            aux.append(c)
        elif c == ')':
            while len(aux) > 0 and aux[-1] != '(':
                result.append(aux.pop())
                result.append(" ")
            aux.pop()
        else:
            while len(aux) > 0 and aux[-1] != "(" and opVal(aux[-1]) >= opVal(c):
                result.append(aux.pop())
                result.append(" ")
            aux.append(c)
        step += 1
        table.add_row(str(step), c, listToStr(aux), listToStr(result))
        table.add_section()

    while len(aux) > 0:
        result.append(aux.pop())
        result.append(" ")

    step += 1
    table.add_row(str(step), "", listToStr(aux), listToStr(result))
    table.add_section()

    print(table)
    strResult = listToStr(result)
    print("postfix\t:", strResult)
    return result


def calculatePostfix(n: list):
    result = []
    print("\nCalculating...\n")
    for c in n:
        if c == " ":
            continue
        if not isOp(c):
            result.append(int(c))
            continue

        b = result.pop()
        a = result.pop()

        match c:
            case "*":
                print(a, "*", b, "=", a*b)
                result.append(a*b)
            case "+":
                print(a, "+", b, "=", a+b)
                result.append(a+b)
            case "-":
                print(a, "-", b, "=", a-b)
                result.append(a-b)
            case "/":
                print(a, "/", b, "=", a/b)
                result.append(a/b)
            case "^":
                print(a, "^", b, "=", a**b)
                result.append(a**b)
    print()
    res = result.pop()
    print("result\t:", res)
    return res


def initTugas(s: str):
    print("infix\t:", s)
    Str = infixToPostfix(s)
    for e in Str:
        if e.isdigit():
            calculatePostfix(Str)
            break
    print()


Str = [
    "2*3^4*5+9",
    "A*B+C*D",
    "2 * ( 3 + 5 )",
    "2*(3^(1+1) + 5 * ((1+1)*(1+1)))",
    "23 + 34 * 21"
]

if __name__ == "__main__":
    print("-- Infix To Postfix -- \n")
    for e in Str:
        initTugas(e)
