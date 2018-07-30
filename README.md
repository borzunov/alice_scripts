alice_scripts
=============

Простой способ создавать сложные сценарии для [Яндекс.Алисы](https://dialogs.yandex.ru/)

*Библиотека не является продуктом Яндекса.*

Быстрый старт
-------------

Эта библиотека позволяет писать многоэтапные сценарии без callback-ов и ручного хранения информации о состоянии диалога.

Достаточно обычных условий и циклов:

```python
from alice_scripts import Skill, request, say

skill = Skill(__name__)

@skill.script
def run_script():
    yield say('Загадайте число от 1 до 100, а я его отгадаю. Готовы?')

    lo = 1
    hi = 100
    while lo < hi:
        middle = (lo + hi) // 2
        yield say('А ваше число больше {}?'.format(middle),
                  'Правда ли, что число больше {}?'.format(middle))

        while True:
            if request.has_lemmas('нет', 'не'):
                hi = middle
                break
            elif request.has_lemmas('да', 'ага'):
                lo = middle + 1
                break
            else:
                yield say('Я вас не поняла. Скажите "да" или "нет"')

    yield say('Думаю, вы загадали число {}!'.format(lo),
              end_session=True)
```

Запустить сценарий можно как обычное [Flask](http://flask.pocoo.org/)-приложение:

    pip install alice_scripts
    FLASK_APP=hello.py flask run --with-threads
    
Примеры
-------

* [Примеры из документации](examples)
* [Навык &laquo;Приложение для знакомств&raquo;](https://github.com/FuryThrue/WhoIsAlice/blob/master/app.py)

Интерфейс
---------

### alice_scripts.Skill

Этот класс реализует WSGI-приложение и является наследником класса [flask.Flask](http://flask.pocoo.org/docs/1.0/api/#flask.Flask). Сценарий, соответствующий приложению, регистрируется с помощью декоратора `@skill.script` (см. пример выше).

Сценарий запускается отдельно для каждого уникального значения `session_id`.

### alice_scripts.say(...)

Конструкция `yield say(...)` служит для выдачи ответа на запрос и принимает три типа параметров:

- Неименованные строковые параметры задают варианты фразы, которую нужно показать и сказать пользователю. При выполнении случайно выбирается один из вариантов:

    ```python
    yield say('Как дела?', 'Как поживаете?')
    ```

- Неименованные *модификаторы* позволяют указать дополнительные свойства ответа. Например, модификатор `suggest` (см. ниже) создаёт кнопки с подсказками для ответа:

    ```python
    yield say('Как дела?', suggest('Хорошо', 'Нормально'))
    ```

- Именованные параметры позволяют задать те поля объекта [response](https://tech.yandex.ru/dialogs/alice/doc/protocol-docpage/#response), для которых не реализовано модификаторов:

    ```python
    yield say('Здравствуйте! Это мы, хороводоведы.',
              tts='Здравствуйте! Это мы, хоров+одо в+еды.')
    ```
  
  Значения полей будут напрямую записаны в JSON-объект в ответе навыка.

### Модификаторы

- `alice_scripts.suggest(...)`

    Создаёт кнопки с подсказками для ответа:
    
    ```python
    yield say('Как дела?', suggest('Хорошо', 'Нормально'))
    ```
    
- Так как библиотека находится в стадии proof of concept, других модификаторов пока не реализовано. Тем не менее, вы можете передать указать все требуемые свойства ответа через именованные параметры в вызове `yield say(...)` или реализовать свои модификаторы.

### alice_scripts.request

Объект `request` представляет собой thread-local хранилище, содержащее информацию о последнем действии пользователя в сессии.

- С объектом `request` можно работать как со словарём, полученным из [JSON-объекта](https://tech.yandex.ru/dialogs/alice/doc/protocol-docpage/#request) в запросе к навыку:

    ```python
    original_utterance = request['request']['original_utterance'] 
    ```

- `request.command` &mdash; свойство, содержащее значение поля [command](https://tech.yandex.ru/dialogs/alice/doc/protocol-docpage/#request), из которого убраны завершающие точки.

- `request.words` &mdash; свойство, содержащее все слова (и числа), найденные в поле [command](https://tech.yandex.ru/dialogs/alice/doc/protocol-docpage/#request).

- `request.lemmas` &mdash; свойство, содержащее начальные формы слов из свойства `request.words` (полученные с помощью библиотеки [pymorphy2](http://pymorphy2.readthedocs.io/en/latest/)).

- `request.has_lemmas(...)` &mdash; метод, позволяющий проверить, были ли в запросе слова, чьи начальные формы совпадают с начальными формами указанных слов:

    ```python
    if request.has_lemmas('нет', 'не'):
        answer = 'no'
    elif request.has_lemmas('да', 'ага'):
        answer = 'yes'
    ``` 

- Так как библиотека находится в стадии proof of concept, методов проверки фразы с помощью нечёткого поиска или регулярных выражений пока не реализовано.

Разбиение сценария на подпрограммы
----------------------------------

Сценарий можно (и нужно) разбивать на подпрограммы. Каждая подпрограмма *должна* вызываться с помощью оператора `yield from` и может возвращать значение с помощью оператора `return`. См. [пример](examples/guess_number_subgens.py).

Ограничения
-----------

Хранение состояния диалога в виде состояния Python-генератора накладывает несколько ограничений:

- При перезапуске приложения все сессии будут разорваны.
- Развёрнутое веб-приложение может работать в нескольких потоках (опция [threads](http://docs.gunicorn.org/en/stable/settings.html#threads) в gunicorn), но не может работать в нескольких процессах (опция [workers](http://docs.gunicorn.org/en/stable/settings.html#workers)).

Автор
-----

The MIT License (MIT)

Copyright &copy; Александр Борзунов, 2018
