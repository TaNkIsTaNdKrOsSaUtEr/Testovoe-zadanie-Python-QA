import socket
import os
import sys
from typing import Tuple


BUFFER_SIZE = 1024
TIMEOUT = 0.1


def get_file_info(file_path: str) -> Tuple[str, int]:
    """Получить имя файла и его размер"""
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    return file_name, file_size


def send_file(
    sock: socket.socket,
    client_addr: Tuple[str, int],
    file_path: str
) -> None:
    """Отправка файла через UDP"""
    file_name, file_size = get_file_info(file_path)

    # Отправляем метаданные
    sock.sendto(f"{file_name},{file_size}".encode(), client_addr)

    # Отправка файла частями
    with open(file_path, "rb") as f:
        seq_num = 0
        while True:
            data = f.read(BUFFER_SIZE - 4)
            if not data:
                break

            # Формируем пакет: [номер пакета (4 байта) + данные]
            packet = seq_num.to_bytes(4, "big") + data
            sock.sendto(packet, client_addr)

            # Ожидание ACK
            ack_received = False
            while not ack_received:
                try:
                    sock.settimeout(TIMEOUT)
                    ack_packet, addr = sock.recvfrom(4)
                    if int.from_bytes(ack_packet, "big") == seq_num:
                        ack_received = True
                except socket.timeout:
                    sock.sendto(packet, client_addr)

            seq_num += 1

    print("finished sending")


def main() -> None:
    """Основная функция сервера"""
    if len(sys.argv) != 2:
        print("Usage: python server.py <file>")
        sys.exit(1)

    file_path = sys.argv[1]
    print(f"serving {os.path.abspath(file_path)}")

    # Настройка UDP сокета
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("localhost", 8081))

    try:
        # Ожидание запроса
        _, client_addr = sock.recvfrom(1)
        print(f"request from {client_addr[0]}:{client_addr[1]}")
        print("sending...")
        send_file(sock, client_addr, file_path)
    finally:
        sock.close()


if __name__ == "__main__":
    main()

