import pytest
from triangle_class import Triangle, IncorrectTriangleSides

def test_valid_triangle_creation(): #Тест test_valid_triangle_creation(), правильность создания треугольника
    triangle = Triangle(3, 4, 5) #Создается экземпляр класса Triangle с параметрами сторон 3, 4, 5
    assert triangle.side1 == 3 #Проверяется, что значения сторон у экземпляра соответствуют заданным: triangle.side1 == 3, triangle.side2 == 4, triangle.side3 == 5
    assert triangle.side2 == 4
    assert triangle.side3 == 5

def test_invalid_triangle_creation(): #Тест test_invalid_triangle_creation(), создание недопустимого треугольника

    with pytest.raises(IncorrectTriangleSides):
        triangle = Triangle(0, 0, 0) #Для случаев с некорректными значениями сторон (0, 0, 0) и (2, 2, 5) ожидается возникновение исключения IncorrectTriangleSides
        triangle = Triangle(2, 2, 5)

def test_triangle_type(): #Nест test_triangle_type(), тип тестового треугольника. Создаются три экземпляра класса Triangle с разными значениями сторон
    triangle1 = Triangle(1, 1, 1)
    assert triangle1.triangle_type() == "equilateral" #Проверяется, что для равностороннего треугольника triangle1.triangle_type() возвращает "equilateral"

    triangle2 = Triangle(5, 5, 3)
    assert triangle2.triangle_type() == "isosceles" #Для равнобедренного треугольника triangle2.triangle_type() возвращает "isosceles"

    triangle3 = Triangle(3, 4, 5)
    assert triangle3.triangle_type() == "nonequilateral" #Для произвольного треугольника triangle3.triangle_type() должен возвращает "nonequilateral"

def test_perimeter(): #Тест test_perimeter(). Создается экземпляр класса Triangle с параметрами 3, 4, 5
    triangle = Triangle(3, 4, 5)
    assert triangle.perimeter() == 12 #Проверяется, что метод triangle.perimeter() возвращает значение периметра равное 12

if __name__ == '__main__':
    pytest.main()
