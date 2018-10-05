from lib.util.error import DiscordError
import re

class base_message():
    validationRules = {}
    length = {
        'min': False,
        'max': False
    }

    def __init__(self,  message):
        self.message = message

    def getMessageParts(self):
        return self.message.content.split()

    def run(self, client):
        return dict()

    def assert_permission(self):
        if not self.message.author.server_permissions.manage_server:
            raise DiscordError('Missing permissions')

    def assert_length(self):
        message_length = len(self.getMessageParts())-1
        if self.length['min'] != False:
            if message_length < self.length['min']:
                raise DiscordError('Missing arguments!')
        if self.length['max'] != False:
            if message_length > self.length['max']:
                raise DiscordError('Too many arguments!')

    def assert_valid(self):
        message_parts = self.getMessageParts()
        for key in range(1, len(message_parts)):
            if key in self.validationRules:
                reg=re.compile(self.validationRules[key])
                if not bool(reg.match(message_parts[key])):
                    raise DiscordError('Invalid format for the ' + self.ndarg(key-1) + ' argument, only ' + self.validationRules[key] + ' is allowed!')

    def ndarg(self, pos):
        vals=[
            'first',
            'second',
            'third',
            'fourth',
            'fifth',
            'sixth'
        ]
        return vals[pos]