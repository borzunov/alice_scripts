from alice_scripts import Skill, request, say


skill = Skill(__name__)


@skill.script
def run_script():
    yield from say_hi()

    lo = 1
    hi = 100
    while lo < hi:
        middle = (lo + hi) // 2
        yield say('А ваше число больше {}?'.format(middle),
                  'Правда ли, что число больше {}?'.format(middle))

        if (yield from ask_yes_or_no()):
            lo = middle + 1
        else:
            hi = middle

    yield say('Думаю, вы загадали число {}!'.format(lo),
              end_session=True)


def say_hi():
    yield say('Загадайте число от 1 до 100, а я его отгадаю. Готовы?')


def ask_yes_or_no():
    while True:
        if request.has_lemmas('нет', 'не'):
            return False
        if request.has_lemmas('да', 'ага'):
            return True

        yield say('Я вас не поняла. Скажите "да" или "нет"')
