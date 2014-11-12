from time import time
from fsmsock import proto
from fsmipmi.proto import IpmiUdpClient

from .agent import AgentClient

class IpmiUdpAgent(IpmiUdpClient, AgentClient):
    def __init__(self, agent, host, type, tag, interval, user='ADMIN', passwd='ADMIN', cmds=[], vendors={}, sdrs=()):
        IpmiUdpClient.__init__(self, host, interval, user, passwd, cmds, vendors, sdrs)
        AgentClient.__init__(self, agent, type, tag)

    def on_disconnect(self):
        # Do not actually remove ourself from async
        pass

    def on_data(self, point, val, tm):
        self._agent(self._tag[0]+'.'+point+self._tag[1], val, tm)

    def stop(self):
        # Run forever
        self._expire = time() + 5.0
