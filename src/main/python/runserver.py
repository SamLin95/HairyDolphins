from webapp import socketio
from webapp import app

#Run the sever on localhost using socket's method. The port is 8080 and debug
#mode is on.
if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=8080, debug=True)
