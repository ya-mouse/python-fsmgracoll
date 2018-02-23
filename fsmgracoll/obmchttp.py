import select
from time import time
from fsmhttp.proto import OpenBmcHttpClient

from .agent import AgentClient

class OpenBmcHttpAgent(OpenBmcHttpClient, AgentClient):
    def __init__(self, agent, host, type, tag, interval, user, passwd, points, keepalive=True, port=80):
        OpenBmcHttpClient.__init__(self, host, interval, user, passwd, points, keepalive, port)
        AgentClient.__init__(self, agent, type, tag)

    def on_disconnect(self):
        pass

    def on_data(self, point, context, val, tm):
        if val == 'na':
            return
        metric = point[0].format(**context)
        self._agent(self._tag[0]+'.'+metric, float(val) / point[1] if point[1] != 1 else val, tm)

    def stop(self):
        # Run forever
        self._bytes_to_read = -1
        if not self._expire:
            self._expire = self._start + self._interval
            self._start = self._expire
        if not self._timeout:
            self._timeout = time() + 15.0

        if not self._keepalive:
            self._state = self.INIT
            self._retries = 0
            if self._sock != None:
                self._sock.close()
                self._sock = None
            return -1

        return 0
