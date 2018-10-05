from lib.message.base_message import base_message
from lib.util.error import DiscordError
from lib.util.parameter import parameter

class list_tags(base_message):
    length = {
        'min': 0,
        'max': 0
    }


    def run(self, client):
        self.assert_length()
        p = parameter.getInstance()
        cfg = p.__config__
        if not self.message.server.id in cfg.sections():
            cfg.add_section(self.message.server.id)
        tags = []
        for section in cfg.sections():
            if section.endswith(':' + self.message.server.id):
                tags.append(section.split(':')[0])
        if len(tags) == 0:
            raise DiscordError('No servers configured!')
        yield from client.send_message(self.message.channel, 'Currently the following tags are configured:' + self.format_list(tags))

    def format_list(self,parts):
        return '\n\u2022 ' + ('\n\u2022 ').join(parts)