from lib.message.base_message import base_message
from lib.util.error import DiscordError
from lib.util.parameter import parameter

class format_edit(base_message):
    validationRules = {
        1: '^(?i)(monitoring|status)$',
        2: '^(?i)(offline|online)$',
        3: '^[a-z0-9]+$',
    }
    length = {
        'min': 4,
        'max': False
    }


    def run(self, client):
        self.assert_permission()
        self.assert_length()
        self.assert_valid()
        message_parts = self.getMessageParts()
        p = parameter.getInstance()
        cfg = p.__config__
        section_name = self.message.server.id + ':format'
        if not section_name in cfg.sections():
            cfg.add_section(section_name)
            for default in cfg.options('default:format'):
                cfg.set(section_name, default, cfg.get('default:format', default))
                with open(p.getConfig(), 'w+') as f:
                    cfg.write(f)
        if message_parts[3] != 'general':
            keyname=message_parts[1] + '_' + message_parts[2] + '_' + message_parts[3]
        else:
            keyname=message_parts[1] + '_' + message_parts[2]
        cfg.set(section_name, keyname, ' '.join(message_parts[4:]))
        with open(p.getConfig(), 'w+') as f:
            cfg.write(f)
        yield from client.send_message(self.message.channel, 'Formatting for ' + message_parts[1] + ':' + message_parts[2] + ' changed to "' + ' '.join(message_parts[4:]) + '"')
