# -*- coding: utf-8 -*-

from fsmgracoll import snmp, ipmi, ssh2
from fsmgracoll.snmp import *

from ipmi_commands import *

config = [

  { 'host': '192.168.0.100',
    'type': snmp.SnmpUdpAgent,
    'tag': ('five_sec.Energy',),
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

  { 'host': '192.168.0.101',
    'type': ipmi.IpmiUdpAgent,
    'tag': ('M3.five_sec.locations.RU.FOL-A.testlab.GIGABYTE2.x.100321130',),
    'interval': 5.0,
    'sdrs': ipmi_sdrs,
    'vendors': ipmi_ven,
    'cmds': ipmi_cmds,
  },

  { 'host': '192.168.0.1',
    'type': ssh2.SSHAgent,
    'tag': ('SSH',),
    'interval': 5.0,
    'user': 'user',
    'passwd': 'password',
    'cmds': ('echo A.b.c 123.3','echo D.e.f 5555.0'),
  },
]
