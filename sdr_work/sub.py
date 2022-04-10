import zmq.green as zmq
import pmt

def zmq_thread(ZMQ_ADDRESS, ZMQ_PORT):
    
    # Establish ZMQ context and socket
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.setsockopt(zmq.SUBSCRIBE, b"")
    socket.connect("tcp://{:s}:{:d}".format(ZMQ_ADDRESS, ZMQ_PORT))

    while True:
        # Receive decoded ADS-B message from the decoder over ZMQ
        pdu_bin = socket.recv()
        pdu = pmt.deserialize_str(pdu_bin)
        plane = pmt.to_python(pmt.car(pdu))

        print(plane)

def main():
    zmq_thread("127.0.0.1", 5001)
main()