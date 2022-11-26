from multiprocessing import Process
from multiprocessing.sharedctypes import Value
import socket
from ctypes import Structure, c_char_p


class DeviceData(Structure):
    _fields_ = [('dcps', c_char_p), ('telemetry', c_char_p), ('http_server', c_char_p)]

    def __init__(self, dcps, telemetry, http_server, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dcps = dcps
        self.telemetry = telemetry
        self.http_server = http_server

    def __str__(self):
        return f'{self.dcps}, {self.telemetry}, {self.http_server}'


def dcps_server(shared_val):
    print('Server proc works')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('127.0.0.1', 8000))
        s.listen()
        try:
            i = 0
            while i < 2:
                conn, addr = s.accept()
                print(f'Server proc accepted conn from {addr}')

                data = conn.recv(1024)
                print(f'Server received from {addr} data: "{data}"')

                answer = f'Server answer for {addr}'
                conn.sendall(answer.encode('utf-8'))
                i += 1
        finally:
            shared_val.dcps = b'dcps'
            conn.close()
            print(f'Server common data: {shared_val}')
            print(f'Server closed conn with {addr}')    

def telemetry_client(shared_val):
    print('Telemetry client works')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.connect(('127.0.0.1', 8000))
        s.sendall(b'Query from telemetry')
        data = s.recv(1024)
        shared_val.telemetry = b'Telemetry'
        print(f'Telemetry client received from server: "{data}"')
        print(f'Telemetry common data: {shared_val}')

def http_server(shared_val):
    print('Http server works')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.connect(('127.0.0.1', 8000))
        s.sendall(b'Query from http server')
        data = s.recv(1024)
        shared_val.http_server = b'HTTP server'
        print(f'Http server received from server: "{data}"')
        print(f'HTTP server common data: {shared_val}')


if __name__ == '__main__':
    val = Value(DeviceData, *(b'init', b'init', b'init'), lock=True)

    dcps_server_proc = Process(name='dcps_server', target=dcps_server, args=(val,))
    dcps_server_proc.start()

    telemetry_client_proc = Process(name='telemetry_client', target=telemetry_client, args=(val,))
    telemetry_client_proc.start()

    http_server_proc = Process(name='http_server', target=http_server, args=(val,))
    http_server_proc.start()
    
    http_server_proc.join()
    telemetry_client_proc.join()
    dcps_server_proc.join()

    print(f'Result common data: {val}')
