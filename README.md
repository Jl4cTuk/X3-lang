# X3_lang

## Как работает

### Лексический анализатор
1. **Типы токенов**: Определение различных типов токенов, которые могут быть распознаны лексером.
2. **Класс `Lexer`**: Основной класс для лексического анализа.
    - **Инициализация**: Метод `__init__` инициализирует поток ввода и начальные значения для текущего символа и токенов.
    - **Метод `get_token`**: Основной метод для получения следующего токена из входного потока.
        - **Пропуск пробельных символов**: Пропускает все пробельные символы.
        - **Пропуск комментариев**: Пропускает комментарии, начинающиеся с `#`.
        - **Обработка идентификаторов и ключевых слов**: Считывает идентификаторы и ключевые слова.
        - **Обработка чисел**: Считывает числовые значения.
        - **Обработка строковых литералов**: Считывает строковые значения.
        - **Обработка конца файла**: Возвращает `TOKEN_EOF`, если достигнут конец файла.
        - **Обработка операторов и разделителей**: Считывает операторы и разделители, такие как `=`, `!`, `<`, `>`, `&`, `|` и одиночные символы.

### Транслятор
1. **Классы для AST**:
   - **ExprAST**: Базовый класс для всех выражений.
   - **NumberExprAST**: Класс для числовых выражений.
   - **StringExprAST**: Класс для строковых выражений.
   - **VariableExprAST**: Класс для выражений переменных.
   - **BinaryExprAST**: Класс для бинарных выражений.
   - **IfExprAST**: Класс для if-выражений.
   - **BlockExprAST**: Класс для блоков выражений.
   - **ArrayExprAST**: Класс для работы с массивами.
   - **ArrayDeclarationExprAST**: Класс для объявления массивов.
   - **VariableAssignmentExprAST**: Класс для присваивания переменных.
   - **VariableDeclarationExprAST**: Класс для объявления переменных.
   - **WhileExprAST**: Класс для while-выражений.
   - **PrintExprAST**: Класс для print-выражений.
   - **EndlExprAST**: Класс для endl-выражений.
   - **InputExprAST**: Класс для input-выражений.

2. **Парсинг**:
   - **get_next_token**: Получает следующий токен из лексера.
   - **parse_expression**: Парсит выражение.
   - **parse_number_expr**: Парсит числовое выражение.
   - **parse_string_expr**: Парсит строковое выражение.
   - **parse_paren_expr**: Парсит выражение в скобках.
   - **parse_identifier_expr**: Парсит выражение идентификатора.
   - **parse_while_expr**: Парсит while-выражение.
   - **parse_print_expr**: Парсит print-выражение.
   - **parse_endl_expr**: Парсит endl-выражение.
   - **parse_input_expr**: Парсит input-выражение.
   - **parse_primary**: Парсит первичное выражение.
   - **get_token_precedence**: Получает приоритет текущего токена.
   - **parse_bin_op_rhs**: Парсит правую часть бинарного оператора.
   - **parse_block**: Парсит блок выражений.
   - **parse_if_expr**: Парсит if-выражение.
   - **parse_int_decl**: Парсит объявление переменной типа int.

3. **Обработка файлов**:
   - **handle_file**: Обрабатывает файл, используя лексер и парсер.
   - **main**: Основная функция, обрабатывающая файл, переданный в качестве аргумента командной строки.

### Отлавливание ошибок в парсере и исполнителе
- Исключения генерируются с помощью оператора raise в случаях, когда что-то идет не так.
- Исключения обрабатываются в функции handle_file, где используется конструкция try-except для захвата и обработки ошибок.

Генерация исключений:

- В процессе парсинга и исполнения выражений, если происходит что-то неожиданное (например, отсутствует ожидаемый символ), генерируется исключение с описанием проблемы.

Обработка исключений:

- В handle_file, после получения AST (абстрактного синтаксического дерева) для выражения, вызывается метод evaluate, который выполняет выражение.
- Если в процессе парсинга или исполнения выражения возникает исключение, оно перехватывается блоком except, и ошибка выводится на экран.

Для улучшения обработки ошибок можно добавить более информативные сообщения об ошибках, включающие контекст, такой как номер строки и позиция в строке. Это поможет быстрее найти и исправить ошибки в исходном коде.

## Баги и недоработки
1. Не работает read. Скорее всего надо делать интерактивный режим.
2. Не сделаны вещественные числа.
3. Не сделан else для if.
4. Не сделаны string.