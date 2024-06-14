import re

# Типы токенов
TOKEN_EOF = -1
TOKEN_NUMBER = -2
TOKEN_IDENTIFIER = -3
TOKEN_INT = -4
TOKEN_PLUS = ord('+')
TOKEN_MINUS = ord('-')
TOKEN_MULTIPLY = ord('*')
TOKEN_DIVIDE = ord('/')
TOKEN_LPAREN = ord('(')
TOKEN_RPAREN = ord(')')
TOKEN_SEMI = ord(';')
TOKEN_EQ = -9
TOKEN_NE = -10
TOKEN_LT = -11
TOKEN_LE = -12
TOKEN_GT = -13
TOKEN_GE = -14
TOKEN_AND = -15
TOKEN_OR = -16
TOKEN_IF = -17
TOKEN_ASSIGN = ord('=')
TOKEN_WHILE = -19
TOKEN_PRINT = -20
TOKEN_ENDL = -21
TOKEN_STRING = -22
TOKEN_LBRACE = ord('{')
TOKEN_RBRACE = ord('}')
TOKEN_LSQUARE = ord('[')
TOKEN_RSQUARE = ord(']')
TOKEN_COMMA = ord(',')
TOKEN_INPUT = -23
TOKEN_COMMENT = -24

class Lexer:
    def __init__(self, input_stream):
        self.input_stream = input_stream
        self.current_char = ' '  # Текущий символ, считанный из потока
        self.identifier_str = ''  # Строка для хранения идентификаторов
        self.num_val = 0  # Числовое значение токена
        self.string_val = ''  # Строковое значение токена

    def get_token(self):
        # Пропуск пробельных символов
        while self.current_char.isspace():
            self.current_char = self.input_stream.read(1)
            if not self.current_char:
                return TOKEN_EOF
        
        # Пропуск комментариев
        if self.current_char == '#':
            while self.current_char not in ('\n', '\r', ''):
                self.current_char = self.input_stream.read(1)
            if self.current_char:
                return self.get_token()

        # Обработка идентификаторов и ключевых слов
        if re.match(r'[a-zA-Zа-яА-Я]', self.current_char):
            self.identifier_str = self.current_char

            # Считываем идентификатор до конца
            while True:
                self.current_char = self.input_stream.read(1)
                if not re.match(r'[a-zA-Z0-9а-яА-Я_]', self.current_char):
                    break
                self.identifier_str += self.current_char

            # Возвращаем соответствующий токен для ключевых слов
            if self.identifier_str == "int":
                return TOKEN_INT
            if self.identifier_str == "if":
                return TOKEN_IF
            if self.identifier_str == "while":
                return TOKEN_WHILE
            if self.identifier_str == "print":
                return TOKEN_PRINT
            if self.identifier_str == "endl":
                return TOKEN_ENDL
            if self.identifier_str == "read":
                return TOKEN_INPUT
            return TOKEN_IDENTIFIER

        # Обработка чисел
        if re.match(r'\d|\.', self.current_char):
            num_str = ''
            while re.match(r'\d|\.', self.current_char):
                num_str += self.current_char
                self.current_char = self.input_stream.read(1)
            self.num_val = float(num_str)
            return TOKEN_NUMBER

        # Обработка строковых литералов
        if self.current_char == '\"':
            self.string_val = ''
            self.current_char = self.input_stream.read(1)
            while self.current_char != '\"' and self.current_char:
                self.string_val += self.current_char
                self.current_char = self.input_stream.read(1)
            self.current_char = self.input_stream.read(1)
            return TOKEN_STRING

        # Обработка конца файла
        if not self.current_char:
            return TOKEN_EOF

        # Обработка операторов и разделителей
        if self.current_char == '=':
            self.current_char = self.input_stream.read(1)
            if self.current_char == '=':
                self.current_char = self.input_stream.read(1)
                return TOKEN_EQ
            return TOKEN_ASSIGN

        if self.current_char == '!':
            self.current_char = self.input_stream.read(1)
            if self.current_char == '=':
                self.current_char = self.input_stream.read(1)
                return TOKEN_NE

        if self.current_char == '<':
            self.current_char = self.input_stream.read(1)
            if self.current_char == '=':
                self.current_char = self.input_stream.read(1)
                return TOKEN_LE
            return TOKEN_LT

        if self.current_char == '>':
            self.current_char = self.input_stream.read(1)
            if self.current_char == '=':
                self.current_char = self.input_stream.read(1)
                return TOKEN_GE
            return TOKEN_GT

        if self.current_char == '&':
            self.current_char = self.input_stream.read(1)
            if self.current_char == '&':
                self.current_char = self.input_stream.read(1)
                return TOKEN_AND

        if self.current_char == '|':
            self.current_char = self.input_stream.read(1)
            if self.current_char == '|':
                self.current_char = self.input_stream.read(1)
                return TOKEN_OR
    
        # Обработка одиночных символов (разделителей)
        single_char = self.current_char
        self.current_char = self.input_stream.read(1)

        return ord(single_char) if single_char in '+-*/(){}[],' else {
            '=': TOKEN_ASSIGN,
            ';': TOKEN_SEMI,
            '<': TOKEN_LT,
            '>': TOKEN_GT,
            '!': TOKEN_NE,
            '&': TOKEN_AND,
            '|': TOKEN_OR
        }.get(single_char, ord(single_char))
