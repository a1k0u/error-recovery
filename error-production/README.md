# Сборка

##### Зависимости
  - Ply

##### Установка зависимостей

Установите в своё виртуальное окружение билиотеку `ply`

```bash
pip install ply
```

##### Запуск парсера
```
python parse.py <path_to_file>
```
Результат сохраняется в `<path_to_file>.out`.

##### Запуск скрипта с тестами. 
```
./run_tests.sh [FILE]...
```


# Описание языка

Пусть у нас есть какой-то абстрактный язык программирования, в котором перед оператором `else` не требуется `;` (например в качестве такого абстрактного языка можно взять `Pascal`).  Напишем грамматику, описывающую `if statement` в таком языке.

```
if-statement -> IF boolean-expr THEN 
                statement else-part
else-part    -> ELSE statement | EPS 
statement    -> ID ASSIGN ID
boolean-expr -> ID EQ ID
```

Эта грамматика не использует `Error production` для восстановления после ошибок. 

# Описание грамматики с Error production

Мы хотим добавить в грамматику вывод, который позволяет парсеру находить такую синтаксическую ошибку. Стоит заметить, что это всё ещё будет синтаксической ошибкой, мы изменяем грамматику только для того, чтобы парсер смог вывести такую цепочку и сообщить об ошибке.

Новая грамматика:
```
if-statement -> IF boolean-expr THEN 
                statement else-part
else-part    -> ELSE statement | EPS | SEMICOLON ELSE statement 
statement    -> ID EQ ID
boolean-expr -> ID EQ ID
```