from fsmsock import proto
from fsmssh2.proto import SSHClient

from agent import AgentClient

class SSHAgent(SSHClient, AgentClient):
    def __init__(self, agent, host, type, tag, interval, user, passwd, cmds):
        SSHClient.__init__(self, host, interval, user, passwd, cmds)
        AgentClient.__init__(self, agent, type, tag)

    def _value(self, data, tm):
        for s in str(data, 'utf-8').split('\r\n'):
            if s == '':
                continue
            try:
                k,v = s.split(' ', 2)
                if k == '':
                    continue
                #self._agent.send(self._tag[0]+'.'+k+self._tag[1], float(v), tm)
                print(self._tag[0]+'.'+k+self._tag[1], float(v), tm)
            except Exception:
                continue

    def stop(self):
        # Run forever
        pass

if __name__ == '__main__':
    import sys
    from fsmsock import async
    fsm = async.FSMSock()
    ssh = SSHAgent(None, sys.argv[1], -1, ('IPMI',), 3.0, 'ADMIN', 'ADMIN', (sys.argv[2],))
    fsm.connect(ssh)
    while fsm.run():
        fsm.tick()
