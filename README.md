# Приложение для передачи файлов через TCP и UDP

Этот репозиторий содержит две реализации программ для передачи файлов:
- передача через TCP
- передача через UDP с собственной реализацией контроля доставки

## Структура репозитория

file-transfer/
├── .gitignore
├── README.md
├── tcp/
│   ├── src/
│   │   ├── server.py
│   │   └── client.py
│   └── test/
│       └── test.sh
└── udp/
    ├── src/
    │   ├── server.py
    │   └── client.py
    └── test/
        └── test.sh


## Требования
- Python 3.6+
- Bash (для запуска тестов)

## Установка
```bash
git clone https://github.com/<ваш-username>/file-transfer.git
cd file-transfer

TCP реализация
Сервер
bash

cd tcp/src
python server.py <путь-к-файлу>

Пример вывода:
text

serving /path/to/filetoserve
request from 127.0.0.1:8081
sending...
finished sending to 127.0.0.1:8081

Клиент
bash

cd tcp/src
python client.py <имя-выходного-файла>

Пример вывода:
text

requesting from 127.0.0.1:8080
downloading...
downloaded as /path/to/newfile

Тестирование TCP
bash

cd tcp/test
chmod +x test.sh
./test.sh

Пример вывода:
text

serving /path/to/testfile.bin
requesting from localhost:8080
downloading...
request from 127.0.0.1:37998
sending...
finished sending
downloaded as /path/to/received.bin
TCP Test passed: Files match

UDP реализация
Сервер
bash

cd udp/src
python server.py <путь-к-файлу>

Пример вывода:
text

serving /path/to/filetoserve
request from 127.0.0.1:58618
sending...
finished sending to 127.0.0.1:58618

Клиент
bash

cd udp/src
python client.py <имя-выходного-файла>

Пример вывода:
text

requesting from 127.0.0.1:8081
downloading...
downloaded as /path/to/newfile

Тестирование UDP
bash

cd udp/test
chmod +x test.sh
./test.sh

Пример вывода:
text

serving /path/to/testfile.bin
requesting from localhost:8081
downloading...
request from 127.0.0.1:58618
sending...
finished sending
downloaded as /path/to/received.bin
UDP Test passed: Files match

Особенности реализации
TCP

    Надежная передача данных

    Простой протокол:

        Сервер отправляет метаданные (имя файла, размер)

        Клиент подтверждает получение метаданных

        Сервер отправляет содержимое файла

    Поддерживает файлы любого размера

UDP

    Собственная реализация надежности поверх UDP

    Протокол "стоп-и-ожидание" (Stop-and-Wait)

    Порядковые номера пакетов

    Подтверждения (ACK)

    Повторная передача при таймауте

    Гарантирует порядок доставки пакетов

Проверка кода

    Соответствие PEP8: pycodestyle src/*.py

    Проверка типов: mypy --strict src/*.py

    Тесты: test/test.sh

Автор

Егор Белов

