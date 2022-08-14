import ast
if 'arg' not in dir(ast):
    ast.arg = type(None)

def parse(code):
    return ast.parse(code).body

# Takes code of the form
# def foo(arg1, arg2 ...):
#     x = arg1 + arg2
#     y = ...
#     return x + y
# And extracts the inputs and the body, where
# it expects the body to be a sequence of
# variable assignments (variables are immutable;
# can only be set once) and a return statement at the end
def extract_inputs_and_body(code):
    o = []
    if len(code) != 1 or not isinstance(code[0], ast.FunctionDef):
        raise Exception("Expecting function declaration")
    # Gather the list of input variables
    inputs = []
    for arg in code[0].args.args:
        if isinstance(arg, ast.arg):
            assert isinstance(arg.arg, str)
            inputs.append(arg.arg)
        elif isinstance(arg, ast.Name):
            inputs.append(arg.id)
        else:
            raise Exception("Invalid arg: %r" % ast.dump(arg))
    # Gather the body
    body = []
    returned = False
    for c in code[0].body:
        if not isinstance(c, (ast.Assign, ast.Return)):
            raise Exception("Expected variable assignment or return")
        if returned:
            raise Exception("Cannot do stuff after a return statement")
        if isinstance(c, ast.Return):
            returned = True
        body.append(c)
    return inputs, body

# Convert a body with potentially complex expressions into
# simple expressions of the form x = y or x = y * z
def flatten_body(body):
    o = []
    for c in body:
        o.extend(flatten_stmt(c))
    return o

# Generate a dummy variable
next_symbol = [0]
def mksymbol():
    next_symbol[0] += 1
    return 'sym_'+str(next_symbol[0])

# "Flatten" a single statement into a list of simple statements.
# First extract the target variable, then flatten the expression
def flatten_stmt(stmt):
    # Get target variable
    if isinstance(stmt, ast.Assign):
        assert len(stmt.targets) == 1 and isinstance(stmt.targets[0], ast.Name)
        target = stmt.targets[0].id
    elif isinstance(stmt, ast.Return):
        target = '~out'
    # Get inner content
    return flatten_expr(target, stmt.value)

# Main method for flattening an expression
def flatten_expr(target, expr):
    # x = y
    if isinstance(expr, ast.Name):
        return [['set', target, expr.id]]
    # x = 5
    elif isinstance(expr, ast.Num):
        return [['set', target, expr.n]]
    # x = y (op) z
    # Or, for that matter, x = y (op) 5
    elif isinstance(expr, ast.BinOp):
        if isinstance(expr.op, ast.Add):
            op = '+'
        elif isinstance(expr.op, ast.Mult):
            op = '*'
        elif isinstance(expr.op, ast.Sub):
            op = '-'
        elif isinstance(expr.op, ast.Div):
            op = '/'
        # Exponentiation gets compiled to repeat multiplication,
        # requires constant exponent
        elif isinstance(expr.op, ast.Pow):
            assert isinstance(expr.right, ast.Num)
            if expr.right.n == 0:
                return [['set', target, 1]]
            elif expr.right.n == 1:
                return flatten_expr(target, expr.left)
            else: # This could be made more efficient via square-and-multiply but oh well
                if isinstance(expr.left, (ast.Name, ast.Num)):
                    nxt = base = expr.left.id if isinstance(expr.left, ast.Name) else expr.left.n
                    o = []
                else:
                    nxt = base = mksymbol()
                    o = flatten_expr(base, expr.left)
                for i in range(1, expr.right.n):
                    latest = nxt
                    nxt = target if i == expr.right.n - 1 else mksymbol()
                    o.append(['*', nxt, latest, base])
                return o
        else:
            raise Exception("Bad operation: " % ast.dump(stmt.op))
        # If the subexpression is a variable or a number, then include it directly
        if isinstance(expr.left, (ast.Name, ast.Num)):
            var1 = expr.left.id if isinstance(expr.left, ast.Name) else expr.left.n
            sub1 = []
        # If one of the subexpressions is itself a compound expression, recursively
        # apply this method to it using an intermediate variable
        else:
            var1 = mksymbol()
            sub1 = flatten_expr(var1, expr.left)
        # Same for right subexpression as for left subexpression
        if isinstance(expr.right, (ast.Name, ast.Num)):
            var2 = expr.right.id if isinstance(expr.right, ast.Name) else expr.right.n
            sub2 = []
        else:
            var2 = mksymbol()
            sub2 = flatten_expr(var2, expr.right)
        # Last expression represents the assignment; sub1 and sub2 represent the
        # processing for the subexpression if any
        return sub1 + sub2 + [[op, target, var1, var2]]
    else:
        raise Exception("Unexpected statement value: %r" % stmt.value)

