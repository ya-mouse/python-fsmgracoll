from fsmsock import proto

class AgentClient():
    def __init__(self, agent, type, tag):
        self._agent = agent
        self._type  = type
        if len(tag) != 2:
            self._tag = (tag[0], '')
        else:
            self._tag = (tag[0], '.'+tag[1])
