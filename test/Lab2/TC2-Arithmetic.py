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
    Binary(
        Grouping(
            Binary(
                Binary(
                    Literal(10),
                    Token(TokenType.MINUS, "-", None, 1),
                    Literal(5)
                ),
                Token(TokenType.PLUS, "+", None, 1),
                Binary(
                    Binary(
                        Literal(7),
                        Token(TokenType.STAR, "*", None, 1),
                        Literal(2)
                    ),
                    Token(TokenType.MODULO, "%", None, 1),
                    Literal(2)
                )
            )
        ),
        Token(TokenType.SLASH, "/", None, 1),
        Literal(1)
    ),
    Token(TokenType.PLUS, "+", None, 1),
    Unary(
        Token(TokenType.MINUS, "-", None, 1),
        Literal(25)
    )
)

print(ASTPrinter().print(expression))

'''
Natural Language Representation:
    ((10 - 5) + (7 * 2) % 2) / 1 + (-25)
Expected: 
    (+ (/ (group (+ (- 10 5) (% (* 7 2) 2))) 1) (- 25))
'''