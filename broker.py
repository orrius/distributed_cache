import zmq

def main():
    context = zmq.Context()

    frontend = context.socket(zmq.ROUTER)
    frontend.bind("tcp://*:5559")

    backend = context.socket(zmq.DEALER)
    backend.bind("txp://*:5560")

    zmp.proxy(frontend, backend)

    frontend.close()
    backend.close()
    context.term()

if __name__ == '__main__':
    main()
