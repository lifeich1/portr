import socketio
from . import index
from .model import KAModel

_m = None

def create_server(kombu_url='amqp://', async_mode='threading'):
    mgr = socketio.KombuManager(kombu_url)
    sio = socketio.Server(client_manager=mgr, async_mode=async_mode)

    global _m
    _m = KAModel(index.keys['lastdate_cache'])

    @_m.commit
    def set_alive():
        global _m
        _m.keepalive = True
        d = _m.data
        t = time.time()
        _m.data = d._replace(first_active_time=t,
                             last_active_time=t,
                             active_op='a')

    @_m.commit
    def set_dead():
        global _m
        _m.keepalive = False
        d = _m.data
        t = time.time()
        _m.data = d._replace(first_active_time=t,
                             active_op='b')

    @sio.event
    def connect(sid, environ):
        print('+++ online', sid)
        set_alive()

    @sio.event
    def auth_ctl(sid, data):
        # TODO auth client
        sio.enter_room(sid, 'pi')

    @sio.event
    def disconnect(sid):
        print('+++ offline', sid)
        set_dead()


def test_main(w=False, kombu_url='amqp://', **kwargs):
    if w:
        mgr = socketio.KombuManager(kombu_url)
        mgr.emit('sy_shutdown', {'sign':'abcd','timestamp':time.time()},room='pi')
    sio = create_server(kombu_url, **kwargs)
    from flask import Flask
    app = Flask(__name__)
    app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)
    app.run(threaded=True)
