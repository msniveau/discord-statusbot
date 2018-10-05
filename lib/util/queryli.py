import json, requests, re
from lib.util.parameter import parameter

class queryli:
    def __init__(self, game, ip, port):
        self._game = game
        self.ip = ip
        self.port = port
        self.refresh()


    def refresh(self):
        response = requests.get('https://query.li/api/%s/%s/%d' % (self._game, self.ip, self.port), timeout=5)
        self.data = json.loads(response.text)
        return self

    @property
    def game(self):
        return QueryResult(self.data['game'])

    @property
    def whois(self):
        return QueryResult(self.data['whois'])

    @property
    def status(self):
        return QueryResult(self.data['status'])

    @property
    def cached(self):
        return self.data['cached']

    def toJson(self):
        return json.dumps(self.data)
  
class QueryResult:
    def __init__(self, data):
        self.data = data

    def __getattr__(self, name):
        if name in self.data:
            if type(self.data[name]) == dict:
                return QueryResult(self.data[name])
            return self.data[name]

    @property
    def __dict__(self):
        d = self.data
        for name in d:
            if type(d[name]) == dict:
                d[name] = QueryResult(self.data[name])
        return d

    def toJson(self):
        return json.dumps(self.data)


def format_message(server, gs, tag, printAll=False, monitoring=False):
    p = parameter.getInstance()
    cfg = p.__config__
    section_name = server + ':format'
    prefix='status'
    if monitoring:
        prefix='monitoring'
    if not section_name in cfg.sections():
        section_name='default:format'
    type='online'
    if gs.status.error:
        type='offline'
    key_name = '%s_%s_%s' % (prefix, type, tag)
    if not key_name in cfg.options(section_name):
        key_name='%s_%s' % (prefix, type)
    message = cfg.get(section_name, key_name)
    for key, value in gs.game.info.__dict__.items():
        if key == 'server_name':
            value = re.sub(r'<.+?>', '', value)
        if printAll:
            message+='%s = %s\n' % (key, value)
        message = message.replace('{' + key + '}', str(value))

    for key, value in gs.whois.addr.__dict__.items():
        if printAll:
            message+='%s = %s\n' % (key, value)
        message = message.replace('{' + key + '}', str(value))

    if printAll:
        message+='%s = %s\n' % ('organization', gs.whois.organization)
        message+='%s = %s\n' % ('tag', tag)
        message+='%s = %s\n' % ('break', 'linebreak')
    message = message.replace('{organization}', gs.whois.organization)
    message = message.replace('{tag}', tag)
    message = message.replace('{break}', '\r\n')
    return message