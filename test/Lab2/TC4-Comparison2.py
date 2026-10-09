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
    Grouping(
        Binary(
            Literal(4),
            Token(TokenType.LESS_EQUAL, "<=", None, 1),
            Literal(10)
        )
    ),
    Token(TokenType.BANG_EQUAL, "!=", None, 1),
    Grouping(
        Binary(
            Literal(6),
            Token(TokenType.LESS, "<", None, 1),
            Literal(8)
        )
    )
)

print(ASTPrinter().print(expression))

'''
Natural Language Representation:
    (4 <= 10) != (6 < 8)
Expected: 
    (!= (group (<= 4 10)) (group (< 6 8)))
'''