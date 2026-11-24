from expression_grammar import Binary, Unary, Literal, Grouping, Expression, Print, Var, Variable, Assign, Block
from token_type import TokenType
from error_handling import RuntimeError, ErrorHandler
from Environment import Environment

# Interpreter class for evaluating expressions and executing statements.
class Interpreter:
    
    # Initializes the interpreter with a global environment for variable storage.
    def __init__(self):
        self.environment = Environment()

    # Evaluates an expression and returns its value.
    def visit_literal_expr(self, expr):
        return expr.value

    # Evaluates a grouping expression by evaluating the inner expression.
    def visit_grouping_expr(self, expr):
        return self.evaluate(expr.expression)

    # Evaluates an expression by calling its accept method, which calls the appropriate visit method.
    def evaluate(self, expr):
        return expr.accept(self)

    # Executes a statement by calling its accept method, which calls the appropriate visit method.
    def visit_unary_expr(self, expr):
        right = self.evaluate(expr.right)

        if expr.operator.type == TokenType.MINUS:
            self.check_number_operand(expr.operator, right)
            return -right
        elif expr.operator.type == TokenType.BANG:
            return not self.is_truthy(right)

        return None

    # Determines the truthiness of a value.
    def is_truthy(self, value):
        if value is None:
            return False
        '''if isinstance(value, (int, float)):
            return value != 0'''
        if isinstance(value, bool):
            return value
        return True

    # Evaluates a binary expression by evaluating its left and right operands and applying the operator.
    def visit_binary_expr(self, expr):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        if expr.operator.type == TokenType.MINUS:
            self.check_number_operands(expr.operator, left, right)
            return left - right
        
        if expr.operator.type == TokenType.SLASH:
            self.check_number_operands(expr.operator, left, right)
            if right == 0:
                raise RuntimeError(expr.operator, "Division by zero.")
            return left / right
        
        if expr.operator.type == TokenType.STAR:
            self.check_number_operands(expr.operator, left, right)
            return left * right
        
        if expr.operator.type == TokenType.PLUS:
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                return left + right
            if isinstance(left, str) and isinstance(right, str):
                return left + right
            raise RuntimeError(expr.operator, "Operands must be two numbers or two strings.")

        if expr.operator.type == TokenType.MODULO:
                    self.check_number_operands(expr.operator, left, right)
                    if right == 0:
                        raise RuntimeError(expr.operator, "Division by zero.")
                    return left % right

        if expr.operator.type == TokenType.GREATER:
            self.check_number_operands(expr.operator, left, right)
            return left > right
        if expr.operator.type == TokenType.GREATER_EQUAL:
            self.check_number_operands(expr.operator, left, right)
            return left >= right
        if expr.operator.type == TokenType.LESS:
            self.check_number_operands(expr.operator, left, right)
            return left < right
        if expr.operator.type == TokenType.LESS_EQUAL:
            self.check_number_operands(expr.operator, left, right)
            return left <= right
        if expr.operator.type == TokenType.BANG_EQUAL:
            return not self.is_equal(left, right)
        
        if expr.operator.type == TokenType.EQUAL_EQUAL:
            return self.is_equal(left, right)

        raise RuntimeError(expr.operator, "Unknown binary operator.")

    # Determines if two values are equal and considersNone as a special case.
    def is_equal(self, a, b):
        if a is None and b is None:
            return True
        if a is None:
            return False

        return a == b    

    # Checks if the operand is a number and raises a RuntimeError if it is not.
    def check_number_operand(self, operator, operand):
        if isinstance(operand, (int, float)):
            return
        raise RuntimeError(operator, "Operand must be a number.")

    # Checks if both operands are numbers and raises a RuntimeError if either is not.
    def check_number_operands(self, operator, left, right):
        self.check_number_operand(operator, left)
        self.check_number_operand(operator, right)

    # Interprets a list of statements (AST nodes) and executes them, handling any runtime errors that may occur.
    def interpret(self, expression):
        try:
            for statement in expression:
                self.execute(statement)
        except RuntimeError as error:
            ErrorHandler.runtime_error(error)

    def stringify(self, value):
        if value is None:
            return "null"
        if isinstance(value, float):
            text = str(value)
           
            if text.endswith(".0"):
                text = text[:-2]
            
            return text

        return str(value)

    # Executes a statement by calling its accept method, which calls the appropriate visit method.
    def execute(self, statement):
        statement.accept(self)

    # Visits an expression statement, evaluates the expression, and returns its value.
    def visit_expression_stmt(self, stmt):
        value = self.evaluate(stmt.expression)
       
    # Visits a print statement, evaluates the expression, and prints its value.
    def visit_print_stmt(self, stmt):
        value = self.evaluate(stmt.expression)
        print(self.stringify(value))

    # Visits a variable declaration statement, evaluates the initializer (if present), and defines the variable in the current environment.
    def visit_var_stmt(self, stmt):
        value = None
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)
        self.environment.define(stmt.name.lexeme, value)

    # Visits a variable expression, retrieves its value from the current environment, and returns it.
    def visit_variable_expr(self, expr):
        return self.environment.get(expr.name)

    # Visits an assignment expression, evaluates the value, assigns it to the variable in the current environment, and returns the value.
    def visit_assign_expr(self, expr):
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value
    # Visits a block statement, creates a new environment for the block, and executes the statements in the block within that environment.
    def visit_block_stmt(self, stmt):
        self.execute_block(stmt.statements, Environment(self.environment))

    # Executes a block of statements within a given environment, temporarily replacing the current environment with the new one.
    def execute_block(self, statements, environment):
        previous = self.environment
        try:
            self.environment = environment

            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous