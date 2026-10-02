# Defines the TokenTypes that can exist in the source code.
from enum import Enum


TokenType = Enum(
    'TokenType',
    [   
        # Punctuation and Operators
        'LEFT_PAREN', 'RIGHT_PAREN', 'LEFT_BRACE', 'RIGHT_BRACE', 'COMMA', 'DOT', 'MINUS', 'PLUS', 'SEMICOLON', 'SLASH', 'STAR', 'MODULO',
        
        'BANG', 'BANG_EQUAL', 'EQUAL', 'EQUAL_EQUAL', 'GREATER', 'GREATER_EQUAL', 'LESS', 'LESS_EQUAL',

        # Literals
        'IDENTIFIER', 'STRING', 'NUMBER', 

        # Keywords
        'AND', 'CLASS', 'ELSE', 'FALSE', 'FUN', 'FOR', 'IF', 'ELSEIF', 'NULL', 'OR', 'PRINT', 'RETURN','SUPER', 'THIS', 'TRUE', 'VAR', 'CONST',
        'WHILE', 'BREAK', 'EOF'
    ]
)
