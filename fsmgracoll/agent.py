import os, sys
import socket
import signal
import cProfile
from zlib import crc32
from setproctitle import setproctitle

from fsmsock import proto, async

from errno import EALREADY, EINPROGRESS, EWOULDBLOCK, ECONNRESET, EINVAL, \
     ENOTCONN, ESHUTDOWN, EINTR, EISCONN, EBADF, ECONNABORTED, EPIPE, EAGAIN, \
     ECONNREFUSED, ETIMEDOUT, errorcode

_DISCONNECTED = frozenset((ECONNRESET, ENOTCONN, ESHUTDOWN, ECONNABORTED, EPIPE,
                           EBADF, ECONNREFUSED, ETIMEDOUT))

class AgentClient():
    def __init__(self, agent, type, tag):
        self._agent = agent
        self._type  = type
        if len(tag) != 2:
            self._tag = (tag[0], '')
        else:
            self._tag = (tag[0], '.'+tag[1])
        if not self._agent:
            self._agent = lambda x,y,z: print(x,y,z)

class Graphite:
    def __init__(self, hostname='localhost', port=42000):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.settimeout(5)
        for level, name, val in ((socket.IPPROTO_TCP, socket.TCP_NODELAY, 1),
                                 (socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1),
                                 (socket.IPPROTO_IP, socket.IP_TOS, 0x10)):
            self._sock.setsockopt(level, name, val)
        self._hostname = hostname
        self._port = port
        self._connect(0)

    def _connect(self, tm):
        self._tm = tm
        self._sock.connect_ex((self._hostname, self._port))

    def __call__(self, *args, **kwargs):
        self.send(*args, **kwargs)

    def send(self, key, val, tm):
#        print("%s %.3f %lu" % (key, val, tm))
        try:
            self._sock.send(bytes("%s %.3f %lu\n" % (key, val, tm), 'ascii'))
        except socket.error as why:
            if why.args[0] in _DISCONNECTED:
                # FIXME: make reconnect time 3.0s configurable
                # Try to reconnect after 3.0 secs
                if tm + 3.0 >= self._tm:
                    self._connect(tm)

def collector(name, cfg, agent, logger, do_profile):
    setproctitle(name)

    if do_profile:
        pr = cProfile.Profile()
        pr.enable()

    def signal_handler(signum, frame):
        if do_profile:
            pr.disable()
            pr.create_stats()
            pr.dump_stats('{0}-{1}.prof'.format(name, os.getpid()))
#        signal.signal(signal.SIGINT, signal.SIG_DFL)
#        signal.signal(signal.SIGQUIT, signal.SIG_DFL)
#        signal.signal(signal.SIGTERM, signal.SIG_DFL)
        # WRND: atexit wouldn't be called on sys.exit()
        fsm.atexit()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGQUIT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    fsm = async.FSMSock()

    for rtu in cfg:
        client = rtu['type'](agent=agent, **rtu)
        fsm.connect(client)

    while fsm.run():
        fsm.tick()

    #signal_handler(signal.SIGTERM, None)
    #os.kill(os.getpid(), signal.SIGTERM)
