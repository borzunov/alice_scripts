from alice_scripts import Skill, request, say, suggest


skill = Skill(__name__)


@skill.script
def run_script():
    yield from say_hi()

    lo, hi = 1, 100
    while lo < hi:
        middle = (lo + hi) // 2
        if (yield from ask_if_greater_than(middle)):
            lo = middle + 1
        else:
            hi = middle

    yield say(f'Думаю, вы загадали число {lo}!', end_session=True)


def say_hi():
    yield say('Загадайте число от 1 до 100, а я его отгадаю. Готовы?')


def ask_if_greater_than(number):
    yield say(f'Ваше число больше {number}?',
              suggest('Ну да', 'Вроде нет'))

    while not request.has_lemmas('да', 'ага', 'нет', 'не'):
        yield say('Я вас не поняла. Скажите "да" или "нет"')

    return not request.has_lemmas('нет', 'не')
