#!/usr/bin/env python3
import sys
from lexer import *

# Базовый класс для всех выражений
class ExprAST:
    def evaluate(self):
        raise NotImplementedError

# Класс для числовых выражений
class NumberExprAST(ExprAST):
    def __init__(self, value):
        self.value = value

    def evaluate(self):
        return self.value

    def __repr__(self) -> str:
        return str(self.value)

# Класс для строковых выражений
class StringExprAST(ExprAST):
    def __init__(self, value):
        self.value = value

    def evaluate(self):
        print(self.value, end='')
        return ""

    def __repr__(self) -> str:
        return str(self.value)

# Класс для выражений переменных
class VariableExprAST(ExprAST):
    def __init__(self, name):
        self.name = name

    def evaluate(self):
        if self.name in named_values:
            var = named_values[self.name]
            if var['type'] == 'array':
                raise RuntimeError(f"Array {self.name} used without index")
            return var['value']
        raise RuntimeError(f"Unknown variable name: {self.name}")
    
    def __repr__(self) -> str:
        return str(self.name)

# Класс для бинарных выражений
class BinaryExprAST(ExprAST):
    def __init__(self, operator, lhs, rhs):
        self.operator = operator
        self.lhs = lhs
        self.rhs = rhs

    def evaluate(self):
        left_value = self.lhs.evaluate()
        right_value = self.rhs.evaluate()
        
        if self.operator == ord('/'):
            if right_value == 0:
                raise ZeroDivisionError("Division by zero")
            return left_value / right_value

        result = {
            ord('+'): left_value + right_value,
            ord('-'): left_value - right_value,
            ord('*'): left_value * right_value,
            TOKEN_EQ: left_value == right_value,
            TOKEN_NE: left_value != right_value,
            TOKEN_LT: left_value < right_value,
            TOKEN_LE: left_value <= right_value,
            TOKEN_GT: left_value > right_value,
            TOKEN_GE: left_value >= right_value,
            TOKEN_AND: left_value and right_value,
            TOKEN_OR: left_value or right_value,
        }[self.operator]
        return result

    def __repr__(self) -> str:
        op = {
            TOKEN_EQ: "=",
            TOKEN_NE: "!=",
            TOKEN_LT: "<",
            TOKEN_LE: "<=",
            TOKEN_GT: ">",
            TOKEN_GE: ">=",
            TOKEN_AND: "и",
            TOKEN_OR: "или",
        }.get(self.operator, None)
        if op is None:
            try:
                op = chr(self.operator)
            except:
                op = str(self.operator)
        return f"{self.lhs} {op} {self.rhs}"

# Класс для if-выражений
class IfExprAST(ExprAST):
    def __init__(self, condition, then_expr):
        self.condition = condition
        self.then_expr = then_expr

    def evaluate(self):
        if self.condition.evaluate():
            return self.then_expr.evaluate()
        return 0.0
    
    def __repr__(self) -> str:
        return f"{self.condition} {self.then_expr} if"

# Класс для блоков выражений
class BlockExprAST(ExprAST):
    def __init__(self, expressions):
        self.expressions = expressions

    def evaluate(self):
        result = 0.0
        for expr in self.expressions:
            result = expr.evaluate()
        return result

    def __repr__(self) -> str:
        return " ; ".join(str(expr) for expr in self.expressions)

# Класс для работы с массивами
class ArrayExprAST(ExprAST):
    def __init__(self, name, index):
        self.name = name
        self.index = index

    def evaluate(self):
        if self.name in named_values:
            if named_values[self.name]['type'] == 'array':
                idx = int(self.index.evaluate())
                array = named_values[self.name]['value']
                if 0 <= idx < len(array):
                    return array[idx]
                else:
                    raise IndexError("Array index out of bounds")
        raise RuntimeError(f"Unknown array name: {self.name}")
    
    def __repr__(self) -> str:
        return f"{self.name}[{self.index}]"
    
# Класс для объявления массивов
class ArrayDeclarationExprAST(ExprAST):
    def __init__(self, name, size):
        self.name = name
        self.size = size

    def evaluate(self):
        named_values[self.name] = {'type': 'array', 'value': [0] * self.size}
        return 0.0
    
    def __repr__(self) -> str:
        return f"{self.name}[{self.size}] array"

