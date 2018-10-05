from lib.message.base_message import base_message
from lib.message.set_nickname import set_nickname
from lib.message.add_server import add_server
from lib.message.del_server import del_server
from lib.message.query_server import query_server
from lib.message.print_server import print_server
from lib.message.list_tags import list_tags
from lib.message.monitoring import monitoring
from lib.message.format_edit import format_edit

def getClass(type):
    if type == "!nick":
        return set_nickname
    if type == "!addserver":
        return add_server
    if type == "!delserver":
        return del_server
    if type == "!status":
        return query_server
    if type == "!servers":
        return list_tags
    if type == "!print":
        return print_server
    if type == "!monitoring":
        return monitoring
    if type == "!format":
        return format_edit
    return base_message

def handle( message):
    return getClass(message.content.split()[0])(message)