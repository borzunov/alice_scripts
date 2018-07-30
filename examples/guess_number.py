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
