#!/bin/bash

if [ -z "$1" ]; then
  echo "Число $0"
  exit 1
fi

number=$1

result=$((number ** 2))

echo "$result"