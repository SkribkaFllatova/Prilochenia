from math import sqrt 
from triangle_func import IncorrectTriangleSides

class Triangle:
    def __init__(self, side1: float, side2: float, side3: float):

        if side1 <= 0 or side2 <= 0 or side3 <= 0:
            raise IncorrectTriangleSides("Стороны треугольника должны быть больше 0")
        if side1 + side2 <= side3 or side1 + side3 <= side2 or side2 + side3 <= side1:
            raise IncorrectTriangleSides("Недопустимые стороны треугольника")

        self.side1 = side1 #Присваиваются значения side1, side2, side3 соответствующим атрибутам self
        self.side2 = side2
        self.side3 = side3

    def triangle_type(self): #Метод triangle_type определяет тип треугольника: равносторонний, равнобедренный или неравносторонний, в зависимости от длин сторон
        if self.side1 == self.side2 == self.side3:
            return "equilateral" #равносторонний
        elif self.side1 == self.side2 or self.side1 == self.side3 or self.side2 == self.side3:
            return "isosceles" #равнобедренный
        else:
            return "nonequilateral" #неравносторонний

    def perimeter(self): #Метод perimeter возвращает периметр треугольника, который равен сумме длин всех трех сторон
        return self.side1 + self.side2 + self.side3
