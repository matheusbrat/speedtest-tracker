from subprocess import Popen, PIPE
from speedtest_parser import SpeedTestParser
import requests
from settings import *


def build_json(my_server_name, my_server_domain, my_ip, server_name, server_location, server_distance,
               server_distance_unit, server_ping, server_ping_unit, download_speed, download_unit, upload_speed,
               upload_unit, share_url):
    return {
        "my_server_name": my_server_name,
        "my_server_domain": my_server_domain,
        "my_ip": my_ip,
        "server_name": server_name,
        "server_location": server_location,
        "server_distance": server_distance,
        "server_distance_unit": server_distance_unit,
        "server_ping": server_ping,
        "server_ping_unit": server_ping_unit,
        "download_speed": download_speed,
        "download_unit": download_unit,
        "upload_speed": upload_speed,
        "upload_unit": upload_unit,
        "share_url": share_url
    }


def run_speedtest(server):
    logging.debug("Running speedtest with server %s" % server)
    command = ["speedtest-cli", "--share"]
    if server:
        command.append('--server')
        command.append(server)
    logging.debug("Command: %s" % command)
    pipe = Popen(command, stdout=PIPE)
    text = pipe.communicate()[0].decode()
    logging.debug("Output: \n %s" % text)
    return text


def send_test_data(json):
    logging.debug("Posting to %s with data %s" % (SERVER, json))

    headers = {'Authorization': 'Token ' + SERVER_TOKEN}
    post = requests.post(SERVER, data=json, headers=headers)


def speedtest():
    if SPEEDTEST_SERVERS:
        servers = SPEEDTEST_SERVERS
    else:
        servers = [None]
    logging.debug("Running speedtest with servers %s" % str(servers))
    for server in servers:
        text = run_speedtest(server)

        p = SpeedTestParser(text)
        json = build_json(p.my_server_name, p.my_server_domain, p.my_ip, p.server_name, p.server_location,
                          p.server_distance, p.server_distance_unit, p.server_ping, p.server_ping_unit, p.download_speed,
                          p.download_unit, p.upload_speed, p.upload_unit, p.share_url)
        send_test_data(json)


speedtest()
