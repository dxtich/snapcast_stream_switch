#!/usr/bin/env python3
import json
import logging
import configparser
from telnetlib import Telnet
from time import sleep, time

log = logging.getLogger(__name__)
host = '127.0.0.1'
port = 1705
streams_priority = dict()
disabled_streams = list()


def initial_config():
    global host
    global port
    config = configparser.ConfigParser(allow_no_value=True)
    config.read('/etc/snapcontrol.conf')
    if 'snapcast' in config:
        if 'host' in config['snapcast']:
            host = config['snapcast']['host']
        if 'port' in config:
            port = config['snapcast']['port']
    if 'streams_priority' in config:
        for k, v in config['streams_priority'].items():
            streams_priority[k] = v
    if 'disabled_streams' in config:
        for item in config['disabled_streams']:
            disabled_streams.append(item)


def message_id():
    id = int(time())
    return id


def group_set_stream(group_id, stream_id):
    try:
        message = f'{{"id":{message_id()},"jsonrpc":"2.0","method":"Group.SetStream",' \
                  f'"params":{{"id":"{group_id}","stream_id":"{stream_id}"}}}}\r\n'
        log.debug(message)
        tn.write(message.encode())
        response = tn.read_until(b'\n')
        log.debug(response)
        return response
    except Exception as e:
        log.error(e)


def stream_on_update(rpc_data):
    try:
        id = message_id()
        message = f'{{"id":{id},"jsonrpc":"2.0","method":"Server.GetStatus"}}\r\n'
        log.debug(message)
        tn.write(message.encode())
        response = tn.read_until(b'\n')
        response_data = json.loads(response.decode("UTF-8"))
        if "id" in response_data:
            if response_data["id"] == id:
                groups = response_data['result']['server']['groups']
                streams = response_data['result']['server']['streams']
                playing_stream = False
                if rpc_data['params']['stream']['status'] == 'playing':
                    if str(rpc_data['params']['stream']['id']).lower() not in disabled_streams:
                        playing_stream = rpc_data['params']['stream']['id']
                else:
                    stream_priority = 0
                    for stream in streams:
                        stream_id_lower = str(stream['id']).lower()
                        if stream['status'] == 'playing':
                            if stream_id_lower in streams_priority:
                                priority = int(streams_priority[stream_id_lower])
                            else:
                                priority = 0
                            if priority >= stream_priority:
                                playing_stream = stream['id']
                                stream_priority = priority
                if playing_stream:
                    for group in groups:
                        group_id = group['id']
                        group_set_stream(group_id, playing_stream)
    except Exception as e:
        log.error(e)


SNAPCAST_METHODS = {
    # "Client.OnConnect": None,
    # "Client.OnDisconnect": None,
    # "Client.OnVolumeChanged": None,
    # "Client.OnLatencyChanged": None,
    # "Client.OnNameChanged": None,
    # "Group.OnMute": None,
    # "Group.OnStreamChanged": None,
    # "Group.OnNameChanged": None,
    "Stream.OnUpdate": stream_on_update,
    # "Server.OnUpdate": None,
}


def rpc_handler(rpc_call):
    rpc_data = json.loads(rpc_call.decode("UTF-8"))
    log.debug(rpc_data)
    if 'method' in rpc_data:
        method = rpc_data['method']
        if method in SNAPCAST_METHODS:
            SNAPCAST_METHODS[method](rpc_data)


if __name__ == "__main__":
    initial_config()
    while True:
        try:
            with Telnet(host, port) as tn:
                log.debug(f"connected to {host}:{port}")
                while True:
                    rpc_call = tn.read_until(b'\n')
                    rpc_handler(rpc_call)
        except EOFError as e:
            log.error(e)
        except Exception as e:
            log.error(e)
        sleep(5)
