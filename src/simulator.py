import socket

from config.settings import Settings


class SimulatorException(Exception):
    pass


#FIXME: tmp
data = {
    1: (1.1, 1.2),
    2: (2.1, 2.2),
    3: (3.1, 3.2),
    4: (4.1, 4.2),
}


def process_command(cmd:str):
    if cmd.startswith(':MEASure') and cmd.endswith(':ALL?'):
        ch = int(cmd[cmd.find(':ALL?', len(':MEASure')) - 1])
        current, voltage = data[ch]
        return f'{current}\n{voltage}\n{0}'

    raise SimulatorException('Unknown command')


if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((Settings.DEVICE_HOST, Settings.DEVICE_PORT))
        s.listen()

        while True:
            try:
                conn, addr = s.accept()
                command = conn.recv(32)
                while command:
                    answer = process_command(command.decode())
                    conn.sendall(answer.encode())

                    command = conn.recv(32)
            finally:
                conn.close()
