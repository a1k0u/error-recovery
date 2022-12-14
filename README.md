# Стратегии восстановление после ошибок 🧐

### Виды ошибок

Всего ошибки делят на 4 типа:

1. Лексические

2. _Синтаксические_

3. Семантические

4. _Логические_

К **лексическим** ошибкам можно отнести опечатки в ключевых 
словах или недопустимые имена переменных. 
Лексические ошибки обнаруживаются лексером.

**Синтаксические** ошибки включают в себя
несбалансированные скобки или отсутствие точки с запятой.
Обнаруживаются на этапе парсинга.

К **семантическим** ошибкам, например, относят несоответствие типов оператора и операнда.
Могут быть обнаружены статическим анализатором.

**Логические** ошибки - самые сложные.
Например, бесконечный цикл или недостижимый код. 
Могут быть обнаружены либо самим программистом, 
либо продвинутым статическим анализатором

### Почему восстановление после ошибок - важная задача парсера

Парсер при обнаружении синтаксической ошибки 
понимает, что входная цепочка не принадлежит 
языку и _может сообщить об ошибке пользователю_.

Но это не совсем то поведение, которое ожидается
от парсера. Мы, в первую очередь, ожидаем, 
что **парсер сообщит о всех синтаксических ошибках**,
допущенных во входной цепочке. 
Поэтому парсер должен уметь при обнаружении 
ошибки сообщить о ней и продолжить парсинг дальше.

Во многом для решения такой задачи и существует 
механизмы восстановления после ошибок.

## Различные способы восстановиться после ошибок

### Panic mode

###### Описание

Одна из самых простых стратегий. 
В данной стратегии парсер пропускает 
поданные на вход символы по одному, пока не дойдёт
то синхронизирующего токена.

###### Использование

Используется для поиска ошибок, связанных с 
парными токенами: открывающие и закрывающие 
скобки, `if` и `then` и т.д.

###### Преимущества

* Используется в большинстве компиляторов.
* Очень прост.

###### Недостатки

* В поисках синхронизирующего токена может 
  пропускать много токенов, которые могут содержать
  ошибки, т.е. пропускать ошибки.
* Не исправляет ошибки, но указывает на место, 
  где они были допущены.

###### Производительность

Линейное время.

###### Реализация

В папке `panic-mode` ([тык](./panic-mode)_) реализована стратегия 
на примере парсера **ПСП**. Стратегия занимается поиском 
синхронизирующих токенов, а если не находит, 
то обозначает тип ошибки и место, в котором 
ошибка совершена. В сравнении с phrase mode_ 
и _global correction_ не исправляет ошибки, 
однако более проста в написании, 
чем _error production_, и со своей функцией - 
поиском ошибок, связанных с синхронизированными 
токенами - **справляется надёжно и быстро**.

###### Пример

Строка, поданная на вход:

```
(()()()())(())())))))(((())((((()())()(((()))))
```

Отработавший _panic mode_ выводит ошибки следующим образом:

```
Unexpected closing bracket
(()()()())(())())))))(((())((((()())()(((()))))
~~~~~~~~~~~~~~~~^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Unexpected closing bracket
(()()()())(())())))))(((())((((()())()(((()))))
~~~~~~~~~~~~~~~~~^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Unexpected closing bracket
(()()()())(())())))))(((())((((()())()(((()))))
~~~~~~~~~~~~~~~~~~^~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Unexpected closing bracket
(()()()())(())())))))(((())((((()())()(((()))))
~~~~~~~~~~~~~~~~~~~^~~~~~~~~~~~~~~~~~~~~~~~~~~~
Unexpected closing bracket
(()()()())(())())))))(((())((((()())()(((()))))
~~~~~~~~~~~~~~~~~~~~^~~~~~~~~~~~~~~~~~~~~~~~~~~
Opening bracket is not closed
(()()()())(())())))))(((())((((()())()(((()))))
~~~~~~~~~~~~~~~~~~~~~~~~~~~~^~~~~~~~~~~~~~~~~~~
Opening bracket is not closed
(()()()())(())())))))(((())((((()())()(((()))))
~~~~~~~~~~~~~~~~~~~~~~~~~~~^~~~~~~~~~~~~~~~~~~~
Opening bracket is not closed
(()()()())(())())))))(((())((((()())()(((()))))
~~~~~~~~~~~~~~~~~~~~~~^~~~~~~~~~~~~~~~~~~~~~~~~
Opening bracket is not closed
(()()()())(())())))))(((())((((()())()(((()))))
~~~~~~~~~~~~~~~~~~~~~^~~~~~~~~~~~~~~~~~~~~~~~~~
```

