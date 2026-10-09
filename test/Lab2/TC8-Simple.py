 # --- Start AI Code ---
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
# --- End AI Code ---

from expression_grammar import Binary, Unary, Literal, Grouping
from AST_Printer import ASTPrinter
from cn_token import Token
from token_type import TokenType


expression_binary = Binary(
    Literal(10),
    Token(TokenType.PLUS, "+", None, 1),
    Literal(5)
)

expression_comparison = Binary(
    Literal(True),
    Token(TokenType.EQUAL_EQUAL, "==", None, 1),
    Literal(False)
)

expression_unary = Unary(
    Token(TokenType.MINUS, "-", None, 1),
    Literal(5)
)

expression_literal = Literal(950)

expression_string = Literal("hello")

expression_grouping = Grouping(
    Literal(5)
)

expression_grouping_binary = Grouping(
    Binary(
        Literal(4),
        Token(TokenType.STAR, "*", None, 1),
        Literal(2)
    )
)

print(ASTPrinter().print(expression_binary))
print(ASTPrinter().print(expression_comparison))
print(ASTPrinter().print(expression_unary))
print(ASTPrinter().print(expression_literal))
print(ASTPrinter().print(expression_string))
print(ASTPrinter().print(expression_grouping))
print(ASTPrinter().print(expression_grouping_binary))

"""
Expected Output:

(+ 10 5)
(- 5)
(== True False)
950
hello
(group 5)
(group (4 * 2))
"""