# Класс для присваивания переменных
class VariableAssignmentExprAST(ExprAST):
    def __init__(self, name, expr, index=None):
        self.name = name
        self.expr = expr
        self.index = index

    def evaluate(self):
        value = self.expr.evaluate()
        if self.index:  # Это массив
            if self.name in named_values and named_values[self.name]['type'] == 'array':
                idx = int(self.index.evaluate())
                array = named_values[self.name]['value']
                if 0 <= idx < len(array):
                    array[idx] = value
                else:
                    raise IndexError("Array index out of bounds")
            else:
                raise RuntimeError(f"Unknown array name: {self.name}")
        else:  # Это обычная переменная
            if self.name in named_values:
                named_values[self.name]['value'] = value
            else:
                raise RuntimeError(f"Unknown variable name: {self.name}")
        return value
    
    def __repr__(self):
        if self.index:
            return f"{self.name}[{self.index}] = {self.expr}"
        return f"{self.name} = {self.expr}"

# Класс для объявления переменных
class VariableDeclarationExprAST(ExprAST):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

    def evaluate(self):
        value = self.expr.evaluate()
        named_values[self.name] = {'type': 'int', 'value': value}
        return value

    def __repr__(self) -> str:
        return f"{self.name} = {self.expr}"

# Класс для while-выражений
class WhileExprAST(ExprAST):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def evaluate(self):
        result = 0.0
        while self.condition.evaluate():
            result = self.body.evaluate()
        return result
    
    def __repr__(self):
        return f"{self.condition} {self.body} while"

# Класс для print-выражений
class PrintExprAST(ExprAST):
    def __init__(self, expr):
        self.expr = expr

    def evaluate(self):
        result = self.expr.evaluate()
        print(result, end='')
        return result
    
    def __repr__(self) -> str:
        return f"{self.expr} print"

# Класс для endl-выражений
class EndlExprAST(ExprAST):
    def evaluate(self):
        print()
        return 0.0
    
    def __repr__(self) -> str:
        return "endl"

# Класс для input-выражений
class InputExprAST(ExprAST):
    def __init__(self, name):
        self.name = name

    def evaluate(self):
        if self.name in named_values:
            value = float(input())
            named_values[self.name]['value'] = value
            return value
        raise RuntimeError(f"Unknown variable name: {self.name}")

    def __repr__(self) -> str:
        return f"{self.name} input"

# Глобальные переменные
named_values = {}

# Лексер
lexer = None
current_token = None

def get_next_token():
    global current_token
    current_token = lexer.get_token()
    try:
        token_char = chr(current_token)
    except:
        token_char = current_token
    return current_token

def parse_expression():
    lhs = parse_primary()
    if not lhs:
        raise RuntimeError("Error in parse_expression")
    return parse_bin_op_rhs(0, lhs)

def parse_number_expr():
    result = NumberExprAST(lexer.num_val)
    get_next_token()
    return result

def parse_string_expr():
    result = StringExprAST(lexer.string_val)
    get_next_token()
    return result

def parse_paren_expr():
    get_next_token()
    expression = parse_expression()
    if not expression:
        raise RuntimeError("Error in parse_expression")
    if current_token != ord(')'):
        raise RuntimeError("Expected ')'")
    get_next_token()
    return expression

def parse_identifier_expr():
    identifier_name = lexer.identifier_str
    get_next_token()
    if current_token == ord('['):
        get_next_token()
        index = parse_expression()
        if current_token != ord(']'):
            raise RuntimeError("Expected ']' after array index")
        get_next_token()
        if current_token == ord('='):
            get_next_token()
            expr = parse_expression()
            return VariableAssignmentExprAST(identifier_name, expr, index)
        return ArrayExprAST(identifier_name, index)
    if current_token == ord('='):
        get_next_token()
        expr = parse_expression()
        return VariableAssignmentExprAST(identifier_name, expr)
    return VariableExprAST(identifier_name)

def parse_while_expr():
    get_next_token()
    if current_token != ord('('):
        raise RuntimeError("Expected '('")
    get_next_token()
    condition = parse_expression()
    if not condition:
        raise RuntimeError("Expected condition")
    if current_token != ord(')'):
        raise RuntimeError("Expected ')'")
    get_next_token()
    if current_token != ord('{'):
        raise RuntimeError("Expected '{'")
    body = parse_block()
    if not body:
        raise RuntimeError("Expected body")
    return WhileExprAST(condition, body)

def parse_print_expr():
    get_next_token()
    expr = parse_expression()
    if not expr:
        raise RuntimeError("Expected expression")
    return PrintExprAST(expr)

def parse_endl_expr():
    get_next_token()
    return EndlExprAST()

def parse_input_expr():
    get_next_token()
    if current_token != TOKEN_IDENTIFIER:
        raise RuntimeError("Expected identifier")
    identifier_name = lexer.identifier_str
    get_next_token()
    return InputExprAST(identifier_name)

