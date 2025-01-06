import unittest
from src.Bellman_Ford import Graph


class TestGraph(unittest.TestCase):

    def setUp(self):
        # Инициализация графа перед каждым тестом
        self.graph = Graph(vertices=5)
        self.graph.vertex_names = ['A', 'B', 'C', 'D', 'E']

    def test_add_edge(self):
        # Тестирование добавления рёбер
        self.graph.add_edge(0, 1, 10)
        self.graph.add_edge(0, 2, 5)
        self.assertEqual(len(self.graph.graph), 2)
        self.assertIn([0, 1, 10], self.graph.graph)
        self.assertIn([0, 2, 5], self.graph.graph)

    def test_bellman_ford_no_negative_cycle(self):
        # Тестирование алгоритма без отрицательных циклов
        self.graph.add_edge(0, 1, 6)
        self.graph.add_edge(0, 2, 7)
        self.graph.add_edge(1, 2, 8)
        self.graph.add_edge(1, 3, 5)
        self.graph.add_edge(1, 4, -4)
        self.graph.add_edge(2, 3, -3)
        self.graph.add_edge(2, 4, 9)
        self.graph.add_edge(3, 1, -2)
        self.graph.add_edge(4, 3, 7)

        status, result = self.graph.bellman_ford(0)
        self.assertTrue(status)
        expected_distances = [0, 2, 7, 4, -2]
        # Парсим результат для проверки расстояний
        for i, line in enumerate(result.split('\n')[1:6]):
            parts = line.split('\t\t')
            vertex = parts[0]
            distance = parts[1]
            self.assertEqual(int(distance) if distance != "бесконечность" else float("Inf"), expected_distances[i])

    def test_bellman_ford_with_negative_cycle(self):
        # Тестирование алгоритма с отрицательным циклом
        self.graph.add_edge(0, 1, 1)
        self.graph.add_edge(1, 2, -1)
        self.graph.add_edge(2, 3, -1)
        self.graph.add_edge(3, 1, -1)  # Создаём цикл отрицательного веса

        status, message = self.graph.bellman_ford(0)
        self.assertFalse(status)
        self.assertEqual(message, "Граф содержит цикл отрицательного веса.")

    def test_bellman_ford_disconnected_graph(self):
        # Тестирование алгоритма на несвязном графе
        self.graph.add_edge(0, 1, 4)
        self.graph.add_edge(0, 2, 5)
        # Вершины 3 и 4 не связаны
        status, result = self.graph.bellman_ford(0)
        self.assertTrue(status)
        # Проверяем, что расстояния до 3 и 4 бесконечны
        lines = result.split('\n')
        distance_e = lines[5].split('\t\t')[1]
        distance_d = lines[4].split('\t\t')[1]
        self.assertEqual(distance_d, "бесконечность")
        self.assertEqual(distance_e, "бесконечность")

    def test_get_path(self):
        # Тестирование восстановления пути
        self.graph.add_edge(0, 1, 2)
        self.graph.add_edge(1, 2, 3)
        self.graph.add_edge(0, 2, 5)
        status, result = self.graph.bellman_ford(0)
        self.assertTrue(status)
        # Проверяем путь до вершины 2
        lines = result.split('\n')
        path = lines[3].split('\t\t')[2]
        self.assertEqual(path, "A -> B -> C")


if __name__ == '__main__':
    unittest.main()