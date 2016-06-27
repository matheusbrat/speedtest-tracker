import dotenv
import logging

dotenv.load()
SERVER = dotenv.get('SERVER')
SERVER_TOKEN = dotenv.get('SERVER_TOKEN', '')
SPEEDTEST_SERVERS = dotenv.get('SPEEDTEST_SERVERS')
LOG = dotenv.get('LOG', logging.CRITICAL)

logging.basicConfig(format='%(levelname)s:%(message)s', level=LOG)