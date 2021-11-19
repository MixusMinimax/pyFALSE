from string import ascii_lowercase
from typing import List, Text, Tuple

from src.operations import *


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
                if (len(code) > 0 and code[0] == '_'):
                    number = -number
                    code = code[1:]
                instructions.append(number)
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