### Phrase mode

###### Описание

В этой стратегии при нахождении локальных ошибок парсер
самостоятельно изменяет входные данные для того,
чтобы продолжить свою работу. Считается, что после скрупулёзной
работы с исправлением одной и нескольких локальных ошибок,
оставшаяся часть текста позволит парсеру продолжить 
свою работу.

###### Использование

В целом, разработчик сам решает какие первоначальные
изменения добавить в свой компилятор. В основном 
эту стратегию используют, чтобы убрать/добавить/переставить знак
конца строки.

###### Преимущества

- Множественная комбинация исправления локальных ошибок,
  есть возможность за несколько итераций исправить несколько
  локальных ошибок.
- Легко встраивается в различные грамматики.

###### Недостатки

- При неправильном анализе локальной ошибки перестановка
  может вызвать бесконечную (_некорректную_) работу парсера.
- Приходиться тратить много мыслетоплива, чтобы парсер не сломался.  

###### Производительность

Можем ограничиться сверху `inf`, потому что в сложных сценариях
локальное исправление может зациклить работу парсера.

Снизу взять `количество строк во входном файле`, так как в нем нет ошибок.

В среднем получается, что `среднее количество ошибок на строку` * `количество строк`.

###### Пример

Код на придуманном `plus-expression-variable-output-lang`,
вкратце **PEVOL**.

```python
;
1 + 1;
a;

OUT dssd = 1033 # не хватает ;
OUT ds = 1033 + 1 2; # пропущен +
OUT ds;
OUT 5 1 + aba = 1033 + 1 # нет ;, не хватает +,
                         # ожидается +, а получили = 

a = b + 1 + c + 10 # нет ;
k = a b c d + 10 + 2 5 + 1 # нет + и ;
b = 10; OUT b; b = 20; OUT b # ;

OUT k;
OUT ;
OUT # ;
```

После итеративной работы парсера, 
работа которого описана _[тут](./phrase-mode)_,
с постепенным изменением локальных ошибок получим файл
с исправленным кодом. Также вывод всех ошибок.

```python
;
1 + 1;
a;

OUT dssd = 1033;
OUT ds = 1033 + 1 + 2;
OUT ds;
OUT 5 + 1 + aba  +  1033 + 1;

a = b + 1 + c + 10;
k = a + b + c + d + 10 + 2 + 5 + 1;
b = 10; OUT b; b = 20; OUT b;

OUT k;
OUT ;
OUT;
```

Вот собственно ошибки нашего кода.

```plain
warning: expected ';' at 5 line.
warning: expected plus in expression at 6 line.
warning: expected plus, got assign at 8 line.
warning: expected ';' at 8 line.
warning: expected plus in expression at 8 line.
warning: expected ';' at 10 line.
warning: expected ';' at 11 line.
warning: expected plus in expression at 11 line.
warning: expected plus in expression at 11 line.
warning: expected plus in expression at 11 line.
warning: expected plus in expression at 11 line.
warning: expected ';' at 12 line.
warning: expected ';' at 16 line.
```

### Error production

###### Описание

**Error production** - один из методов 
восстановления после ошибок типа Ad Hoc. 
Основная идея метода Error production в том, 
что теперь некоторые синтаксические ошибки 
становятся частью грамматики. При этом синтаксис 
самого языка не меняется. Изменения в грамматику 
вносятся для того, чтобы цепочки, которые не 
лежат в языке, можно было обработать и продолжить парсинг.

###### Преимущества

- Разработчик парсера понимает, какие синтаксические ошибки встречаются чаще всего (ex. после `statement` пропущен `semicolon`) и может обработать именно их.
- Метод можно использовать в совокупности с другими методами восстановления. Это удобно, потому что **Error production** не может обработать все ошибки, а только те, о которых подумали разработчики парсера, тем не менее часто он бывает удобнее других методов.
- Хорошо читаемые сообщения об ошибках.

###### Недостатки

- При изменении грамматики языка, меняется и грамматика, которая позволяет находить ошибки. Тяжело поддерживать в крупных проектах.
- Невозможно обработать все ошибки, а только те, о которых подумал разработчик парсера.

###### Производительность

Основная суть метода `Error production` в том, что мы добавляем выводы в грамматику, которые позволяют нам обрабатывать ошибки. Добавление выводов в грамматику не влияют на производительность парсера.

###### Реализация стратегии на языке `Python`

[Error-production](./error-production)

###### Пример использования метода

Синтаксис условного оператора в языке `C++` выглядит следующим образом:

```C++
if (expr) {
    statement;
}
```

