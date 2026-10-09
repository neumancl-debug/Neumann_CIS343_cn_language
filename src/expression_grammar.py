# AST classes for expressions in the CN language
class Expr:
    def accept(self, visitor):
        raise NotImplementedError()
    
class Literal(Expr):
        def __init__(self, value):
            self.value = value
        def accept(self, visitor):
            return visitor.visit_literal(self)

class Binary(Expr):
    def __init__(self, left_expr, operator, right_expr):
        self.left = left_expr
        self.operator = operator
        self.right = right_expr
    def accept(self, visitor):
        return visitor.visit_binary(self)

class Unary(Expr):
    def __init__(self, operator, right_expr):
        self.operator = operator
        self.right = right_expr
    def accept(self, visitor):
        return visitor.visit_unary(self)

class Grouping(Expr):
    def __init__(self, expression):
        self.expression = expression
    def accept(self, visitor):
        return visitor.visit_grouping(self)

    