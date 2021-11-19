from typing import Mapping

from src.stack import Stack
from src.operations import *


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
