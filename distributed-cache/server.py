import sys
import zmq
import logging
import os

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger()

context = zmq.Context()

PEERS = os.getenv("PEERS", "").split(",")

class DistributedDict():
    def __init__(self):
        self.rep_socket = context.socket(zmq.REP)
        self.rep_socket.bind("tcp://*:5557")

        req_sockets = []
        for peer in PEERS:
            socket = context.socket(zmq.REQ)
            socket.connect(f'tcp://{peer}:5557')
            req_sockets.append(socket)

        self.req_sockets = req_sockets

        self.data = {}

    def get(self, key):
        try:
            value = self.data[key]
            data.rep_socket.send_pyobj(('OK', value))
        except KeyError:
            data.rep_socket.send_pyobj(('ERR', ''))

    def set(self, key, value):
        self.data[key] = value
        data.rep_socket.send_pyobj(('OK',))

    def fan_set(self, key, value):
        for socket in self.req_sockets:
            socket.send_pyobj(('localset', (key, value)))
            resp = socket.recv_pyobj()
            if resp[0] == 'OK':
                continue
            else:
                raise KeyError

    def run(self):
        while True:
            logger.info('Waiting for message')

            message = data.rep_socket.recv_pyobj()
            logger.info(f'Recieved message:{message}')
            if message[0] == 'get':
                self.get(message[1])
            if message[0] == 'set':
                self.set(*message[1])
                self.fan_set(*message[1])
            if message[0] == 'localset':
                self.set(*message[1])
            logger.info(self.data)

if __name__ == '__main__':
    data = DistributedDict()
    logger.info("Starting server")
    data.run()
