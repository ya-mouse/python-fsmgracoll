from time import time
from struct import pack, unpack
from fsmsock import proto
from fsmodbus.proto import *
import logging

from .agent import AgentClient
from .types import *

class ModbusAgentClient(AgentClient):
    def on_data(self, bufidx, response, tm):
        for regnum, data in self._regs[bufidx]['points'].items():
            v = ModbusAgentClient._get_value(response, regnum, data[0])
            if not v is None:
                data[2](self, tm, v / data[1], data[3])
#                logging.debug((self._tag[0]+".%s %.3f %.3f") % (data[3], v / data[1], tm))

    @staticmethod
    def _get_value(r, idx, t):
        if t is None or r[0] is None:
            return None
        elif t == TYPE_INT16:
            return unpack('h', pack('H', r[idx]))[0]
        elif t == TYPE_UINT16:
            return r[idx]
        elif t == TYPE_UINT32:
            return (r[idx] << 16) | r[idx+1]
        elif t == TYPE_INT32:
            return unpack('i', pack('I', ((r[idx] << 16) | r[idx + 1]) ))[0]
        elif t == TYPE_FLOAT32:
            return unpack('f', pack('I', ((r[idx] << 16) | r[idx + 1]) ))[0]
        return None

    @classmethod
    def _send_register(cls, obj, tm, value, point):
        obj._agent.send(obj._tag[0]+'.'+point+obj._tag[1], value, tm)

    @classmethod
    def _send_bits(cls, obj, tm, value, bits):
        value = int(value)
        for bit, point in bits.items():
            obj._agent.send(obj._tag[0]+'.'+point+obj._tag[1], (value & (1 << bit)) >> bit, tm)

class ModbusTcpAgent(ModbusTcpClient, ModbusAgentClient):
    def __init__(self, agent, host, type, tag, interval, slave, func, regs, rps=None):
        ModbusTcpClient.__init__(self, host, interval, slave, func, regs, rps=rps)
        ModbusAgentClient.__init__(self, agent, type, tag)

    def on_data(self, points, response, tm):
        for regnum, data in points:
            v = ModbusAgentClient._get_value(response, regnum, data[0])
            if v is not None:
                data[2](self, tm, v / data[1], data[3])
#                logging.debug('{}{} {:.3} {:.3}'.format(self._tag[0], data[3], v / data[1], tm))

    def on_disconnect(self):
        super().on_disconnect()
        if self._sock:
            self._sock.close()

    def stop(self):
        # Run forever
        self._expire = time() + self._interval
        self._timeout = self._expire + 15.0

class ModbusRtuAgent(ModbusRtuClient, ModbusAgentClient):
    def __init__(self, agent, host, type, tag, interval, slave, func, serial, regs):
        ModbusRtuClient.__init__(self, host, interval, slave, func, serial, regs)
        ModbusAgentClient.__init__(self, agent, type, tag)

    def on_data(self, *args):
        ModbusAgentClient.on_data(self, *args)

    def on_disconnect(self):
        super().on_disconnect()
        if self._sock:
            self._sock.close()

    def stop(self):
        # Run forever
        self._expire = time() + self._interval
        self._timeout = self._expire + 15.0

class ModbusRealcomAgent(ModbusRealcomClient, ModbusAgentClient):
    def __init__(self, agent, host, type, tag, interval, slave, func, serial, realcom_port, regs):
        ModbusRealcomClient.__init__(self, host, interval, slave, func, serial, realcom_port, regs)
        ModbusAgentClient.__init__(self, agent, type, tag)

    def on_data(self, *args):
        ModbusAgentClient.on_data(self, *args)

    def on_disconnect(self):
        super().on_disconnect()
        if self._sock:
            self._sock.close()
        if self._cmd._sock:
            self._cmd._sock.close()

    def stop(self):
        # Run forever
        self._expire = time() + self._interval
        self._timeout = self._expire + 15.0
