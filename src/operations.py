from typing import Any, Callable, Text, Union

from src.stack import Stack
from src.getch import getch


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
    stack.push(stack[-index - 1])

def _input(stack: Stack) -> None:
    try:
        a = ord(chr(ord(getch())))
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
