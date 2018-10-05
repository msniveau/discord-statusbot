from lib.message.base_message import base_message
from lib.util.error import DiscordError
from lib.util.parameter import parameter
import re

class add_server(base_message):
    validationRules = {
        1: '^[a-z0-9-_~!+\.]+$',
        2: '^[a-z0-9]+$',
        3: '^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$',
        4: '^[0-9]+$',
    }
    length = {
        'min': 4,
        'max': 4
    }

    def getMessageParts(self):
        ip=re.compile('^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
        message_parts = self.message.content.split()
        if len(message_parts) not in [4,5]:
            return message_parts
        if bool(ip.match(message_parts[2])):
            l = list()
            l.append(message_parts[0])
            l.append(message_parts[1])
            l.append('steam')
            l.append(message_parts[2])
            l.append(message_parts[3])
            message_parts = l
        return message_parts


    def run(self, client):
        self.assert_permission()
        self.assert_length()
        self.assert_valid()
        message_parts = self.getMessageParts()
        p = parameter.getInstance()
        cfg = p.__config__
        if not self.message.server.id in cfg.sections():
            cfg.add_section(self.message.server.id)
        cfg.set(self.message.server.id, message_parts[1], 'false')
        server_uid=message_parts[1] + ':' + self.message.server.id
        if server_uid in cfg.sections():
            raise DiscordError("Server with the tag \"%s\" is already configured, delete server first: !delserver <tag>" % (message_parts[1]))
        else:
            cfg.add_section(server_uid)
        cfg.set(server_uid, 'game', message_parts[2])
        cfg.set(server_uid, 'ip', message_parts[3])
        cfg.set(server_uid, 'port', message_parts[4])
        with open(p.getConfig(), 'w+') as f:
            cfg.write(f)
        yield from client.send_message(self.message.channel, 'Added %s server %s with address %s:%s' % (message_parts[2], message_parts[1], message_parts[3], message_parts[4]))
