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
        Unary(
            Token(TokenType.BANG, "!", None, 1),
            Literal(True)
        )
    ),
    Token(TokenType.EQUAL_EQUAL, "==", None, 1),
    Grouping(
        Binary(
            Literal(False),
            Token(TokenType.EQUAL_EQUAL, "==", None, 1),
            Literal(None)
        )
    )
)

print(ASTPrinter().print(expression))

'''
Natural Language Representation:
    (!true) == (false == NULL)
Expected: 
    (== (group (! True)) (group (== False Null)))
'''