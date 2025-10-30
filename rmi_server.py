# rmi_server.py
# RMI-like: registra objetos con object_id y atiende invocaciones {"type":"rmi","object_id":"id","method":"m","params":[...]}
import socket, threading, uuid
from utils_protocol import send_json, recv_json

SIN_HOST = '127.0.0.1'
SIN_PORT = 40000

def register_in_sin(name, typ, host, port, metadata=None, ttl=0):
    s = socket.socket()
    s.connect((SIN_HOST, SIN_PORT))
    send_json(s, {'cmd':'REGISTER','name':name,'type':typ,'host':host,'port':port,'metadata':metadata or {}, 'ttl':ttl})
    r = recv_json(s)
    s.close()
    return r

class RMIRegistry:
    def __init__(self):
        self.objects = {}  # object_id -> instance

    def export(self, obj):
        oid = str(uuid.uuid4())
        self.objects[oid] = obj
        return oid

    def invoke(self, object_id, method, params):
        obj = self.objects.get(object_id)
        if obj is None:
            raise Exception("no such object")
        fn = getattr(obj, method, None)
        if not fn:
            raise Exception("no such method")
        return fn(*params)

registry = RMIRegistry()

class ExampleObj:
    def greet(self, name):
        return f"Hola {name} desde RMI object"
    def add(self,a,b): return a+b

def serve(host='127.0.0.1', port=0):
    s = socket.socket()
    s.bind((host,port))
    s.listen(4)
    host, port = s.getsockname()
    print("RMI server listening", host, port)
    # register endpoint in SIN so clients know where to ask for objects or for object lookups
    register_in_sin('rmi_host', 'rmi', host, port, metadata={'desc':'rmi endpoint'}, ttl=300)
    while True:
        conn, _ = s.accept()
        threading.Thread(target=handle_conn, args=(conn,), daemon=True).start()

def handle_conn(conn):
    try:
        req = recv_json(conn)
        if not req:
            return
        if req.get('type') != 'rmi':
            send_json(conn, {'status':'error','error':'not_rmi'})
            return
        if req.get('cmd') == 'EXPORT':
            # create object and return object id
            # in realistic case the object is created by server code and then exported
            obj = ExampleObj()
            oid = registry.export(obj)
            send_json(conn, {'status':'ok','object_id':oid})
            return
        # invocation
        object_id = req.get('object_id')
        method = req.get('method')
        params = req.get('params',[])
        try:
            res = registry.invoke(object_id, method, params)
            send_json(conn, {'status':'ok','result':res})
        except Exception as e:
            send_json(conn, {'status':'error','error':str(e)})
    finally:
        conn.close()

if __name__ == '__main__':
    serve()
