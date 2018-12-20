from lib.message.base_message import base_message
from lib.util.parameter import parameter
from lib.util.queryli import queryli
from lib.util.error import DiscordError
from lib.util.queryli import format_message

class query_server(base_message):
    validationRules = {
        1: '^[a-z0-9-_~!+\.]+$',
        2: '^(all)$',
    }
    length = {
        'min': 0,
        'max': 2
    }

    def run(self, client):
        self.assert_length()
        self.assert_valid()
        message_parts = self.getMessageParts()
        tag='main'
        if len(message_parts) > 1:
            tag=message_parts[1]
        p = parameter.getInstance()
        cfg = p.__config__
        tags = []
        if tag == 'all':
            for section in cfg.sections():
                if section.endswith(':' + self.message.server.id):
                    tags.append(section.split(':')[0])
        else:
            tags.append(tag)
        message=''
        for tag in tags:
            keyindex=tag + ':' + self.message.server.id
            if not keyindex in cfg.sections():
                raise DiscordError('No server with the tag "%s" found.' % (tag))
            game = cfg.get(keyindex, 'game')
            ip = cfg.get(keyindex, 'ip')
            port = cfg.get(keyindex, 'port')
            gs = queryli(game, ip, int(port))
            printAll = False
            if len(self.getMessageParts()) > 2:
                printAll=True
            message+=format_message(self.message.server.id, gs, game, printAll, False)
        yield from client.send_message(self.message.channel, message)
