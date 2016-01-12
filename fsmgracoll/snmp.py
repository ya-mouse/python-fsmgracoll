import logging
from time import time
from fsmsnmp import proto

from .agent import AgentClient
from .types import *

class SnmpUdpAgent(proto.SnmpUdpClient, AgentClient):
    def __init__(self, agent, host, type, tag, interval, version, community, points, port=161):
        self._points = points
        self._oids = { d[0] : [ k, d ] for k, d in self._points.items() }
        proto.SnmpUdpClient.__init__(self, host, interval, version, community, [x[0] for x in self._points.values()], port)
        AgentClient.__init__(self, agent, type, tag)
        self._start = time()

    def on_data(self, oid, val, tm):
        try:
            d = self._oids[str(oid)]
            v = float(SnmpUdpAgent._get_value(val, d[1][1])) / d[1][2]
            self._agent.send(self._tag[0]+'.'+d[0]+self._tag[1], v, tm)
        except KeyError:
            logging.warning('{}: unexpected OID received {}'.format(self._host, oid))

    def on_disconnect(self):
        # Do not actually remove ourself from async
        pass

    def stop(self):
        # Run forever
        self._expire = self._start + self._interval
        self._start = self._expire
        self._timeout = time() + 15.0
        return False

    @staticmethod
    def _get_value(v, t):
        if t == TYPE_INT16:
            return unpack('h', pack('H', v))[0]
        elif t == TYPE_UINT16 or t == TYPE_UINT32:
            return v
        elif t == TYPE_FLOAT32:
            return unpack('f', pack('I', v))[0]
        return None

if __name__ == '__main__':
    import sys
    from fsmsock import async
    fsm = async.FSMSock()
    udp = SnmpUdpAgent(None, sys.argv[1], -1, ('GraColl','five_sec'), 4.0, '1', 'public', {'UPS.output-current.l1': [ '1.3.6.1.2.1.33.1.4.4.1.3.1', TYPE_UINT32, 10.0 ]})
    fsm.connect(udp)
    while fsm.run():
        fsm.tick()
