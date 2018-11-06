from lib.message.base_message import base_message

class set_nickname(base_message):
    validationRules = {
        1: '^[a-zA-Z0-9-_~!+\.]+$'
    }
    length = {
        'min': 1,
        'max': 1
    }

    def run(self, client):
        self.assert_permission()
        self.assert_length()
        self.assert_valid()
        current_nick=self.message.server.me.display_name
        yield from client.change_nickname(self.message.server.me, self.getMessageParts()[1])
        yield from client.send_message(self.message.channel, 'Nickname was changed from %s to %s' % (current_nick, self.getMessageParts()[1]))
