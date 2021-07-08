class Expr:
    pass

class Binary(Expr):
    def __init__(self, expr_left, token_operator, expr_right):
        self.expr_left = expr_left
        self.token_operator = token_operator
        self.expr_right = expr_right

class Grouping(Expr):
    def __init__(self, expr_expression):
        self.expr_expression = expr_expression

class Literal(Expr):
    def __init__(self, object_value):
        self.object_value = object_value

class Unary(Expr):
    def __init__(self, token_operator, expr_right):
        self.token_operator = token_operator
        self.expr_right = expr_right

