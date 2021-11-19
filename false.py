from src.emulator import Emulator
from src.parse import parse

def is_valid_file(parser, arg):
    import os
    if not os.path.exists(arg):
        parser.error(f'The file {arg} does not exist!')
    else:
        return arg  # return path

def main():
    from argparse import ArgumentParser
    parser = ArgumentParser(description='Interpret FALSE code')
    parser.add_argument('input', action='store', nargs='?',
                        help='file that contains code', metavar='FILE',
                        type=lambda x: is_valid_file(parser, x))
    parser.add_argument('-c', '--code', action='store',
                        help='raw code string', metavar='TEXT')
    parser.add_argument('-p', '--print-stack', action='store_true',
                        help='Print stack after execution')
    args = parser.parse_args()

    path = args.input
    code = args.code

    # (path != None) iff (code != None)
    if (not path) == (not code):
        raise RuntimeError('Either code or file must be supplied exclusively!')

    if path and not code:
        with open(path, 'r', encoding='utf-8') as file:
            code = file.read()

    instructions = parse(code)
    emulator = Emulator()

    # Run Instructions
    stack = emulator.run(instructions)

    if args.print_stack:
        print(f'Stack: {stack}')

if __name__ == '__main__':
    main()
