import tkinter as tk
from tkinter import messagebox
import math
import re

class Graph:
    def __init__(self, vertices):
        self.M = vertices   # Общее количество вершин в графе
        self.graph = []     # Список рёбер
        self.vertex_names = []  # Список названий вершин

    # Добавление ребра
    def add_edge(self, a, b, c):
        self.graph.append([a, b, c])

    # Печать решения с путями
    def print_solution(self, distance, predecessor, vertex_names):
        result = "Вершина\tРасстояние\tПуть от Источника\n"
        for k in range(self.M):
            path = self.get_path(k, predecessor, vertex_names)
            distance_str = "бесконечность" if distance[k] == float("Inf") else str(distance[k])
            result += f"{vertex_names[k]}\t\t{distance_str}\t\t{path}\n"
        return result

    # Восстановление пути от источника до вершины
    def get_path(self, vertex, predecessor, vertex_names):
        path = []
        while vertex is not None:
            path.insert(0, vertex_names[vertex])
            vertex = predecessor[vertex]
        return " -> ".join(path)

    # Алгоритм Форда-Беллмана
    def bellman_ford(self, src):
        distance = [float("Inf")] * self.M
        predecessor = [None] * self.M
        distance[src] = 0

        # Обновление расстояний
        for _ in range(self.M - 1):
            for a, b, c in self.graph:
                if distance[a] != float("Inf") and distance[a] + c < distance[b]:
                    distance[b] = distance[a] + c
                    predecessor[b] = a

        # Проверка на наличие цикла отрицательного веса
        for a, b, c in self.graph:
            if distance[a] != float("Inf") and distance[a] + c < distance[b]:
                return (False, "Граф содержит цикл отрицательного веса.")

        return (True, self.print_solution(distance, predecessor, vertex_names=self.vertex_names))

class BellmanFordGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Алгоритм Форда-Беллмана")
        self.root.geometry("800x600")
        self.create_main_window()

    def create_main_window(self):
        # Инструкция
        instruction = tk.Label(self.root,
                               text="Инструкция:\n'-' заменяется на 0\n'б' заменяется на бесконечность (999)\n"
                                    "Введите рёбра графа в формате: Вершина1 -> Вершина2 вес",
                               justify=tk.LEFT, font=('Arial', 12))
        instruction.pack(pady=10)

        # Ввод количества вершин
        vertices_frame = tk.Frame(self.root)
        vertices_frame.pack(pady=5)
        tk.Label(vertices_frame, text="Количество вершин:", font=('Arial', 12)).pack(side=tk.LEFT, padx=5)
        self.vertices_entry = tk.Entry(vertices_frame, width=10, font=('Arial', 12))
        self.vertices_entry.pack(side=tk.LEFT, padx=5)

        # Ввод названий вершин
        names_frame = tk.Frame(self.root)
        names_frame.pack(pady=5)
        tk.Label(names_frame, text="Названия вершин (через запятую):", font=('Arial', 12)).pack(side=tk.LEFT, padx=5)
        self.names_entry = tk.Entry(names_frame, width=50, font=('Arial', 12))
        self.names_entry.pack(side=tk.LEFT, padx=5)

        # Кнопка "Продолжить"
        tk.Button(self.root, text="Продолжить", command=self.show_edge_input_page, font=('Arial', 12, 'bold')).pack(pady=20)

    def show_edge_input_page(self):
        try:
            self.vertex_count = int(self.vertices_entry.get())
            self.vertex_names = [name.strip() for name in self.names_entry.get().split(',')]
            if len(self.vertex_names) != self.vertex_count:
                raise ValueError("Количество имён не совпадает с количеством вершин.")
            if self.vertex_count <= 0:
                raise ValueError("Количество вершин должно быть положительным числом.")
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
            return

        # Создание экземпляра Graph
        self.graph_instance = Graph(self.vertex_count)
        self.graph_instance.vertex_names = self.vertex_names  # Передаём названия вершин в класс Graph

        # Уничтожаем главное окно и создаём окно ввода рёбер
        for widget in self.root.winfo_children():
            widget.destroy()

        self.create_edge_input_page()

    def create_edge_input_page(self):
        # Инструкция
        instruction = tk.Label(self.root,
                               text="Введите рёбра графа в формате:\n"
                                    "Вершина1 -> Вершина2 вес\n"
                                    "Каждое ребро на новой строке.\n"
                                    "Для завершения ввода нажмите \"Рассчитать\".",
                               justify=tk.LEFT, font=('Arial', 12))
        instruction.pack(pady=10)

        # Текстовое поле для ввода рёбер
        self.edges_text = tk.Text(self.root, width=100, height=20, font=('Arial', 12))
        self.edges_text.pack(pady=10)

        # Кнопка расчёта
        tk.Button(self.root, text="Рассчитать", command=self.process_edges, font=('Arial', 12, 'bold')).pack(pady=10)

    def process_edges(self):
        raw_input = self.edges_text.get("1.0", tk.END).strip()
        if not raw_input:
            messagebox.showerror("Ошибка", "Пожалуйста, введите хотя бы одно ребро.")
            return

        lines = raw_input.split('\n')
        # Обновлённый паттерн: допускает произвольное количество пробелов вокруг '->' и после 'вес'
        edge_pattern = re.compile(r'^(\w+)\s*->\s*(\w+)\s+вес\s+([-+]?\d+)$')

        for line_num, line in enumerate(lines, start=1):
            # Удаляем лишние пробелы внутри строки
            normalized_line = ' '.join(line.strip().split())

            # Пропускаем пустые строки
            if not normalized_line:
                continue

            match = edge_pattern.match(normalized_line)
            if match:
                a, b, c = match.groups()
                if a not in self.graph_instance.vertex_names or b not in self.graph_instance.vertex_names:
                    messagebox.showerror("Ошибка",
                                         f"В строке {line_num}: Вершины должны существовать в списке названий.")
                    return
                a_index = self.graph_instance.vertex_names.index(a)
                b_index = self.graph_instance.vertex_names.index(b)

                # Обработка специальных символов
                if c == '-':
                    c = 0
                elif c.lower() == 'б':
                    c = 999
                else:
                    try:
                        c = int(c)
                    except ValueError:
                        messagebox.showerror("Ошибка", f"В строке {line_num}: Некорректный вес '{c}'.")
                        return

                self.graph_instance.add_edge(a_index, b_index, c)
            else:
                # Если строка не соответствует паттерну, проверяем, является ли она пустой после нормализации
                if normalized_line:
                    messagebox.showerror("Ошибка", f"В строке {line_num}: Некорректный формат.")
                    return
                # Если строка пустая, просто продолжаем
                continue

        # После успешного ввода всех рёбер запускаем алгоритм
        self.calculate_bellman_ford()

    def calculate_bellman_ford(self):
        status, result = self.graph_instance.bellman_ford(0)  # Источник - первая вершина

        # Создание окна с результатами
        result_window = tk.Toplevel(self.root)
        result_window.title("Результаты Алгоритма Форда-Беллмана")

        canvas = tk.Canvas(result_window, width=800, height=600, bg='white')
        canvas.pack(pady=10)

        # Размещение вершин по кругу
        radius = 250
        center_x = 400
        center_y = 300
        vertex_positions = []

        for i in range(self.graph_instance.M):
            angle = 2 * math.pi * i / self.graph_instance.M
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            vertex_positions.append((x, y))

            # Рисуем вершину
            canvas.create_oval(x - 25, y - 25, x + 25, y + 25, fill='lightblue', width=2)
            canvas.create_text(x, y, text=self.graph_instance.vertex_names[i], font=('Arial', 14, 'bold'))

        # Рисуем рёбра
        for edge in self.graph_instance.graph:
            a, b, c = edge
            x1, y1 = vertex_positions[a]
            x2, y2 = vertex_positions[b]

            # Вычисляем направляющий вектор
            dx = x2 - x1
            dy = y2 - y1
            length = math.sqrt(dx * dx + dy * dy)

            if length != 0:
                # Нормализуем вектор
                dx /= length
                dy /= length

                # Сдвигаем начальную и конечную точки
                start_x = x1 + dx * 25
                start_y = y1 + dy * 25
                end_x = x2 - dx * 25
                end_y = y2 - dy * 25

                # Рисуем стрелку
                canvas.create_line(start_x, start_y, end_x, end_y,
                                   arrow=tk.LAST, width=2, fill='black',
                                   arrowshape=(16, 20, 8))

                # Смещение текста перпендикулярно ребру
                perp_dx = -dy
                perp_dy = dx
                offset = 20  # Размер смещения
                mx = (start_x + end_x) / 2 + perp_dx * offset
                my = (start_y + end_y) / 2 + perp_dy * offset

                canvas.create_text(mx, my, text=str(c),
                                   font=('Arial', 12, 'bold'), fill='red')

        # Отображение результатов в текстовом формате
        if not status:
            # Если обнаружен отрицательный цикл
            tk.Label(result_window, text=result, font=('Arial', 14, 'bold'), fg='red').pack(pady=10)
        else:
            # Если цикла нет, отображаем расстояния и пути
            result_text = "Кратчайшие расстояния и пути от источника:\n\n"
            for line in result.split('\n')[1:]:
                result_text += f"{line}\n"

            # Используем виджет Text для более структурированного отображения
            text_widget = tk.Text(result_window, width=60, height=20, font=('Arial', 12))
            text_widget.pack(pady=10)
            text_widget.insert(tk.END, result)
            text_widget.config(state='disabled')  # Сделать текст только для чтения

if __name__ == "__main__":
    app = BellmanFordGUI()
    app.root.mainloop()