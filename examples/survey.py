from alice_scripts import Skill, request, say, suggest


skill = Skill(__name__)


@skill.script
def run_script():
    yield say('Добрый день! Как вас зовут?')
    name = request.command

    yield say('Сколько вам лет?')
    while not request.matches(r'\d+'):
        yield say('Я вас не поняла. Скажите число')
    age = int(request.command)

    yield say('Вы любите кошек или собак?',
              suggest('Обожаю кошечек', 'Люблю собак'))
    while not request.has_lemmas('кошка', 'кошечка',
                                 'собака', 'собачка'):
        yield say('У вас только два варианта - кошки или собаки')
    loves_cats = request.has_lemmas('кошка', 'кошечка')

    yield say(f'Рада познакомиться, {name}! Когда вам '
              f'исполнится {age + 1}, я могу подарить '
              f'{"котёнка" if loves_cats else "щенка"}!',
              end_session=True)
