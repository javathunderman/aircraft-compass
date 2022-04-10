import math
from numpy import NaN
import zmq.green as zmq
import pmt
from flask import Flask, request
from flask_socketio import SocketIO
from threading import Thread
import geopy.distance

app = Flask(__name__, static_url_path="", static_folder="public")
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app)
global_pos = {'a0d6a8': {'latitude': 39.001952364038424, 'longitude': -76.92266280682385}} # Must fix
users = {}

def zmq_thread():
    ZMQ_ADDRESS = "127.0.0.1"
    ZMQ_PORT = 5001
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
        
        
        global_pos[plane['icao']] = {'latitude': plane['latitude'], 'longitude': plane['longitude']}
        
        for flight in global_pos.keys():
            for user in users.keys():
                newDist = geopy.distance.geodesic((global_pos[flight]['latitude'], global_pos[flight]['longitude']), (users[user]['latitude'], users[user]['longitude'])).km
                if (newDist < users[user]['distanceToFlight']):
                    users[user]['nearestFlight'] = global_pos[flight]
                    users[user]['distanceToFlight'] = newDist

        for user in users:
            nearestFlightToUser = users[user]['nearestFlight']
            print(nearestFlightToUser)
            bearing = 33 # Must fix
            print(bearing)
            socketio.emit("updateFlight", {'bearing': bearing})
        
        print(global_pos)       

@app.route("/")
def index():
    return app.send_static_file("index.html")


@socketio.on("connect")
def connect():
    users[request.sid] = {'latitude': 0, 'longitude': 0, "nearestFlight": "", "distanceToFlight": 50000}
    print("Client connected", request.sid)
    print(users)


@socketio.on("disconnect")
def disconnect():
    users.pop(request.sid)
    print("Client disconnected", request.sid)

@socketio.event
def updateGeolocation(data):
    users[request.sid]['latitude'] = data['latitude']
    users[request.sid]['longitude'] = data['longitude']
    print(data)
    print(users)



if __name__ == "__main__":
    thread = Thread(target=zmq_thread)
    thread.daemon = True
    thread.start()

    socketio.run(app, host="10.0.0.2", port=5000, debug=True, use_reloader=False)

