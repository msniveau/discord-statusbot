# -*- coding: utf-8 -*-

import os, sys, time, socket, argparse, asyncio, discord
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from lib.util import *
from lib.message import handle
from bin import __version__, __bundledir__
from lib.util.error import DiscordError
from lib.util.queryli import queryli, format_message


print("     _        _             _           _")
print(" ___| |_ __ _| |_ _   _ ___| |__   ___ | |_")
print("/ __| __/ _` | __| | | / __| '_ \ / _ \| __|")
print("\__ \ || (_| | |_| |_| \__ \ |_) | (_) | |_")
print("|___/\__\__,_|\__|\__,_|___/_.__/ \___/ \__|")
print(banner_message(22, "discord status bot v" + __version__))
param = parameter(argparse.ArgumentParser())
cfg = param.getInstance().__config__
print(banner_message(22, "config path: " + param.getConfig()))
if param.isVerbose() and not param.isDebugMode():
    print(banner_message(22, "running in verbose mode (debugging only!)"))
if param.isDebugMode():
    print(banner_message(22, "running in debug mode!"))
if param.getDSN():
    print(banner_message(22, "sentry logging enabled"))

client = discord.Client()

if param.isDebugMode():
    print('[info  ] Bundle dir is: %s' % (__bundledir__))

@asyncio.coroutine
def monitoring():
    yield from client.wait_until_ready()
    while True:
        for section in cfg.sections():
            if not ':' in section and section.isdigit():
                for tag in cfg.options(section):
                    if cfg.get(section, tag).isdigit():
                        if param.isDebugMode():
                            print('[info  ] Monitoring run for %s %s' % (section, tag))
                        yield from monitoring_run(section, tag)
        yield from asyncio.sleep(param.getMonitoringInterval())

@asyncio.coroutine
def monitoring_run(section, tag):
    sct = tag + ':' + section
    game=cfg.get(sct, 'game')
    gs = queryli(game, cfg.get(sct, 'ip'), int(cfg.get(sct, 'port')))
    if not cfg.has_option(sct, 'status'):
        cfg.set(sct, 'status', 'false')
    old = cfg.get(sct, 'status')
    changed=False
    if gs.status.error:
        if old == 'false':
            pass
        else:
            cfg.set(sct, 'status', 'false')
            changed=True
            with open(param.getConfig(), 'w+') as f:
                cfg.write(f)
    else:
        if old == 'false':
            cfg.set(sct, 'status', 'true')
            changed=True
            with open(param.getConfig(), 'w+') as f:
                cfg.write(f)
        else:
            pass
    if changed:
        if param.isDebugMode():
            print('[info  ] Monitoring status changed! (%s %s)' % (section, tag))
        try:
            yield from client.send_message(discord.Object(id=cfg.get(section, tag)), format_message(section, gs, game, False, True))
        except except (discord.client.Forbidden, discord.errors.NotFound):
            print('[error ] Monitoring wasn\'t able to send a message for (%s %s)' % (section, tag))
            yield from dict() 

@client.event
@asyncio.coroutine
def on_message(message):
    if (param.isVerbose()):
        server_id='direct'
        if message.server:
            server_id='guild '
        print("[%s][%s] %s:\t %s" % (server_id, message.channel.id, message.author.name, message.content))
    cmd = handle(message)
    try:
        yield from cmd.run(client)
    except DiscordError as e:
        if param.isDebugMode():
            print("[error ] " + str(e))
        yield from client.send_message(discord.Object(id=message.channel.id), "Error: " + str(e))

@client.event
@asyncio.coroutine
def on_ready():
    print("[info  ] Logging in as %s (%s)" % (client.user.name, client.user.id))

client.loop.create_task(monitoring())
client.run(param.getToken())
