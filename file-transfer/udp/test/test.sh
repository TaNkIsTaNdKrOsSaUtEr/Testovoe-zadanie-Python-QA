#!/bin/bash

# Генерация тестового файла (1.5MB)
dd if=/dev/urandom of=testfile.bin bs=1M count=1 status=none
dd if=/dev/urandom seek=1 bs=512K count=1 of=testfile.bin status=none

# Запуск сервера в фоне
python3 ../src/server.py testfile.bin &
SERVER_PID=$!

# Даем серверу время на запуск
sleep 2  # Для UDP нужно больше времени

# Запуск клиента
python3 ../src/client.py received.bin

# Остановка сервера
kill $SERVER_PID
wait $SERVER_PID 2>/dev/null

# Проверка файлов
if cmp -s testfile.bin received.bin; then
    echo "UDP Test passed: Files match"
else
    echo "UDP Test failed: Files differ"
fi

# Удаление временных файлов
rm testfile.bin received.bin
