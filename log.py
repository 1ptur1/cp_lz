import pandas as pd
import os
import socket
import getpass
from datetime import datetime
from functools import wraps

def log_decorator(log_file='logs.csv'):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Данные для логирования
            log_id = 1
            pc_name = socket.gethostname()
            username = getpass.getuser()
            function_name = func.__name__
            now = datetime.now()
            date_str = now.strftime("%d.%m.%Y")
            time_str = now.strftime("%H:%M:%S")
            
            # Запись
            log_entry = {
                "id": log_id,
                "pc": pc_name,
                "username": username,
                "function name": function_name,
                "Date": date_str,
                "Time": time_str
            }
            
            # Загрузка или создание DF
            if os.path.exists(log_file):
                df = pd.read_csv(log_file)
                log_entry["id"] = df.shape[0] + 1  # ID на основе количества записей
                df = pd.concat([df, pd.DataFrame([log_entry])], ignore_index=True)
            else:
                df = pd.DataFrame([log_entry])
            
            # Сохранение в файл
            df.to_csv(log_file, index=False)
            
            return func(*args, **kwargs)
        return wrapper
    return decorator