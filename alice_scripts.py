import logging
import random
import re
import threading

import flask
import pymorphy2
from werkzeug.local import LocalProxy


request = LocalProxy(lambda: flask.g.request)


class Skill(flask.Flask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._sessions = {}
        self._session_lock = threading.RLock()

        @self.before_request
        def save_request():
            flask.g.request = Request(flask.request.json)

    def script(self, generator):
        @self.route("/", methods=['POST'])
        def handle_post():
            logging.debug('Request: %r', request)

            content = self._switch_state(generator)
            response = {
                'version': request['version'],
                'session': request['session'],
                'response': content,
            }

            logging.debug('Response: %r', response)
            return flask.jsonify(response)

        return generator

    def _switch_state(self, generator):
        session_id = request['session']['session_id']
        with self._session_lock:
            if session_id not in self._sessions:
                state = self._sessions[session_id] = generator()
            else:
                state = self._sessions[session_id]

        content = next(state)

        if content['end_session']:
            with self._session_lock:
                del self._sessions[session_id]
        return content


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


def suggest(*options):
    def modifier(response):
        if 'buttons' not in response:
            response['buttons'] = []

        response['buttons'] += [{'title': item, 'hide': True}
                                for item in options]

    return modifier
