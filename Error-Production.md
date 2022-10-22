# Error production recovery method

## Описание метода

Error production - один из методов восстановления после ошибок типа Ad Hoc. 

Основная идея метода Error production в том, что теперь некоторые синтаксические ошибки становятся частью грамматики. При этом синтаксис самого языка не меняется. Изменения в грамматику вносятся для того, чтобы цепочки, которые не лежат в языке, можно было обработать и продолжить парсинг.

## Плюсы
1. Разработчик парсера понимает, какие синтаксические ошибки встречаются чаще всего (ex. после statement пропущен semicolon) и может обработать именно их.
1. Метод можно использовать в совокупности с другими методами восстановления. Это удобно, потому что Error production не может обработать все ошибки, а только те, о которых подумали разработчики парсера, тем не менее часто он бывает удобнее других методов.
1. Хорошо читаемые сообщения об ошибках.

## Минусы
1. При изменении грамматики языка, меняется и грамматика, которая позволяет находить ошибки. Тяжело поддерживать в крупных проектах.
1. Невозможно обработать все ошибки, а только те, о которых подумал разработчик парсера.

## Пример

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

# Влияние на производительность парсера

Основная суть метода `Error production` в том, что мы добавляем выводы в грамматику, которые позволяют нам обрабатывать ошибки. Добавление выводов в грамматику не влияют на производительность парсера.