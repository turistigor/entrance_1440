import socket

from config.settings import Settings


class SimulatorException(Exception):
    pass


data = {
    1: [1.1, 1.2, True],
    2: [2.1, 2.2, True],
    3: [3.1, 3.2, True],
    4: [4.1, 4.2, True],
}


def process_command(cmd:str):
    if cmd.startswith(':MEASure') and cmd.endswith(':ALL?'):
        ch = int(cmd[cmd.find(':ALL?', len(':MEASure')) - 1])
        current, voltage, __ = data[ch] if data[ch][2] else (0, 0, False)
        return f'{current}\n{voltage}\n{0}'
    elif cmd.startswith(':SOURce'):
        parts = cmd.split(':')[1:]
        ch = int(parts[0][-1])
        val_type, val = parts[1].split()
        if val_type == 'CURRent':
            data[ch][0] = float(val)
        else:
            data[ch][1] = float(val)
        return
    elif cmd.startswith(':OUTPut'):
        ch = int(cmd[len(':OUTPut')])
        data[ch][2] = cmd.endswith('ON')
        return

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
                    if answer:
                        conn.sendall(answer.encode())

                    command = conn.recv(32)
            finally:
                conn.close()
