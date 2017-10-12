import zmq
from random import randrange
import sys


context = zmq.Context()

class Client:
    def __init__(self, server_name):
        self.req = context.socket(zmq.REQ)
        self.req.connect(f'tcp://{server_name}:5557')


    def get(self, key):
        self.req.send_pyobj(('get', key))
        resp = self.req.recv_pyobj()
        if resp[0] == 'OK':
            return resp[1]
        else:
            raise KeyError

    def set(self, key, value):
        self.req.send_pyobj(('set', (key, value)))
        resp = self.req.recv_pyobj()
        return resp[0]

if __name__ == '__main__':
    c1 = Client("server-1")
    c2 = Client("server-2")
