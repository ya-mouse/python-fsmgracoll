from time import time
from struct import pack, unpack
from fsmsock import proto
from fsmodbus.proto import *
import logging

from .agent import AgentClient
from .types import *

class ModbusAgentClient(AgentClient):
    def on_data(self, bufidx, response, tm):
        for k, d in self._regs[bufidx]['points'].items():
            v = ModbusAgentClient._get_value(response, d[0], d[1]) / d[2]
#            logging.debug((self._tag[0]+".%s %.3f %.3f") % (k, v, tm))
            self._agent.send(self._tag[0]+'.'+k+self._tag[1], v, tm)

    @staticmethod
    def _get_value(r, idx, t):
        if t == TYPE_INT16:
            return unpack('h', pack('H', r[idx]))[0]
        elif t == TYPE_UINT16:
            return r[idx]
        elif t == TYPE_UINT32:
            return (r[idx] << 16) | r[idx+1]
        elif t == TYPE_FLOAT32:
            return unpack('f', pack('I', ((r[idx] << 16) | r[idx + 1]) ))[0]
        return None

class ModbusTcpAgent(ModbusTcpClient, ModbusAgentClient):
    def __init__(self, agent, host, type, tag, interval, slave, func, regs):
        ModbusTcpClient.__init__(self, host, interval, slave, func, regs)
        ModbusAgentClient.__init__(self, agent, type, tag)

    def on_data(self, *args):
        ModbusAgentClient.on_data(self, *args)

    def stop(self):
        # Run forever
        self._expire = time() + 5.0

class ModbusRtuAgent(ModbusRtuClient, ModbusAgentClient):
    def __init__(self, agent, host, type, tag, interval, slave, func, serial, regs):
        ModbusRtuClient.__init__(self, host, interval, slave, func, serial, regs)
        ModbusAgentClient.__init__(self, agent, type, tag)

    def on_data(self, *args):
        ModbusAgentClient.on_data(self, *args)

    def stop(self):
        # Run forever
        self._expire = time() + 5.0

class ModbusRealcomAgent(ModbusRealcomClient, ModbusAgentClient):
    def __init__(self, agent, host, type, tag, interval, slave, func, serial, realcom_port, regs):
        ModbusRealcomClient.__init__(self, host, interval, slave, func, serial, realcom_port, regs)
        ModbusAgentClient.__init__(self, agent, type, tag)

    def on_data(self, *args):
        ModbusAgentClient.on_data(self, *args)

    def stop(self):
        # Run forever
        self._expire = time() + 5.0
