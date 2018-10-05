from lib.message.base_message import base_message
from lib.util.parameter import parameter
from lib.util.error import DiscordError

class print_server(base_message):
    validationRules = {
        1: '^[a-z0-9-_~!+\.]+$',
    }
    length = {
        'min': 1,
        'max': 1
    }

    def run(self, client):
        self.assert_length()
        self.assert_valid()
        message_parts = self.getMessageParts()
        tag=message_parts[1]
        p = parameter.getInstance()
        cfg = p.__config__
        keyindex=tag + ':' + self.message.server.id
        if not keyindex in cfg.sections():
            raise DiscordError('No server with the tag "%s" found.' % (tag))
        game = cfg.get(keyindex, 'game')
        ip = cfg.get(keyindex, 'ip')
        port = cfg.get(keyindex, 'port')
        yield from client.send_message(self.message.channel, '```ini\nip = %s\nport = %s\ngame = %s```' % (ip, port, game))