import logging
import threading

import flask

from .requests import Request, request


__all__ = ['Skill']


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
