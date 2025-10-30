# sin_name_service.py
# Servidor central del SIN. Protocolo simple JSON sobre TCP.
# Comandos: REGISTER, UNREGISTER, LOOKUP, LIST, QUERY

import socket
import threading
import time
import json
from utils_protocol import send_json, recv_json

HOST = '127.0.0.1'
PORT = 40000

class SIN:
    def __init__(self):
        # nombre -> entry
        # entry: {name, type, host, port, metadata, expires}
        self.store = {}
        self.lock = threading.Lock()

    def register(self, name, typ, host, port, metadata=None, ttl=0):
        if metadata is None:
            metadata = {}
        expires = None
        if ttl and ttl > 0:
            expires = time.time() + ttl
        entry = {'name': name, 'type': typ, 'host': host, 'port': port, 'metadata': metadata, 'expires': expires}
        with self.lock:
            self.store[name] = entry
        return {'status': 'ok', 'entry': entry}

    def unregister(self, name):
        with self.lock:
            if name in self.store:
                del self.store[name]
                return {'status': 'ok'}
            else:
                return {'status': 'error', 'error': 'not_found'}

    def lookup(self, name):
        now = time.time()
        with self.lock:
            entry = self.store.get(name)
            if not entry:
                # try prefix match (namespace)
                return {'status': 'error', 'error': 'not_found'}
            if entry['expires'] and entry['expires'] < now:
                del self.store[name]
                return {'status': 'error', 'error': 'expired'}
            return {'status': 'ok', 'entry': entry}

    def list_by_prefix(self, prefix):
        now = time.time()
        with self.lock:
            res = []
            for e in self.store.values():
                if e['expires'] and e['expires'] < now:
                    continue
                if e['name'].startswith(prefix):
                    res.append(e)
            return {'status': 'ok', 'entries': res}

    def query(self, typ=None, metadata_kv=None):
        now = time.time()
        metadata_kv = metadata_kv or {}
        with self.lock:
            res = []
            for e in self.store.values():
                if e['expires'] and e['expires'] < now:
                    continue
                if typ and e['type'] != typ:
                    continue
                ok = True
                for k,v in metadata_kv.items():
                    if e['metadata'].get(k) != v:
                        ok = False; break
                if ok:
                    res.append(e)
            return {'status': 'ok', 'entries': res}

sin = SIN()

def handle_client(conn, addr):
    try:
        while True:
            req = recv_json(conn)
            if req is None:
                break
            cmd = req.get('cmd')
            if cmd == 'REGISTER':
                r = sin.register(req['name'], req['type'], req['host'], req['port'], req.get('metadata'), req.get('ttl', 0))
                send_json(conn, r)
            elif cmd == 'UNREGISTER':
                r = sin.unregister(req['name'])
                send_json(conn, r)
            elif cmd == 'LOOKUP':
                r = sin.lookup(req['name'])
                send_json(conn, r)
            elif cmd == 'LIST':
                r = sin.list_by_prefix(req.get('prefix', ''))
                send_json(conn, r)
            elif cmd == 'QUERY':
                r = sin.query(req.get('type'), req.get('metadata'))
                send_json(conn, r)
            else:
                send_json(conn, {'status':'error','error':'unknown_cmd'})
    except Exception as e:
        print("client handler err", e)
    finally:
        conn.close()

def serve():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(8)
    print(f"SIN NameService listening on {HOST}:{PORT}")
    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn,addr), daemon=True).start()

if __name__ == '__main__':
    serve()
