import sys
import zmq

context = zmq.Context()

class DistributedDict():
    def __init__(self):
        self.rep_socket = context.socket(zmq.REP)
        self.rep_socket.connect("tcp://localhost:5557")

        self.sub_socket = context.socket(zmq.SUB)
        self.sub_socket.connect("tcp://localhost:5556")
        self.sub_socket.setsockopt(zmq.SUBSCRIBE, b"")

        self.poller = zmq.Poller()
        self.poller.register(self.rep_socket, zmq.POLLIN)
        self.poller.register(self.sub_socket, zmq.POLLIN)


        self.data = {}

    def get(self, key):
        return self.data.get(key, '')

    def set(self, message):
        key, value = message
        self.data[key] = value


if __name__ == '__main__':
    data = DistributedDict()

    while True:
        try:
            socks = dict(data.poller.poll())
        except KeyboardInterrupt:
            break

        print("reading data")
        if data.rep_socket in socks:
            message = data.get(data.rep_socket.recv_string())
            data.rep_socket.send_string(message)

        if data.sub_socket in socks:
            data.set(data.sub_socket.recv_pyobj())

        print(data.data)
