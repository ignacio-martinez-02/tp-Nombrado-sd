# utils_protocol.py
# Pequeñas utilidades: enviar/recibir JSON por socket con newline como separador.

import json
import socket

def send_json(sock: socket.socket, obj):
    data = json.dumps(obj, separators=(',', ':')) + '\n'
    sock.sendall(data.encode('utf-8'))

def recv_json(sock: socket.socket):
    # lee hasta el primer newline
    buf = b''
    while True:
        ch = sock.recv(1)
        if not ch:
            if not buf:
                return None
            break
        if ch == b'\n':
            break
        buf += ch
    return json.loads(buf.decode('utf-8'))
