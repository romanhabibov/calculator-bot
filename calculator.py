class BinTreeNode():
    """Binary tree node."""

    def __init__(self, val, left, right):
        self.payload = val
        self.left = left
        self.right = right

    def is_leaf(self):
        """Check if node is a leaf"""
        if not self.left and not self.right:
            return True

    def calculate(self):
        """Traverse a tree and return a result result."""
        if self.is_leaf():
            return self.payload

        left_res = self.left.calculate()
        right_res = self.right.calculate()
        if self.payload == '+':
            return left_res + right_res
        if self.payload == '-':
            return left_res - right_res
        if self.payload == '*':
            return left_res * right_res
        if self.payload == '/':
            return left_res / right_res

class TreeBuilder():
    """TreeBuilder - a set of functions for parsing arithmetic
    expressions and constructing an abstract syntax tree by
    left-recursive descent. Class functions are handlers of one of
    the grammar rules:

    number := [0-9]+
    expr := prod ( [+ | -] Prod)*
    prod := term ( [× | /] Term)*
    term := ( expr ) | number.
    """

    def __init__(self, expression):
        self.expression = expression
        self.current_idx = 0

    def current_char(self):
        """Get character by current string index."""
        return self.expression[self.current_idx]

    def out_of_range(self):
        """Check if string index is out of range."""
        return self.current_idx >= len(self.expression)

    def get_number(self):
        """Try to process ther rule "number" (terminal) and create
        a tree leaf.
        """
        val = 0
        counter = 0
        while (not self.out_of_range() and
               (ord(self.current_char()) >= ord('0') and
               ord(self.current_char()) <= ord('9'))):
            counter += 1
            val *= 10
            val += int(self.current_char())
            self.current_idx += 1
        if not counter:
            raise RuntimeError("incorret symbol")
        result = BinTreeNode(val, None, None)

        return result

    def get_expr(self):
        """Try to process ther rule "expr" (non terminal) and
        create a tree node.
        """
        lhs = self.get_prod()
        while not self.out_of_range() and (self.current_char() == '+' or
                                           self.current_char() == '-'):
            op = self.current_char()
            self.current_idx += 1
            lhs = BinTreeNode(op, lhs, self.get_prod())
        return lhs

    def get_prod(self):
        """Try to process ther rule "prod" (non terminal) and
        create a tree node.
        """
        lhs = self.get_term()
        while (not self.out_of_range() and (self.current_char() == '*' or
                                            self.current_char() == '/')):
            op = self.current_char()
            self.current_idx += 1
            lhs = BinTreeNode(op, lhs, self.get_term())
        return lhs

    def get_term(self):
        """Try to process ther rule "term" (non terminal) and
        create a tree node.
        """
        if not self.out_of_range() and self.current_char() == '(':
            self.current_idx += 1
            result = self.get_expr()
            if not self.out_of_range() and self.current_char() == ')':
                self.current_idx += 1
            else:
                raise RuntimeError("incorrect bracket sequence")
            return result
        else:
            result = self.get_number()
        return result

def calculate_expression(string):
    """Calculate an expression and return the result."""
    try:
        tree = TreeBuilder(string).get_expr()
    except RuntimeError as err:
        return "Syntax error: "+ str(err)
    try:
        res = tree.calculate()
    except ZeroDivisionError:
        return "Calculation error: zero division"
    return res
