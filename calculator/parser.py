from lark import Lark
from lark import Transformer
import math

standard_expr_grammar = r"""
?expr: sum
?sum: product
      | sum "+" product -> add
      | sum "-" product -> sub
?product: atom
          | product "*" atom -> mul
          | product "/" atom -> div
?atom: "(" expr ")"
        | "log" "(" expr "," expr ")" -> log
        | "pow" "(" expr "," expr ")" -> pow
        | "sin" "(" expr ")" -> sin
        | "cos" "(" expr ")" -> cos
        | "tan" "(" expr ")" -> tan
        | "atan" "(" expr ")" -> atan
        | "sqrt" "(" expr ")" -> sqrt
        | "exp" "(" expr ")" -> exp
        | "!" expr -> fact
        | NUMBER -> number

%import common.SIGNED_NUMBER -> NUMBER
%import common.WS
%ignore WS
"""

programmer_expr_grammar = r"""
expr: "convert" "(" num "," base ")" -> convert
?base: "2" -> bin_base
      | "8" -> oct_base
      | "10" -> dec_base
      | "16" -> hex_base
?num:  BIN -> bin
      | OCT -> oct
      | DEC -> dec
      | HEX -> hex

BIN: /0b[01]+/
OCT: /0o[0-7]+/ 
DEC: /[1-9][0-9]*/
HEX: /0x[0-9A-Fa-f]+/

%import common.WS
%ignore WS
"""


class StandardExprTransformer(Transformer):
    @staticmethod
    def add(args):
        return args[0] + args[1]

    @staticmethod
    def sub(args):
        return args[0] - args[1]

    @staticmethod
    def mul(args):
        return args[0] * args[1]

    @staticmethod
    def div(args):
        return args[0] / args[1]

    @staticmethod
    def log(args):
        return math.log(args[0], args[1])

    @staticmethod
    def pow(args):
        return math.pow(args[0], args[1])

    @staticmethod
    def sin(args):
        return math.sin(args[0])

    @staticmethod
    def cos(args):
        return math.cos(args[0])

    @staticmethod
    def tan(args):
        return math.tan(args[0])

    @staticmethod
    def atan(args):
        return math.atan(args[0])

    @staticmethod
    def sqrt(args):
        return math.sqrt(args[0])

    @staticmethod
    def exp(args):
        return math.exp(args[0])

    @staticmethod
    def fact(args):
        return math.factorial(args[0])

    @staticmethod
    def number(args):
        return float(args[0])


class ProgrammerExprTransformer(Transformer):
    @staticmethod
    def convert(args):
        convert_fn = args[1]
        return convert_fn(args[0])

    @staticmethod
    def bin(args):
        return int(args[0], 2)

    @staticmethod
    def bin_base(_):
        return bin

    @staticmethod
    def oct(args):
        return int(args[0], 8)

    @staticmethod
    def oct_base(_):
        return oct

    @staticmethod
    def dec(args):
        return int(args[0])

    @staticmethod
    def dec_base(_):
        return int

    @staticmethod
    def hex(args):
        return int(args[0], 16)

    @staticmethod
    def hex_base(_):
        return hex

    @staticmethod
    def num(args):
        return args[0]


standard_expr_parser = \
    Lark(standard_expr_grammar, parser='lalr', start='expr', transformer=StandardExprTransformer())

programmer_expr_parser = \
    Lark(programmer_expr_grammar, parser='lalr', start='expr', transformer=ProgrammerExprTransformer())


def evaluate_as_standard_expr(expr):
    return evaluate_with_error_handling(expr, standard_expr_parser)


def evaluate_as_programmer_expr(expr):
    return evaluate_with_error_handling(expr, programmer_expr_parser)


def evaluate_with_error_handling(expr, parser):
    try:
        return parser.parse(expr), None
    except Exception as e:
        return None, str(e)
