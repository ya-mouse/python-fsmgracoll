from time import time
from fsmbacnet.proto import BacnetUdpClient

from .agent import AgentClient

class BacnetUdpAgent(BacnetUdpClient, AgentClient):
    def __init__(self, agent, host, type, tag, interval, device, props):
        BacnetUdpClient.__init__(self, host, interval, device, props)
        AgentClient.__init__(self, agent, type, tag)

    def on_disconnect(self):
        pass

    def on_data(self, prop, val, tm):
        self._agent(self._tag[0]+'.'+prop+self._tag[1], val, tm)

    def stop(self):
        # Run forever
        if not self._expire:
            self._expire = self._start + self._interval
            self._start = self._expire
        if not self._timeout:
            self._timeout = time() + 15.0
