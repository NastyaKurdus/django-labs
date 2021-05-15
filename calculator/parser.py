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
        | NAME -> variable

%import common.CNAME -> NAME
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
      | NAME -> variable

BIN: /0b[01]+/
OCT: /0o[0-7]+/ 
DEC: /[1-9][0-9]*/
HEX: /0x[0-9A-Fa-f]+/

%import common.CNAME -> NAME
%import common.WS
%ignore WS
"""


class CalculatorTransformerMixin(Transformer):
    def __init__(self, variables):
        super().__init__()
        self.variables = variables

    def variable(self, args):
        name = args[0]
        try:
            return self.variables[name]
        except KeyError:
            raise Exception("Variable not found: %s" % name)


class StandardExprTransformer(CalculatorTransformerMixin):
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


class ProgrammerExprTransformer(CalculatorTransformerMixin):
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

    def variable(self, args):
        return int(super().variable(args))


standard_expr_parser = Lark(standard_expr_grammar, parser='lalr', start='expr')
programmer_expr_parser = Lark(programmer_expr_grammar, parser='lalr', start='expr')


def evaluate_as_standard_expr(expr, variables):
    return evaluate_with_error_handling(expr, standard_expr_parser, StandardExprTransformer, variables)


def evaluate_as_programmer_expr(expr, variables):
    return evaluate_with_error_handling(expr, programmer_expr_parser, ProgrammerExprTransformer, variables)


def evaluate_with_error_handling(expr, parser, transformer, variables):
    try:
        return transformer(variables).transform(parser.parse(expr)), None
    except Exception as e:
        return None, str(e)
