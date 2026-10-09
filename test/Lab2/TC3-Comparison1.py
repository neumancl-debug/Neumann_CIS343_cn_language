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
            Literal(15),
            Token(TokenType.GREATER, ">", None, 1),
            Literal(9)
        )
    ),
    Token(TokenType.EQUAL_EQUAL, "==", None, 1),
    Grouping(
        Binary(
            Literal(2),
            Token(TokenType.GREATER_EQUAL, ">=", None, 1),
            Literal(7)
        )
    )
)

print(ASTPrinter().print(expression))

'''
Natural Language Representation:
    (15 > 9) == (2 >= 7)
Expected: 
    (== (group (> 15 9)) (group (>= 2 7)))
'''