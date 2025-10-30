# rmi_client.py
# Cliente RMI: localiza endpoint via SIN y solicita EXPORT o INVOKE
import socket
from utils_protocol import send_json, recv_json

SIN_HOST = '127.0.0.1'
SIN_PORT = 40000

def lookup(name):
    s = socket.socket()
    s.connect((SIN_HOST, SIN_PORT))
    send_json(s, {'cmd':'LOOKUP','name':name})
    r = recv_json(s)
    s.close()
    return r

def export_remote_object():
    r = lookup('rmi_host')
    entry = r['entry']
    s = socket.socket()
    s.connect((entry['host'], entry['port']))
    send_json(s, {'type':'rmi','cmd':'EXPORT'})
    resp = recv_json(s)
    s.close()
    return resp

def invoke(object_id, method, params):
    r = lookup('rmi_host')
    entry = r['entry']
    s = socket.socket()
    s.connect((entry['host'], entry['port']))
    send_json(s, {'type':'rmi','object_id':object_id,'method':method,'params':params})
    resp = recv_json(s)
    s.close()
    return resp

if __name__ == '__main__':
    ex = export_remote_object()
    oid = ex['object_id']
    print("object id:", oid)
    print(invoke(oid, 'greet', ['Nacho']))
    print(invoke(oid, 'add', [10,20]))
