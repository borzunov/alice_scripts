from alice_scripts import Skill, request, say


skill = Skill(__name__)


@skill.script
def run_script():
    yield say('Загадайте число от 1 до 100, а я его отгадаю. Готовы?')

    lo = 1
    hi = 100
    while lo < hi:
        middle = (lo + hi) // 2
        yield say(f'Ваше число больше {middle}?')

        while not request.has_lemmas('да', 'ага', 'нет', 'не'):
            yield say('Я вас не поняла. Скажите "да" или "нет"')

        if request.has_lemmas('да', 'ага'):
            lo = middle + 1
        else:
            hi = middle

    yield say(f'Думаю, вы загадали число {lo}!', end_session=True)
