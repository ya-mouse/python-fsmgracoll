from fsmsock import proto
from fsmipmi.proto import IpmiUdpClient

TYPE_INT16      = 1
TYPE_UINT16     = 2
TYPE_UINT32     = 3
TYPE_FLOAT32    = 5

class AgentClient():
    def __init__(self, agent, type, tag):
        self._agent = agent
        self._type  = type
        if len(tag) != 2:
            self._tag = (tag[0], '')
        else:
            self._tag = (tag[0], '.'+tag[1])

class SnmpUdpAgent(proto.snmp.SnmpUdpClient, AgentClient):
    def __init__(self, agent, host, type, tag, interval, version, community, points):
        self._points = points
        self._oids = { d[0] : [ k, d ] for k, d in self._points.items() }
        proto.snmp.SnmpUdpClient.__init__(self, host, interval, version, community, [x[0] for x in self._points.values()])
        AgentClient.__init__(self, agent, type, tag)

    def _value(self, oid, val, tm):
        d = self._oids[str(oid)]
        v = float(SnmpUdpAgent._get_value(val, d[1][1])) / d[1][2]
#        self._agent.send(self._tag[0]+'.'+d[0]+self._tag[1], v, tm)
        print(self._tag[0]+'.'+d[0]+self._tag[1], v, tm)

    @staticmethod
    def _get_value(v, t):
        if t == TYPE_INT16:
            return unpack('h', pack('H', v))[0]
        elif t == TYPE_UINT16 or t == TYPE_UINT32:
            return v
        elif t == TYPE_FLOAT32:
            return unpack('f', pack('I', v))[0]
        return None

    def stop(self):
        # Run forever
        pass

class IpmiUdpAgent(IpmiUdpClient, AgentClient):
    def __init__(self, agent, host, type, tag, interval):
        IpmiUdpClient.__init__(self, host, interval)
        AgentClient.__init__(self, agent, type, tag)

    def _value(self, point, val, tm):
        print(self._tag[0]+'.'+point+self._tag[1], val, tm)

    def stop(self):
        # Run forever
        pass

if __name__ == '__main__':
    import sys
    from fsmsock import async
    fsm = async.FSMSock()
    udp = SnmpUdpAgent(None, sys.argv[1], -1, ('GraColl','five_sec'), 4.0, '1', 'public', {'UPS.output-current.l1': [ '1.3.6.1.2.1.33.1.4.4.1.3.1', TYPE_UINT32, 10.0 ]})
#    udp = IpmiUdpAgent(None, sys.argv[1], -1, ('IPMI',), 3.0)
    fsm.connect(udp)
    while fsm.run():
        fsm.tick()
