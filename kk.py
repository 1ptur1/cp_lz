import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from log import log_decorator

class SchoolStatistics:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None

    @log_decorator()
    def load_data(self):
        """Загружает данные из CSV по ссылке"""
        self.df = pd.read_csv(self.file_path)
        print("Данные загружены успешно!")

    @log_decorator()
    def filter_states(self, states_to_keep):
        """Фильтрует данные по списку штатов"""
        if self.df is None:
            print("Ошибка: данные не загружены!")
            return None

        self.df = self.df[self.df["STATE"].isin(states_to_keep)]
        print("Фильтрация завершена!")

    @log_decorator()
    def process_data(self):
        """Обрабатывает данные, считая количество школ и средний бюджет по штатам"""
        if self.df is None:
            print("Ошибка: данные не загружены!")
            return None

        stats = self.df.groupby("STATE").agg(
            schools_count=("STATE", "count"),
            avg_budget=("TOTALREV", "mean")
        ).reset_index()

        return stats

    @log_decorator()
    def plot_statistics(self, stats):
        """Строит 3D-гистограмму: количество школ и средний бюджет по штатам"""
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        
        xpos = np.arange(len(stats["STATE"]))
        ypos = np.zeros_like(xpos)
        dz_schools = stats["schools_count"].values
        dz_budget = stats["avg_budget"].values
        
        ax.bar3d(xpos, ypos, np.zeros_like(dz_schools), 0.5, 0.5, dz_schools, color='b', label='Количество школ')
        ax.bar3d(xpos, ypos + 1, np.zeros_like(dz_budget), 0.5, 0.5, dz_budget, color='g', label='Средний бюджет')
        
        ax.set_xticks(xpos)
        ax.set_xticklabels(stats["STATE"], rotation=45)
        ax.set_ylabel("Параметры")
        ax.set_zlabel("Значение")
        ax.set_title("Количество школ и их средний бюджет по штатам")
        
        plt.legend()
        plt.show()

file_path = "school_data.csv"  # Путь к файлу с данными
stats = SchoolStatistics(file_path)
stats.load_data()
stats.filter_states(["Texas", "California", "Alabama", "Iowa", "Washington", "Hawaii"])
data = stats.process_data()

if data is not None:
    stats.plot_statistics(data)