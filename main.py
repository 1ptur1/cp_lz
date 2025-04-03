from kk import SchoolStatistics

file_path = "school_data.csv"  # Путь к файлу с данными
stats = SchoolStatistics(file_path)
print(stats.load_data())
print(stats.process_data())
print(stats.plot_statistics())