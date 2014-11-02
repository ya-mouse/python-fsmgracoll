from fsmsock import proto
from fsmipmi.proto import IpmiUdpClient

from agent import AgentClient

class IpmiUdpAgent(IpmiUdpClient, AgentClient):
    def __init__(self, agent, host, type, tag, interval, user='ADMIN', passwd='ADMIN', cmds=[], vendors={}, sdrs=()):
        IpmiUdpClient.__init__(self, host, interval, user, passwd, cmds, vendors, sdrs)
        AgentClient.__init__(self, agent, type, tag)

    def on_data(self, point, val, tm):
        print(self._tag[0]+'.'+point+self._tag[1], val, tm)

    def stop(self):
        # Run forever
        pass

if __name__ == '__main__':
    import sys
    from fsmsock import async

    sdrs = {
        'TEMP_CPU0': 'temp.cpu0',
        'TEMP_CPU1': 'temp.cpu1',
        'CPU1 TEMP': 'temp.cpu0',
        'CPU2 TEMP': 'temp.cpu1',
        'CPU0': 'temp.cpu0',
        'CPU1': 'temp.cpu1',
        'FAN1': 'fan.1',
        'FAN2': 'fan.2',
        'FAN3': 'fan.3',
        'FAN4': 'fan.4',
        'FAN5': 'fan.5',
        'FAN6': 'fan.6',
        'FAN7': 'fan.7',
        'FAN8': 'fan.8',
        'FAN9': 'fan.9',
        'FAN10': 'fan.10',
        'FAN11': 'fan.11',
        'FAN12': 'fan.12',
        'FAN13': 'fan.13',
        'FAN14': 'fan.14',
        'FAN15': 'fan.15',
        'FAN16': 'fan.16',
        'FAN17': 'fan.17',
        'FAN18': 'fan.18',
        'FAN19': 'fan.19',
        'FAN20': 'fan.20',
        'FAN21': 'fan.21',
        'FAN22': 'fan.22',
        'FAN23': 'fan.23',
        'FAN24': 'fan.24',
        'FAN25': 'fan.25',
        'FAN26': 'fan.26',
        'FAN27': 'fan.27',
        'FAN28': 'fan.28',
        'FAN29': 'fan.29',
        'FAN30': 'fan.30',
        'FAN31': 'fan.31',
        'FAN32': 'fan.32',
        'FAN33': 'fan.33',
        'FAN34': 'fan.34',
        'FAN35': 'fan.35',
        'FAN36': 'fan.36',
        'INLET': 'temp.inlet',
        'OUTLET': 'temp.outlet',
        'NODE_WATT': 'power.W',
        'UP_RACK_POWER': 'rack.power.up',
        'LOW_RACK_POWER': 'rack.power.low',
        'ALL_RACK_POWER': 'rack.power.all',
        'INLET_TEMP_UP': 'rack.temp.inlet-up',
        'INLET_TEMP_LOW': 'rack.temp.inlet-low',
        'OUTLET_UR_UP': 'rack.temp.outlet-ur-up',
        'OUTLET_UR_LOW': 'rack.temp.outlet-ur-low',
        'OUTLET_LR_UP': 'rack.temp.outlet-lr-up',
        'OUTLET_LR_LOW': 'rack.temp.outlet-lr-low',
        'PSU_INPUT_POWER': 'power.W',
    }

    def _cmd_got_poweron(obj, response, tm):
#        if not obj._sdr_is_valid(response) != 0:
#            return True
#        obj._l.debug("%s.%s %d %lu" % (obj._cmds[obj._cmdidx][0], response[7] & 1, tm))
        obj.on_data(obj._cmds[obj._cmdidx][0], response[7] & 1, tm)
        return True

    def _cmd_got_watt(obj, response, tm):
#        if not obj._sdr_is_valid(response) != 0:
#            return True
        val = unpack('<H', response[8:10])[0]
#        obj._l.debug("%s.%s %s %lu" % (obj._tag[0], obj._cmds[obj._cmdidx][0], val, tm))
        obj.on_data(obj._cmds[obj._cmdidx][0], val, tm)
        return True

    def _cmd_got_watt_aic(obj, response, tm):
        val = unpack('<H', response[7:9])[0]
#        obj._l.debug("%s.%s %s %lu" % (obj._tag[0], obj._cmds[obj._cmdidx][0], val, tm))
        obj.on_data(obj._cmds[obj._cmdidx][0], val, tm)
        return True

    def _cmd_got_watt2(obj, response, tm):
        if not obj._sdr_is_valid(response) != 0:
            return True
        val = 2 * response[7]
#        obj._l.debug("%s.%s %s %lu" % (obj._tag[0], obj._cmds[obj._cmdidx][0], val, tm))
        obj.on_data(obj._cmds[obj._cmdidx][0], val, tm)
        return True

    cmds = [
        ( 'power.on', 0x00, 0x01, (), _cmd_got_poweron ),
    ]

    ven = {
        (0, 0) : ( ( 'power.W', 0x04, 0x2d, (0x66,), _cmd_got_watt2 ), ),
        (42385, 1) : ( ( 'rack.power.fans-up', 0x36, 0xaa, (0x1,), _cmd_got_watt_aic ),
                   ( 'rack.power.fans-low', 0x36, 0xaa, (0x2,), _cmd_got_watt_aic ) ),
        (10876, 43707) : ( ( 'power.W', 0x30, 0x19, (), _cmd_got_watt ), ),
        (10876, 1811) : ( ( 'power.W', 0x30, 0xe2, (), _cmd_got_watt ), ),
    }

    fsm = async.FSMSock()
    udp = IpmiUdpAgent(None, sys.argv[1], -1, ('IPMI',), 3.0, sdrs=sdrs, cmds=cmds, vendors=ven)
    fsm.connect(udp)
    while fsm.run():
        fsm.tick()
