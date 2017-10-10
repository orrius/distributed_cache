import zmq
from random import randrange
import sys


context = zmq.Context()

class Client:
    def __init__(self):
        self.pub = context.socket(zmq.PUB)
        self.pub.bind("tcp://*:5556")

        self.req = context.socket(zmq.REQ)
        self.req.bind("tcp://*:5557")



    def get(self, key):
        self.req.send_string(key)
        return self.req.recv_string()

    def set(self, key, value):
       self.pub.send_pyobj((key, value))

