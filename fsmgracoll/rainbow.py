from time import time
from fsmsock import proto
from struct import pack,unpack
from fsmrainbow.proto import RainbowTcpClient

from .agent import AgentClient
from .types import *

class RainbowTcpAgent(RainbowTcpClient, AgentClient):
    def __init__(self, agent, host, type, tag, interval, cmds):
        RainbowTcpClient.__init__(self, host, interval, cmds)
        AgentClient.__init__(self, agent, type, tag)

    def on_disconnect(self):
        super().on_disconnect()
        if self._sock:
            self._sock.close()

    def on_data(self, points, response, tm):
        for off, info in points[2].items():
            v = 0
            if info[0] == TYPE_FLOAT16:
                v = pack('!H', int(response[off:off+4], 16))
                v = unpack('!h', v)[0] / info[1]
            elif info[0] == TYPE_UINT16:
                v = int(response[off:off+4], 16) // info[1]
            elif info[0] == TYPE_UINT8:
                v = int(response[off:off+2], 16)
            else:
                continue

            self._agent.send(self._tag[0]+'.'+info[2]+self._tag[1], v, tm)

    def stop(self):
        # Run forever
        if not self._expire:
            self._expire = self._start + self._interval
            self._start = self._expire
        if not self._timeout:
            self._timeout = time() + 15.0
