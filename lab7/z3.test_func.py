import unittest
from triangle_func import get_triangle_type, IncorrectTriangleSides #Импорn функция get_triangle_type и класс IncorrectTriangleSides из модуля triangle_func

class TestTriangleFunc(unittest.TestCase): #Создание класса TestTriangleFunc, который наследуется от unittest.TestCase

    def test_equilateral_triangle(self): #Тест равносторонний треугольник
        self.assertEqual(get_triangle_type(1, 1, 1), "equilateral")

    def test_isosceles_triangle(self): #Тест равнобедренный треугольник
        self.assertEqual(get_triangle_type(5, 5, 3), "isosceles")

    def test_nonequilateral_triangle(self): #Тест неравносторонний треугольник
        self.assertEqual(get_triangle_type(3, 4, 6), "nonequilateral")
#В каждом тестовом методе вызывается функция get_triangle_type с определенными сторонами треугольника и сравнивается возвращаемое значение с ожидаемым

    def test_invalid_triangle_sides(self):
        with self.assertRaises(IncorrectTriangleSides):
            get_triangle_type(0, 0, 0)
            get_triangle_type(2, 2, 5)
#В последнем тестовом методе test_invalid_triangle_sides проверяется обработка исключения IncorrectTriangleSides при передаче недопустимых значений сторон треугольника

if __name__ == "__main__":
    unittest.main()
    
#Программа проверяет все тестовые методы с помощью unittest
#Вызывается функция unittest.main() для запуска всех тестов
