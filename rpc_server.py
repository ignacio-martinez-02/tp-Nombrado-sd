# rpc_server.py
# Servidor RPC simple. Registra su servicio en el SIN e atiende peticiones JSON: {"type":"rpc","method":"name","params":[...]}
import socket, threading, argparse
from utils_protocol import send_json, recv_json
import json

SIN_HOST = '127.0.0.1'
SIN_PORT = 40000

def register_in_sin(service_name, host, port, metadata=None, ttl=0):
    import socket
    from utils_protocol import send_json, recv_json
    s = socket.socket()
    s.connect((SIN_HOST, SIN_PORT))
    send_json(s, {'cmd':'REGISTER','name':service_name,'type':'rpc','host':host,'port':port,'metadata':metadata or {}, 'ttl':ttl})
    resp = recv_json(s)
    s.close()
    return resp

class RPCServer:
    def __init__(self, host='127.0.0.1', port=0):
        self.host = host
        self.port = port
        self.funcs = {}

    def register_function(self, fn, name=None):
        self.funcs[name or fn.__name__] = fn

    def serve_forever(self):
        s = socket.socket()
        s.bind((self.host, self.port))
        s.listen(4)
        self.host, self.port = s.getsockname()
        print("RPC server listening on", self.host, self.port)
        # self-register in SIN:
        register_in_sin('calculator_service', self.host, self.port, metadata={'desc':'demo rpc calculator'}, ttl=300)
        while True:
            conn, _ = s.accept()
            threading.Thread(target=self.handle_conn, args=(conn,), daemon=True).start()

    def handle_conn(self, conn):
        try:
            req = recv_json(conn)
            if not req:
                return
            if req.get('type') != 'rpc':
                send_json(conn, {'status':'error','error':'not_rpc'})
                return
            method = req.get('method')
            params = req.get('params',[])
            fn = self.funcs.get(method)
            if not fn:
                send_json(conn, {'status':'error','error':'no_such_method'})
            else:
                try:
                    res = fn(*params)
                    send_json(conn, {'status':'ok','result':res})
                except Exception as e:
                    send_json(conn, {'status':'error','error':str(e)})
        finally:
            conn.close()

# demo functions
def add(a,b): return a+b
def mul(a,b): return a*b
def echo(x): return x

if __name__ == '__main__':
    srv = RPCServer()
    srv.register_function(add)
    srv.register_function(mul)
    srv.register_function(echo)
    srv.serve_forever()
