__all__ = ['suggest']


def suggest(*options):
    def modifier(response):
        if 'buttons' not in response:
            response['buttons'] = []

        response['buttons'] += [{'title': item, 'hide': True}
                                for item in options]

    return modifier
