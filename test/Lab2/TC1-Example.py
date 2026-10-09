 # --- Start AI Code ---
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
# --- End AI Code ---

from expression_grammar import Binary, Unary, Literal, Grouping
from AST_Printer import ASTPrinter
from cn_token import Token
from token_type import TokenType


expression = Binary(
    Unary(
        Token(TokenType.MINUS, "-", None, 1),
        Literal(123)
    ),
    Token(TokenType.STAR, "*", None, 1),
    Grouping(
        Literal(45.67)
    )
)

print(ASTPrinter().print(expression))

'''
Natural Language Representation:
    ((-123) * (45.67))
Expected: 
    (* (- 123) (group 45.67))
'''