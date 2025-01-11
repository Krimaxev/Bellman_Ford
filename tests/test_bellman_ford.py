import unittest
import time
from memory_profiler import memory_usage
from src.Bellman_Ford import Graph


class TestGraph(unittest.TestCase):

    def setUp(self):
        # Инициализация графа перед каждым тестом
        self.graph = Graph(vertices=15)
        self.graph.vertex_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O']

    def measure_performance(self, setup_edges):
        """
        Метод для измерения времени и памяти выполнения алгоритма Форда-Беллмана.
        :param setup_edges: Функция для добавления рёбер в граф.
        :return: Tuple (время выполнения, память)
        """
        # Добавление рёбер графа
        setup_edges()

        # Функция для запуска алгоритма
        def run_bellman_ford():
            self.graph.bellman_ford(0)

        # Измерение времени выполнения
        start_time = time.perf_counter()
        mem_usage = memory_usage((run_bellman_ford,), max_iterations=1, interval=0.01)
        end_time = time.perf_counter()

        execution_time = end_time - start_time
        max_memory = max(mem_usage) - min(mem_usage)

        return execution_time, max_memory

    def test_graph1_performance(self):
        """Тестирование производительности на Графе 1: Случайный граф без отрицательных циклов"""

        def setup_graph1():
            edges = [
                (0, 1, 2), (0, 2, 4), (1, 2, 1), (1, 3, 7), (2, 4, 3),
                (3, 5, 1), (4, 5, 5), (5, 6, 2), (6, 7, 3), (7, 8, 1),
                (8, 9, 4), (9, 10, 2), (10, 11, 3), (11, 12, 1), (12, 13, 2),
                (13, 14, 3), (14, 0, 6), (1, 4, 2), (2, 3, 3), (4, 6, 4),
                (5, 7, 2), (6, 8, 3), (7, 9, 2), (8, 10, 4), (9, 11, 3),
                (10, 12, 2), (11, 13, 3), (12, 14, 2), (13, 0, 4), (14, 1, 5)
            ]
            for src, dest, weight in edges:
                self.graph.add_edge(src, dest, weight)

        time_exec, mem_usage = self.measure_performance(setup_graph1)
        print(f"Граф 1 - Время выполнения: {time_exec:.6f} секунд, Потребление памяти: {mem_usage:.2f} МБ")
        self.assertTrue(time_exec < 1)  # Примерное условие для успешного прохождения теста

    def test_graph2_performance(self):
        """Тестирование производительности на Графе 2: Граф с отрицательным циклом"""

        def setup_graph2():
            edges = [
                (0, 1, 5), (1, 2, 3), (2, 3, 1), (3, 4, -10), (4, 1, 2),
                (4, 5, 4), (5, 6, 2), (6, 7, 3), (7, 8, 1), (8, 9, 4),
                (9, 10, 2), (10, 11, 3), (11, 12, 1), (12, 13, 2), (13, 14, 3),
                (14, 0, 6), (1, 4, 2), (2, 3, 1), (3, 4, -10), (4, 1, 2)
            ]
            for src, dest, weight in edges:
                self.graph.add_edge(src, dest, weight)

        time_exec, mem_usage = self.measure_performance(setup_graph2)
        print(f"Граф 2 - Время выполнения: {time_exec:.6f} секунд, Потребление памяти: {mem_usage:.2f} МБ")
        # Для графа с отрицательным циклом нет необходимости проверять время выполнения

    def test_graph3_performance(self):
        """Тестирование производительности на Графе 3: Плотный граф с положительными весами"""

        def setup_graph3():
            edges = [
                (0, 1, 1), (0, 2, 2), (0, 3, 3), (0, 4, 4), (0, 5, 5),
                (0, 6, 6), (0, 7, 7), (0, 8, 8), (0, 9, 9), (0, 10, 10),
                (0, 11, 11), (0, 12, 12), (0, 13, 13), (0, 14, 14),
                (1, 2, 1), (1, 3, 2), (1, 4, 3), (1, 5, 4), (1, 6, 5),
                (1, 7, 6), (1, 8, 7), (1, 9, 8), (1, 10, 9), (1, 11, 10),
                (1, 12, 11), (1, 13, 12), (1, 14, 13), (2, 3, 1), (2, 4, 2),
                (2, 5, 3), (2, 6, 4), (2, 7, 5), (2, 8, 6), (2, 9, 7),
                (2, 10, 8), (2, 11, 9), (2, 12, 10), (2, 13, 11), (2, 14, 12),
                (3, 4, 1), (3, 5, 2), (3, 6, 3), (3, 7, 4), (3, 8, 5),
                (3, 9, 6), (3, 10, 7), (3, 11, 8), (3, 12, 9), (3, 13, 10),
                (3, 14, 11), (4, 5, 1), (4, 6, 2), (4, 7, 3), (4, 8, 4),
                (4, 9, 5), (4, 10, 6), (4, 11, 7), (4, 12, 8), (4, 13, 9),
                (4, 14, 10), (5, 6, 1), (5, 7, 2), (5, 8, 3), (5, 9, 4),
                (5, 10, 5), (5, 11, 6), (5, 12, 7), (5, 13, 8), (5, 14, 9),
                (6, 7, 1), (6, 8, 2), (6, 9, 3), (6, 10, 4), (6, 11, 5),
                (6, 12, 6), (6, 13, 7), (6, 14, 8), (7, 8, 1), (7, 9, 2),
                (7, 10, 3), (7, 11, 4), (7, 12, 5), (7, 13, 6), (7, 14, 7),
                (8, 9, 1), (8, 10, 2), (8, 11, 3), (8, 12, 4), (8, 13, 5),
                (8, 14, 6), (9, 10, 1), (9, 11, 2), (9, 12, 3), (9, 13, 4),
                (9, 14, 5), (10, 11, 1), (10, 12, 2), (10, 13, 3), (10, 14, 4),
                (11, 12, 1), (11, 13, 2), (11, 14, 3), (12, 13, 1), (12, 14, 2),
                (13, 14, 1)
            ]
            for src, dest, weight in edges:
                self.graph.add_edge(src, dest, weight)

        time_exec, mem_usage = self.measure_performance(setup_graph3)
        print(f"Граф 3 - Время выполнения: {time_exec:.6f} секунд, Потребление памяти: {mem_usage:.2f} МБ")
        self.assertTrue(time_exec < 5)  # Примерное условие для успешного прохождения теста


if __name__ == '__main__':
    unittest.main()