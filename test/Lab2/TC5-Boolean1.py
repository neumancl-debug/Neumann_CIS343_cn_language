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
    Literal(True),
    Token(TokenType.OR, "or", None, 1),
    Grouping(
        Binary(
            Binary(
                Literal("hello"),
                Token(TokenType.LESS_EQUAL, "<=", None, 1),
                Literal("world")
            ),
            Token(TokenType.AND, "and", None, 1),
            Binary(
                Literal("word"),
                Token(TokenType.BANG_EQUAL, "!=", None, 1),
                Literal(None)
            )
        )
    )
)

print(ASTPrinter().print(expression))

'''
Natural Language Representation:
    true or ("hello" <= "world" and "word" != NULL)
Expected: 
    (or True (group (and (<= hello world) (!= word None))))
'''