import socket
import os
import sys
from typing import Tuple


def parse_file_info(file_info: str) -> Tuple[str, int]:
    """Разобрать информацию о файле."""
    file_name, file_size_str = file_info.split(",")
    return file_name, int(file_size_str)


def save_file(conn: socket.socket, file_name: str, file_size: int) -> None:
    """Сохранение полученного файла."""
    save_path = os.path.join(os.getcwd(), file_name)
    with open(save_path, "wb") as f:
        bytes_received = 0
        while bytes_received < file_size:
            chunk = conn.recv(min(1024, file_size - bytes_received))
            if not chunk:
                break
            f.write(chunk)
            bytes_received += len(chunk)
    print(f"downloaded as {save_path}")


def main() -> None:
    """Основная функция клиента."""
    if len(sys.argv) != 2:
        print("Usage: python client.py <output_file>")
        sys.exit(1)

    output_file = sys.argv[1]
    print("requesting from localhost:8080")
    print("downloading...")

    # Подключение к серверу
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("localhost", 8080))

    try:
        # Получаем информацию о файле
        file_info = client_socket.recv(1024).decode()
        client_socket.send(b"ACK")  # Подтверждение

        file_name, file_size = parse_file_info(file_info)
        save_file(client_socket, output_file, file_size)
    finally:
        client_socket.close()


if __name__ == "__main__":
    main()
