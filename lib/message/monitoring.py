from lib.message.base_message import base_message
from lib.util.error import DiscordError
from lib.util.parameter import parameter

class monitoring(base_message):
    validationRules = {
        1: '^[a-z0-9-_~!+\.]+$',
        2: '^(?i)(true|false)$',
    }
    length = {
        'min': 1,
        'max': 2
    }

    def run(self, client):
        self.assert_permission()
        self.assert_length()
        self.assert_valid()
        message_parts = self.getMessageParts()
        p = parameter.getInstance()
        cfg = p.__config__
        if not self.message.server.id in cfg.sections():
            cfg.add_section(self.message.server.id)
        if not cfg.has_option(self.message.server.id, message_parts[1]):
            raise DiscordError('No server configured with this tag')
        if len(message_parts) > 2:
            option=message_parts[2]
            if message_parts[2] == 'true':
                option=self.message.channel.id
            cfg.set(self.message.server.id, message_parts[1], option)
            with open(p.getConfig(), 'w+') as f:
                cfg.write(f)
            yield from client.send_message(self.message.channel, 'Monitoring was set to %s' % (message_parts[2]))
        else:
            yield from client.send_message(self.message.channel, 'Monitoring is currenty %s' % (cfg.get(self.message.server.id, message_parts[1])))