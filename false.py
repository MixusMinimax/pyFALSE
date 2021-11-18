from typing import Any, Callable, List, Mapping, Text, Tuple, Union
from string import ascii_lowercase
from getch import getch


code = R'''
{ factorial program in false! }

[$1=~[$1-f;!*]?]f:          { fac() in false }

"calculate the factorial of [1..8]: "
ß^ß'0-$$0>~\8>|$
"result: "
~[\f;!.\]?
["illegal input!"]?"
"
'''

class Stack(list):
    def push(self, a):
        return self.append(a)
    
    def pop(self):
        if len(self) == 0:
            raise RuntimeError('Tried popping from empty stack!')
        return super().pop()


class StackOp:
    def __init__(self, op: Callable[[Stack], Union[Stack, None]]) -> None:
        self.op = op

    def apply(self, stack: Stack) -> Stack:
        self.op(stack)
        return stack


class UnaryOp(StackOp):
    def __init__(self, op: Callable[[Any], Any]) -> None:
        self.op = op

    def apply(self, stack: Stack) -> Stack:
        stack.push(self.op(stack.pop()))
        return stack


class BinaryOp(StackOp):
    def __init__(self, op: Callable[[Any, Any], Any]) -> None:
        self.op = op

    def apply(self, stack: Stack) -> Stack:
        x = stack.pop()
        stack.push(self.op(stack.pop(), x))
        return stack


class StoreReferenceOp(StackOp):
    def __init__(self, name: Text) -> None:
        self.name = name

    def apply(self, stack: Stack) -> Stack:
        stack.push(self.name)
        return stack


class PrintOp(StackOp):
    def __init__(self, text: Text) -> None:
        self.text = text

    def apply(self, stack: Stack) -> Stack:
        print(self.text, end='')
        return stack


class ExecuteLambdaOp:
    def __init__(self, conditional: bool = False) -> None:
        self.conditional = conditional


class WhileOp: pass
class StoreOp: pass
class LoadOp: pass


def _dup(stack: Stack) -> None:
    if len(stack) == 0:
        raise RuntimeError('Tried duping from empty stack!')
    stack.push(stack[-1])

def _swap(stack: Stack) -> None:
    b, a = stack.pop(), stack.pop()
    stack.push(b)
    stack.push(a)

def _rot(stack: Stack) -> None:
    c, b, a = stack.pop(), stack.pop(), stack.pop()
    stack.push(b)
    stack.push(c)
    stack.push(a)

def _pick(stack: Stack) -> None:
    index = stack.pop()
    if not index < len(stack):
        raise RuntimeError('Tried picking from too small stack!')
    stack.push(stack[-index])

def _input(stack: Stack) -> None:
    ch = getch()
    try:
        a =  ord(ch)
    except:
        a = -1
    stack.push(a)

def _outputChar(stack: Stack) -> None:
    a = stack.pop()
    import sys
    sys.stdout.write(chr(a))

def _outputDecimal(stack: Stack) -> None:
    a = stack.pop()
    import sys
    sys.stdout.write(str(a))

def _flush(stack: Stack) -> None:
    import sys
    sys.stdin.flush()
    sys.stdout.flush()
    

DUP = StackOp(_dup)
DROP = StackOp(lambda stack : stack.pop())
SWAP = StackOp(_swap)
ROT = StackOp(_rot)
PICK = StackOp(_pick)

INPUT = StackOp(_input)
OUTPUT_CHAR = StackOp(_outputChar)
OUTPUT_DEC = StackOp(_outputDecimal)
FLUSH = StackOp(_flush)


NEG = UnaryOp(lambda a : -a)
NOT = UnaryOp(lambda a : not a)

