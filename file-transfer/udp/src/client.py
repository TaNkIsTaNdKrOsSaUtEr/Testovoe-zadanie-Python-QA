import socket
import os
import sys
from typing import Tuple


BUFFER_SIZE = 1024
SERVER_ADDR = ("localhost", 8081)


def parse_file_info(file_info: str) -> Tuple[str, int]:
    """Разобрать информацию о файле."""
    file_name, file_size_str = file_info.split(",")
    return file_name, int(file_size_str)


def save_file(sock: socket.socket, file_name: str, file_size: int) -> None:
    """Сохранение полученного файла."""
    save_path = os.path.join(os.getcwd(), file_name)
    expected_seq = 0

    with open(save_path, "wb") as f:
        bytes_received = 0
        while bytes_received < file_size:
            packet, _ = sock.recvfrom(BUFFER_SIZE)
            seq_num = int.from_bytes(packet[:4], "big")
            data = packet[4:]

            # Отправка ACK
            sock.sendto(seq_num.to_bytes(4, "big"), SERVER_ADDR)

            if seq_num == expected_seq:
                f.write(data)
                bytes_received += len(data)
                expected_seq += 1

    print(f"downloaded as {save_path}")


def main() -> None:
    """Основная функция клиента."""
    if len(sys.argv) != 2:
        print("Usage: python client.py <output_file>")
        sys.exit(1)

    output_file = sys.argv[1]
    print(f"requesting from {SERVER_ADDR[0]}:{SERVER_ADDR[1]}")
    print("downloading...")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        sock.sendto(b"REQUEST", SERVER_ADDR)

        # Получение метаданных
        file_info, _ = sock.recvfrom(BUFFER_SIZE)
        file_name, file_size = parse_file_info(file_info.decode())

        save_file(sock, output_file, file_size)
    finally:
        sock.close()


if __name__ == "__main__":
    main()
