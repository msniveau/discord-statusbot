from lib.message.base_message import base_message
from lib.util.parameter import parameter

class del_server(base_message):
    validationRules = {
        1: '^[a-z0-9-_~!+\.]+$',
    }
    length = {
        'min': 1,
        'max': 1
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
        cfg.remove_option(self.message.server.id, message_parts[1])
        server_uid=message_parts[1] + ':' + self.message.server.id
        if server_uid in cfg.sections():
            cfg.remove_section(server_uid)
        with open(p.getConfig(), 'w+') as f:
            cfg.write(f)
        yield from client.send_message(self.message.channel, 'Deleted server %s' % (message_parts[1]))