def parse_primary():
    if current_token == TOKEN_IDENTIFIER:
        return parse_identifier_expr()
    if current_token == TOKEN_NUMBER:
        return parse_number_expr()
    if current_token == TOKEN_STRING:
        return parse_string_expr()
    if current_token == ord('('):
        return parse_paren_expr()
    if current_token == TOKEN_IF:
        return parse_if_expr()
    if current_token == TOKEN_WHILE:
        return parse_while_expr()
    if current_token == TOKEN_PRINT:
        return parse_print_expr()
    if current_token == TOKEN_ENDL:
        return parse_endl_expr()
    if current_token == TOKEN_INPUT:
        return parse_input_expr()
    return None

def get_token_precedence():
    return {
        ord('+'): 10,
        ord('-'): 10,
        ord('*'): 20,
        ord('/'): 20,
        TOKEN_EQ: 5,
        TOKEN_NE: 5,
        TOKEN_LT: 15,
        TOKEN_LE: 15,
        TOKEN_GT: 15,
        TOKEN_GE: 15,
        TOKEN_AND: 3,
        TOKEN_OR: 1
    }.get(current_token, -1)

def parse_bin_op_rhs(expr_prec, lhs):
    while True:
        token_prec = get_token_precedence()
        if token_prec < expr_prec:
            return lhs
        bin_op = current_token
        get_next_token()
        rhs = parse_primary()
        if not rhs:
            raise RuntimeError("Expected right-hand side expression")
        next_prec = get_token_precedence()
        if token_prec < next_prec:
            rhs = parse_bin_op_rhs(token_prec + 1, rhs)
            if not rhs:
                raise RuntimeError("Expected right-hand side expression")
        lhs = BinaryExprAST(bin_op, lhs, rhs)

def parse_block():
    get_next_token()
    expressions = []
    while current_token != ord('}') and current_token != TOKEN_EOF:
        if current_token == ord(';'):
            get_next_token()
            continue
        expr = parse_expression()
        if not expr:
            raise RuntimeError("Expected expression")
        expressions.append(expr)
        if current_token != ord(';'):
            raise RuntimeError("Expected ';' at the end of expression")
        get_next_token()
    if current_token != ord('}'):
        raise RuntimeError("Expected '}' at the end of block")
    get_next_token()
    if len(expressions) == 1:
        return expressions[0]
    return BlockExprAST(expressions)

def parse_if_expr():
    get_next_token()
    if current_token != ord('('):
        raise RuntimeError("Expected '(' after 'if'")
    get_next_token()
    condition = parse_expression()
    if not condition:
        raise RuntimeError("Expected condition")
    if current_token != ord(')'):
        raise RuntimeError("Expected ')' after condition")
    get_next_token()
    if current_token != ord('{'):
        raise RuntimeError("Expected '{' after 'if'")
    then_expr = parse_block()
    if not then_expr:
        raise RuntimeError("Expected then expression")
    return IfExprAST(condition, then_expr)

def parse_int_decl():
    get_next_token()
    if current_token != TOKEN_IDENTIFIER:
        raise RuntimeError("Expected identifier after 'int'")
    identifier_name = lexer.identifier_str
    get_next_token()
    if current_token == ord('['):
        get_next_token()
        if current_token != TOKEN_NUMBER:
            raise RuntimeError("Expected number in array declaration")
        array_size = int(lexer.num_val)
        get_next_token()
        if current_token != ord(']'):
            raise RuntimeError("Expected ']' after array size")
        get_next_token()
        return ArrayDeclarationExprAST(identifier_name, array_size)
    if current_token != ord('='):
        raise RuntimeError("Expected '=' after identifier")
    get_next_token()
    expr = parse_expression()
    if not expr:
        raise RuntimeError("Expected expression")
    return VariableDeclarationExprAST(identifier_name, expr)

def handle_file(filename):
    global lexer
    with open(filename, 'r') as file:
        lexer = Lexer(file)
        while True:
            get_next_token()
            if current_token == TOKEN_EOF:
                break
            if current_token == ord(';'):
                continue
            ast = None
            if current_token == TOKEN_INT:
                ast = parse_int_decl()
            else:
                ast = parse_expression()
            print(ast)
            try:
                if ast:
                    ast.evaluate()
                else:
                    raise RuntimeError("Error parsing expression")
            except Exception as e:
                print("Error :", e)
                print("AST: ", ast)
                return

if __name__ == "__main__":
    if len(sys.argv) > 1:
        handle_file(sys.argv[1])
    else:
        print("Usage: main.py <filename>")