import re

import flask
import pymorphy2
from werkzeug.local import LocalProxy


__all__ = ['Request', 'request']


morph = pymorphy2.MorphAnalyzer()


class Request(dict):
    def __init__(self, dictionary):
        super().__init__(dictionary)

        self._command = self['request']['command'].rstrip('.')
        self._words = re.findall(r'[\w-]+', self._command, flags=re.UNICODE)
        self._lemmas = [morph.parse(word)[0].normal_form
                        for word in self._words]

    @property
    def command(self):
        return self._command

    @property
    def words(self):
        return self._words

    @property
    def lemmas(self):
        return self._lemmas

    @property
    def session_id(self):
        return self['session']['session_id']

    @property
    def user_id(self):
        return self['session']['user_id']

    def has_lemmas(self, *lemmas):
        return any(morph.parse(item)[0].normal_form in self._lemmas
                   for item in lemmas)


request = LocalProxy(lambda: flask.g.request)