Одна из частых синтаксических ошибок - отсутствие скобок вокруг `boolean-expression`. Давайте добавим такую ошибку в грамматику языка:

```
S -> IF ROPAR boolean-expr RCPAR FOPAR statement FCPAR
S -> IF boolean-expr FOPAR statement FCPAR
IF -> if
ROPAR -> (
RCPAR -> )
FOPAR -> {
FCPAR -> }
```

В случае если вы вывели цепочку языка по правилу `S -> IF boolean-expr FOPAR statement FCPAR` мы можем сообщить об ошибке, при этом парсинг продолжится.

### Global correction

###### Описание

Эта стратегия нацелена на то, чтобы превратить неправильный ввод в правильный за как можно более минимальное число изменений, базируясь на фрагментах ввода, которые ошибок не содержат. В данный момент стратегия имеет скорее теоретический характер и в серьёзных парсерах не реализована.

###### Преимущества

* Исправляет ошибки, которые не исправляет _Phrase mode_.

* Отлично подходит для статических анализаторов кода.

###### Недостатки

* Очень медленный

* Может искажать смысл ввода: исправлять неправильную строку на правильную, но не соответствующую по смыслу той, которую пытался ввести пользователь.

###### Производительность

Как было сказано ранее, медленнее всех стратегий, упомянутых в данном проекте.

###### Реализация

В папке _global correction_ реализована на игрушечном примере парсера правильных скобочных последовательностей. В ПСП ошибки могут быть двух типов:

1) У открывающей скобки нет закрывающей

2) У закрывающей скобки нет открывающей

В случае первой ошибки парсер добавляет необходимое количество закрывающих скобок в конце строки.

Во случае второй ошибки парсер не добавляет в результирующую строку все закрывающие скобки, у которых нет открывающих.

По сравнению с _panic mode_ и _error production_. Как реализовать исправление таких ошибок с _phrase mode_ можно, но, кажется, более трудоёмко. Из минусов можно выделить тот факт, что строка может не соответствовать той, которую подразумевал пользователь

### Сравнение стратегий и заключение

Очевидно, что каждая из стратегий оптимальна в конкретных случаях, и универсального решения нет. Так, например, легко заметить, что _panic-mode_ в поисках синхронизирующего токена может пропустить ошибки в примере с грамматикой _if-then_, а _global correction_ вовсе может исказить смысл введённой строки. 

Отличаются они и по производительности: _global correction_ является наиболее вычислительно сложной из всех перечисленных, поскольку при исправлении каждой конкретной ошибки берёт во внимание весь ввод.

Немаловажно, что отличия имеют место быть и сложности реализации: _panic mode_ традиционно считается самой простой, _phrase mode_ и _error production_ требует большей работы разработчика за счёт обработки каждой отдельной ошибки.

### В ходе выполнения

###### Роман Гостило

- Ознакомился с классификацией ошибок

- Ознакомился с 4 основными стратегиями восстановления после ошибок, 2 из которых (`global correction` и `panic mode`) реализовал на примере парсера правильных скобочных последовательностей на языке `Python`

- Попрактиковался в работе с _git_, когда мерджил ветку, склонированную с ветки, склонированной с _main_

- Написал тесты, свою часть отчёта

- Прошёл путь от "я не понимаю что от меня хотят" до выполнения поставленной задачи

- Прочитал 10-15 статей и книжных глав на тему и до сих пор не уверен, что правильно всё понял

- Получил удовольствие

###### Александр Виноградов

- Изучил все возможные методы восстановления после ошибок
- Изучил некоторые уже реализованные методы восстановления в существующих генераторах парсеров
- Реализовал стратегию `error production` на языке `Python`
- Написал грамматику языка упрощенных условных выражений
- Написал тесты для парсера

###### Алексей Косенко

Встретился со всеми возможными
ошибками в ply, прочитал документацию вдоль и поперек.
Несколько раз сломал парсер (`воспроизвел бесконечный цикл`).
Прочитал несколько десятков статей про стратегию восстановлений.

В итоге Алексей Косенко:

- Написал мини-яп с суммой целых чисел, использованием
  переменных и выводом из в stdin.
- Реализовал для них стратегию `phrase-mode`, где
  локально исправлял ошибки в арифметических выражениях
  (пропущенные `+`, перепутанные `=`),
  добавлял забытые `;`.
- Написал **семь** тестов, которые покрывают разные куски кода.
- Написал свою часть репорта, описал реализацию работы своего кода.
- Поработал командно, обсуждал другие стратегии и сравнивал их.



> By Alexander Vinogradov, Alexey Kosenko and Roman Gostilo.
> 
> **@** _group project of formal languages, 2022_
