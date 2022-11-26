from multiprocessing import Process


def dcps_server():
    print('Server proc works')


def telemetry_client():
    print('Telemetry client works')


def http_server():
    print('Http server works')


if __name__ == '__main__':
    dcps_server_proc = Process(name='dcps_server', target=dcps_server)
    dcps_server_proc.start()
    dcps_server_proc.join()

    telemetry_client_proc = Process(name='telemetry_client', target=telemetry_client)
    telemetry_client_proc.start()
    telemetry_client_proc.join()

    http_server_proc = Process(name='http_server', target=http_server)
    http_server_proc.start()
    http_server_proc.join()
