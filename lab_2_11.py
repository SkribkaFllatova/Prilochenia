#1.	Считать с клавиатуры произвольную строку.
#2.	Подсчитать самую длинную последовательность подряд идущих букв "g".
#3.	Заменить все точки восклицательными знаками.
#4.	Вывести в консоль полученную строку.

def longest_sequence_of_g(input_string):
    max_count = 0
    current_count = 0
    
    for letter in input_string:
        if letter == 'g':
            current_count += 1
            max_count = max(max_count, current_count)
        else:
            current_count = 0
    return max_count

input_string = input("Введите произвольную строку: ")
print("Самая длинная последовательность букв 'g' подряд:", longest_sequence_of_g(input_string))

new_string = input_string.replace('.', '!')
print("Строка с замененными точками:", new_string)
