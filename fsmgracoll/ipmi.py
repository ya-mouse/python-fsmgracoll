from fsmsock import proto
from fsmipmi.proto import IpmiUdpClient

from agent import AgentClient

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
    udp = IpmiUdpAgent(None, sys.argv[1], -1, ('IPMI',), 3.0)
    fsm.connect(udp)
    while fsm.run():
        fsm.tick()
