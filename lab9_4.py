LIMIT_1 = 10000
LIMIT_2 = 20000
RATE_1 = 0.1
RATE_2 = 0.15
RATE_3 = 0.2

def calculate_tax(income): #Калькулятор расчета налога
    if income <= LIMIT_1: 
        return income * RATE_1 #Если доход до 10000, то умножаем на 0.1 (10%)
    elif income <= LIMIT_2: 
        return income * RATE_2 #Если доход до 20000, то умножаем на 0.15 (15%)
    else: 
        return income * RATE_3 #В ином случае умножаем на 0.2 (20%)
