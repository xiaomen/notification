# -*- coding: utf-8 -*-

import os
import web

from gevent.queue import Queue 
from jinja2 import Environment, FileSystemLoader

urls = ('/long', 'long_polling',
        '/queue', 'queue',
        '/.*', 'index')

jinja_env = Environment(
    loader=FileSystemLoader(os.path.join(os.path.dirname(__file__),
                            'templates')),
    extensions=[])
jinja_env.globals.update({})

message_queue = Queue()

class index:

    def GET(self):
        return jinja_env.get_template('index.html').render()

    def POST(self):
        user_data = web.input()
        message_queue.put(user_data['message'])
        return web.seeother('/')

class queue:

    def GET(self):
        return ' '.join(list(message_queue.queue))

class long_polling:

    def GET(self):
        message = message_queue.get()
        return message


app = web.application(urls, globals())
wsgi_app = app.wsgifunc()

if __name__ == "__main__":
    app.run()
