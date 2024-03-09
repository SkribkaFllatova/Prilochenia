#1.	Считать из параметров командной строки одномерный массив, состоящий из N целочисленных элементов.
#2.	Вывести наибольший элемент массива, который делиться на 2 без остатка.
#3.	Вывести в порядке возрастания четные числа массива меньше 10 или сообщить, что таких чисел нет.

import sys

if len(sys.argv) < 2:
    print("Введите целочисленные элементы массива")
    sys.exit()

N = len(sys.argv) - 1
arr = []

for i in range(N):
    arr.append(int(sys.argv[i+1]))

max_even_divisible_by_2 = None
even_less_than_10 = []

for num in arr:
    if num % 2 == 0 and (max_even_divisible_by_2 is None or num > max_even_divisible_by_2):
        max_even_divisible_by_2 = num

    if num % 2 == 0 and num < 10:
        even_less_than_10.append(num)

if max_even_divisible_by_2:
    print(f"Наибольший элемент массива, который делится на 2 без остатка: {max_even_divisible_by_2}")
else:
    print("В массиве нет элементов, которые делятся на 2 без остатка")

if even_less_than_10:
    print("Четные числа массива меньше 10 в порядке возрастания:", sorted(even_less_than_10))
else:
    print("В массиве нет четных чисел меньше 10")
