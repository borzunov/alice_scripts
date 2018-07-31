import logging
import threading

import flask

from .requests import Request


__all__ = ['Skill']


class Skill(flask.Flask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._sessions = {}
        self._session_lock = threading.RLock()

    def script(self, generator):
        @self.route("/", methods=['POST'])
        def handle_post():
            flask.g.request = Request(flask.request.get_json())
            logging.debug('Request: %r', flask.g.request)

            content = self._switch_state(generator)
            response = {
                'version': flask.g.request['version'],
                'session': flask.g.request['session'],
                'response': content,
            }

            logging.debug('Response: %r', response)
            return flask.jsonify(response)

        return generator

    def _switch_state(self, generator):
        session_id = flask.g.request['session']['session_id']
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
