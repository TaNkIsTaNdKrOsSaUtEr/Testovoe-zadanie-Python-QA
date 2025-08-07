import socket
import os
import sys
from typing import Tuple


def get_file_info(file_path: str) -> Tuple[str, int]:
    """Получить имя файла и его размер"""
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    return file_name, file_size


def send_file(conn: socket.socket, file_path: str) -> None:
    """Отправка файла клиенту"""
    file_name, file_size = get_file_info(file_path)

    # Отправляем информацию о файле
    conn.send(f"{file_name},{file_size}".encode())
    ack = conn.recv(1024)  # Ждем подтверждения

    # Отправляем содержимое файла
    with open(file_path, "rb") as f:
        bytes_sent = 0
        while bytes_sent < file_size:
            data = f.read(1024)
            if not data:
                break
            conn.sendall(data)
            bytes_sent += len(data)
    print("finished sending")


def main() -> None:
    """Основная функция сервера"""
    if len(sys.argv) != 2:
        print("Usage: python server.py <file>")
        sys.exit(1)

    file_path = sys.argv[1]
    print(f"serving {os.path.abspath(file_path)}")

    # Настройка сокета
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 8080))
    server_socket.listen(1)

    try:
        conn, addr = server_socket.accept()
        print(f"request from {addr[0]}:{addr[1]}")
        print("sending...")
        send_file(conn, file_path)
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()

