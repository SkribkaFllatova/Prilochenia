from math import sqrt

class IncorrectTriangleSides(Exception): #Создание исключения IncorrectTriangleSides
    pass

def get_triangle_type(side1: float, side2: float, side3: float):

    if side1 <= 0 or side2 <= 0 or side3 <= 0:
        raise IncorrectTriangleSides("Стороны треугольника должны быть больше 0")
    if side1 + side2 <= side3 or side1 + side3 <= side2 or side2 + side3 <= side1:
        raise IncorrectTriangleSides("Недопустимые стороны треугольника")
    
    if side1 == side2 == side3:
        return "equilateral" #Равносторонний
    elif side1 == side2 or side1 == side3 or side2 == side3:
        return "isosceles" #Равнобедренный
    else:
        return "nonequilateral" #Неравносторонний
