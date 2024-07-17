from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_byte/<direction>')
def send_byte(direction):
    bytes_map = {
        'up': b'\x01\x00\x00\x00',
        'down': b'\x00\x01\x00\x00',
        'left': b'\x00\x00\x01\x00',
        'right': b'\x00\x00\x00\x01'
    }
    
    if direction in bytes_map:
        byte_to_send = bytes_map[direction]
        print(f'Sent byte: {byte_to_send}')
        socketio.emit('message', f'Sent byte for {direction}')
        return f'Sent byte for {direction}'
    else:
        return 'Invalid direction', 400

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, debug=True)
