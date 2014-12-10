from time import time
from fsmsock.proto import UdpTransport

from .agent import AgentClient

class NetcatUdpAgent(UdpTransport, AgentClient):
    def __init__(self, agent, host, type, tag, interval, port=1500):
        self._resp = b''
        UdpTransport.__init__(self, host, interval, port)
        AgentClient.__init__(self, agent, type, tag)

    def _build_buf(self):
        self._buf = b'get\n'

    def process_data(self, data):
        self._retries = 0
        if len(data) == 0:
            return False

        # Process data
        self._resp += data

        if b'END' in self._resp:
            tm = time()
            for s in str(self._resp, 'ascii').split('\n'):
                if s == '': continue
                if s == 'END': break
                v = s.split()
                self._agent.send(self._tag[0]+'.'+v[0]+self._tag[1], float(v[1]), tm)
            self._resp = b''
            self._state = self.READY
            return False
        return True

    def on_disconnect(self):
        # Do not actually remove ourself from async
        pass

    def stop(self):
        # Run forever
        self._expire = time() + self._interval
        self._timeout = self._expire + 15.0
