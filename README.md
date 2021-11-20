# FALSE interpreter written in python3

FALSE is an esoteric programming language created by [Wouter van Oortmerssen](https://strlen.com/false-language/) in 1993.

Wiki page on eslolangs.org: [https://esolangs.org/wiki/FALSE](https://esolangs.org/wiki/FALSE)

### Usage

```
usage: false.py [-h] [-c TEXT] [-p] [FILE]

Interpret FALSE code

positional arguments:
  FILE                  file that contains code

optional arguments:
  -h, --help            show this help message and exit
  -c TEXT, --code TEXT  raw code string
  -p, --print-stack     Print stack after execution
```

#### Examples

```bash
python3 false.py -p examples/fac.f

python3 false.py examples/fac.f

echo 3 | python false.py -p examples/fac.f

python3 false.py -c '"Hello, World!
"'

# dumb way to copy a file:
cat examples/fac.f | python false.py examples/copy.f > examples/fac2.f
```

