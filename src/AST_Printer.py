# AST printer for the CN language
class ASTPrinter:
    def print(self, expr):
        return expr.accept(self)

    # Visitor methods to handle different types of expressions
    def visit_binary(self, expr):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping(self, expr):
        return self.parenthesize("group", expr.expression)

    def visit_literal(self, expr):
        if expr.value is None:
            return "null"
        return str(expr.value)

    def visit_unary(self, expr):
        return self.parenthesize(expr.operator.lexeme, expr.right)

    # Helper method to parenthesize expressions
    def parenthesize(self, name, *exprs):
        base = "(" + name
        for expr in exprs:
            base += " " + expr.accept(self)
        base += ")"
        return base