ADD = BinaryOp(lambda a, b : a + b)
SUB = BinaryOp(lambda a, b : a - b)
MUL = BinaryOp(lambda a, b : a * b)
DIV = BinaryOp(lambda a, b : a // b)

AND = BinaryOp(lambda a, b : a & b)
OR = BinaryOp(lambda a, b : a | b)

GRT = BinaryOp(lambda a, b : a > b)
EQU = BinaryOp(lambda a, b : a == b)

def parse(code: Text) -> List:
    instructions, remainder = _parse(code)
    return instructions

def _parse(code: Text) -> Tuple[List, Text]:

    instructions = []

    number = 0

    while len(code) > 0:
        letter = code[0]
        code = code[1:]

        if letter.isdigit():
            number = number * 10 + int(letter)
            if len(code) == 0 or not code[0].isdigit():
                instructions.append(number)
                number = 0
        elif letter == '_':
            instructions.append(-number)
            number = 0
        elif letter == "'":
            if len(code) == 0:
                raise RuntimeError('"\'" must precede a character!')
            instructions.append(ord(code[0]))
            code = code[1:]
        elif letter in ascii_lowercase:
            instructions.append(StoreReferenceOp(name=letter))
        elif letter == '[':
            lam, code = _parse(code)
            instructions.append(lam)
        elif letter == ']':
            break
        elif letter == '{':
            code = code[code.index('}')+1:]
        elif letter == '"':
            index = code.index('"')
            instructions.append(PrintOp(code[:index]))
            code = code[index + 1:] 
        else:
            MAP = {
                '$': DUP,
                '%': DROP,
                '\\': SWAP,
                '@': ROT,
                'ø': PICK,
                '+': ADD,
                '-': SUB,
                '*': MUL,
                '/': DIV,
                '_': NEG,
                '&': AND,
                '|': OR,
                '~': NOT,
                '>': GRT,
                '=': EQU,
                '!': ExecuteLambdaOp(conditional=False),
                '?': ExecuteLambdaOp(conditional=True),
                '#': WhileOp(),
                ':': StoreOp(),
                ';': LoadOp(),
                '^': INPUT,
                ',': OUTPUT_CHAR,
                '.': OUTPUT_DEC,
                'ß': FLUSH
            }
            if letter in MAP:
                instructions.append(MAP[letter])

    return instructions, code


class Emulator:
    def __init__(self, stack: Stack = None) -> None:
        self.stack = stack or Stack()
        self.variables: Mapping[Text, Any] = {}
        pass

    def run(self, instructions: list):

        stack = self.stack

        for instruction in instructions:
            if isinstance(instruction, (int, list)):
                stack.push(instruction)
            elif isinstance(instruction, StackOp):
                instruction.apply(stack)
            elif isinstance(instruction, ExecuteLambdaOp):
                code: list = stack.pop()
                if not isinstance(code, list):
                    raise RuntimeError('top of stack is not lambda!')
                execute = True
                if instruction.conditional:
                    if not stack.pop():
                        execute = False
                if execute:
                    self.run(code)
            elif isinstance(instruction, WhileOp):
                body: list = stack.pop()
                condition: list = stack.pop()
                if not isinstance(body, list) or not isinstance(condition, list):
                    raise RuntimeError('top of stack is not lambda!')
                while True:
                    self.run(condition)
                    result = stack.pop()
                    if not result:
                        break
                    self.run(body)
            elif isinstance(instruction, StoreOp):
                name = stack.pop()
                self.variables[name] = stack.pop()
            elif isinstance(instruction, LoadOp):
                name = stack.pop()
                stack.push(self.variables[name])

        return stack


def main():

    code = R'''
{ factorial program in false! }

[$1=~[$1-f;!*]?]f:          { fac() in false }

"calculate the factorial of [1..8]: "
ß^ß'0-$$0>~\8>|$
"result: "
~[\f;!.]?
["illegal input!"]?"
"
    '''

    instructions = parse(code)
    emulator = Emulator()
    stack = emulator.run(instructions)
    print(stack)

if __name__ == '__main__':
    main()