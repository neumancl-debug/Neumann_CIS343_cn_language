# AST classes for expressions in the CN language
class Expr:
    def accept(self, visitor):
        raise NotImplementedError()
    
class Literal(Expr):
        def __init__(self, value):
            self.value = value
        def accept(self, visitor):
            return visitor.visit_literal_expr(self)

class Binary(Expr):
    def __init__(self, left_expr, operator, right_expr):
        self.left = left_expr
        self.operator = operator
        self.right = right_expr
    def accept(self, visitor):
        return visitor.visit_binary_expr(self)

class Unary(Expr):
    def __init__(self, operator, right_expr):
        self.operator = operator
        self.right = right_expr
    def accept(self, visitor):
        return visitor.visit_unary_expr(self)

class Grouping(Expr):
    def __init__(self, expression):
        self.expression = expression
    def accept(self, visitor):
        return visitor.visit_grouping_expr(self)

class Stmt:
    def accept(self, visitor):
        raise NotImplementedError()

class Expression(Stmt):
    def __init__(self, expression):
        self.expression = expression
    def accept(self, visitor):
        return visitor.visit_expression_stmt(self)

class Print(Stmt):
    def __init__(self, expression):
        self.expression = expression
    def accept(self, visitor):
        return visitor.visit_print_stmt(self)