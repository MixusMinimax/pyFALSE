{ Original code: }
{
[$1=~[$1-f;!*]?]f:

"calculate the factorial of [1..8]: "
ß^ß'0-$$0>~8>|$
"result: "
~[f;!.]?
["illegal input!"]?"
"
}

{ New code: }

{ factorial program in false! }

[$1=~[$1-f;!*]?]f:          { fac() in false }

"calculate the factorial of [1..8]: "
ß^ß'0-$$0>~\8>|$
"result: "
~[\f;!.]?
["illegal input!"]?"
"

{
Explanation:

Let's say the input is 3.

code   description                    stack after code
ß^ß    flush and read                 ['3']
'0-    convert character to number    [3]
$$     copy twice                     [3, 3, 3]
0                                     [3, 3, 3, 0]
>      compare against 0              [3, 3, true]
~                                     [3, 3, false]
\      swap comparison result         [3, false, 3]
8                                     [3, false, 3, 8]
>                                     [3, false, false]
|      or both conditions             [3, false]
$      copy for if/else               [3, false, false]

~          negate condition, so call function only if condition is false (so no input errors)    [3, false, true]
[\         swap top two elements. Remember, the "true" is gone because the "?" consumes it before this lambda is executed. [false, 3]
f;!.       call function and print result. There is no swap after this, since the function consumed the top element on the stack.
]?         put lambda on the stack, and execute, since 3 is valid input                          [false]

["illegal input!"]?   use the second copy of the boolean for the error message                   []

}