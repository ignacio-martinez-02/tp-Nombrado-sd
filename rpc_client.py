# rpc_client.py
# Consulta SIN para encontrar un servicio RPC y la invoca.
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

def call_rpc(service_name, method, params):
    r = lookup(service_name)
    if r.get('status') != 'ok':
        raise Exception("lookup failed: "+str(r))
    entry = r['entry']
    host, port = entry['host'], entry['port']
    s = socket.socket()
    s.connect((host, port))
    send_json(s, {'type':'rpc','method':method,'params':params})
    resp = recv_json(s)
    s.close()
    return resp

if __name__ == '__main__':
    print(call_rpc('calculator_service','add',[3,5]))
    print(call_rpc('calculator_service','mul',[4,7]))
    print(call_rpc('calculator_service','echo',['hola desde cliente']))
