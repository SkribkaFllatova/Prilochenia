#!/bin/bash

if [ -z "$1" ]; then # -z — проверяет, пустая ли строка, $1 — доступ к аргументам, переданным скрипту.
    echo "Укажите верное имя текстового файла, проверьте правильность написания!" # вывод текста в консоль.
    exit 1
fi

if [ -f "$1" ]; then
    wc -l "$1" # wc -l <file> - подсчет строк.
    wc -w "$1" # wc -w <file> - подсчет слов.
    wc -m "$1" # wc -m <file> - подсчет символов.
fi
