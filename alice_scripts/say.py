import random


__all__ = ['say']


def say(*args, **kwargs):
    if not all(isinstance(item, str) or callable(item)
               for item in args):
        raise ValueError('Each argument of say(...) must be str or callable')

    response = kwargs.copy()

    phrases = [item for item in args if isinstance(item, str)]
    if phrases:
        response['text'] = random.choice(phrases)

    if 'end_session' not in response:
        response['end_session'] = False

    for item in args:
        if callable(item):
            item(response)

    return response
