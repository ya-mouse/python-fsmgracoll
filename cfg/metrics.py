# -*- coding: utf-8 -*-

from fsmgracoll import *

from ipmi_commands import *

rainbow_points = {
  24: [ TYPE_FLOAT16, 10.0, 'outdoor_temp' ],
  28: [ TYPE_FLOAT16, 10.0, 'indoor_temp' ],
  32: [ TYPE_UINT16, 1, 'fan' ],
  36: [ TYPE_UINT16, 1, 'throttle' ],
  40: [ TYPE_UINT16, 1, 'home1' ],
  44: [ TYPE_UINT16, 1, 'home2_1' ],
  48: [ TYPE_UINT16, 1, 'home2_2' ],
  52: [ TYPE_UINT8, 1, 'motor' ],
  54: [ TYPE_FLOAT16, 10.0, 'temp1' ],
  58: [ TYPE_FLOAT16, 10.0, 'temp2' ]
}

config = [

  { 'host': '192.168.1.110',
    'type': snmp.SnmpUdpAgent,
    'tag': ('SNMP',),
    'interval': 4.0,
    'version': '1',
    'community': 'public',
    'points': {
'UPS4-3.output-current.l1': [ '1.3.6.1.2.1.33.1.4.4.1.3.1', TYPE_UINT32, 10.0 ],
'UPS4-3.output-current.l2': [ '1.3.6.1.2.1.33.1.4.4.1.3.2', TYPE_UINT32, 10.0 ],
'UPS4-3.output-current.l3': [ '1.3.6.1.2.1.33.1.4.4.1.3.3', TYPE_UINT32, 10.0 ],
'UPS4-3.output-voltage.l1': [ '1.3.6.1.2.1.33.1.4.4.1.2.1', TYPE_UINT32, 1.0 ],
'UPS4-3.output-voltage.l2': [ '1.3.6.1.2.1.33.1.4.4.1.2.2', TYPE_UINT32, 1.0 ],
'UPS4-3.output-voltage.l3': [ '1.3.6.1.2.1.33.1.4.4.1.2.3', TYPE_UINT32, 1.0 ],
'UPS4-3.battery-voltage': [ '1.3.6.1.2.1.33.1.2.5.0', TYPE_UINT32, 1.0 ],
'UPS4-3.battery-current': [ '1.3.6.1.2.1.33.1.2.6.0', TYPE_UINT32, 10.0 ],
'UPS4-3.battery-temp': [ '1.3.6.1.2.1.33.1.2.7.0', TYPE_UINT32, 1.0 ],
'UPS4-3.remaining': [ '1.3.6.1.2.1.33.1.2.3.0', TYPE_UINT32, 1.0 ],
'UPS4-3.bypass-voltage.l1': [ '1.3.6.1.2.1.33.1.5.3.1.2.1', TYPE_UINT32, 1.0 ],
'UPS4-3.bypass-voltage.l2': [ '1.3.6.1.2.1.33.1.5.3.1.2.2', TYPE_UINT32, 1.0 ],
'UPS4-3.bypass-voltage.l3': [ '1.3.6.1.2.1.33.1.5.3.1.2.3', TYPE_UINT32, 1.0 ],
'UPS4-3.alarm': [ '1.3.6.1.2.1.33.1.6.1.0', TYPE_UINT32, 1.0 ],
'UPS4-3.output-power.l1': [ '1.3.6.1.2.1.33.1.4.4.1.4.1', TYPE_UINT32, 1.0 ],
'UPS4-3.output-power.l2': [ '1.3.6.1.2.1.33.1.4.4.1.4.2', TYPE_UINT32, 1.0 ],
'UPS4-3.output-power.l3': [ '1.3.6.1.2.1.33.1.4.4.1.4.3', TYPE_UINT32, 1.0 ],
'UPS4-3.load.l1': [ '1.3.6.1.2.1.33.1.4.4.1.5.1', TYPE_UINT32, 1.0 ],
'UPS4-3.load.l2': [ '1.3.6.1.2.1.33.1.4.4.1.5.2', TYPE_UINT32, 1.0 ],
'UPS4-3.load.l3': [ '1.3.6.1.2.1.33.1.4.4.1.5.3', TYPE_UINT32, 1.0 ],
    }
  },

  { 'host': '192.168.1.112',
    'type': ipmi.IpmiUdpAgent,
    'tag': ('IPMI',),
    'interval': 5.0,
    'sdrs': ipmi_sdrs,
    'vendors': ipmi_ven,
    'cmds': ipmi_cmds,
  },

  { 'host': '192.168.1.113',
    'type': ssh2.SSHAgent,
    'tag': ('SSH',),
    'interval': 5.0,
    'user': 'ADMIN',
    'passwd': 'ADMIN',
    'cmds': ('echo A.b.c 123.3','echo D.e.f 5555.0'),
  },

  { 'host': '192.168.1.115',
    'type': netcat.NetcatUdpAgent,  # ask data with "get" word and read answer until "END" word
    'tag': ('NETCAT',),
    'interval': 5.0,
    'port': 1500, # this is default port number
  },

  { 'host': '192.168.1.114',
    'type': modbus.ModbusTcpAgent,
    'tag': ('MBUS',),
    'interval': 3.0,
    'slave': 1,
    'func': 4,
    'regs': [ { 'offset': 256,
        'read': 4,                     # registers' number to read at once
        'total': 4,                    # total registers' number
        'points': {
0: [ TYPE_INT16, 1.0, modbus.ModbusAgentClient._send_bits, { 0: 'U_2_01.temp.0', 1: 'U.1', 2: 'U.2' } ],
1: [ TYPE_INT16, 1.0, modbus.ModbusAgentClient._send_register, 'U_2_01.humidity' ],
2: [ TYPE_INT16, 1.0, modbus.ModbusAgentClient._send_register, 'U_2_01.CO2' ],
3: [ TYPE_INT16, 1.0, modbus.ModbusAgentClient._send_register, 'U_2_01.VOC' ],
        }
    } ]
  },

  { 'host': '172.19.0.49',
    'type': rainbow.RainbowTcpAgent,
    'tag': ('RAINBOW',),
    'interval': 3.0,
    'cmds': [
        [ 0x001, 0x006, rainbow_points ],
        [ 0x002, 0x006, rainbow_points ]
    ]
  }
]
