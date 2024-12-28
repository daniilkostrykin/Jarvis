import tkinter as tk
import psutil
import pygetwindow as gw

def get_current_app_name():
    """Получает название приложения для активного окна."""
    windows = gw.getWindowsWithTitle(gw.getActiveWindow().title)
    if windows:
        window = windows[0]
        return window.title  # Возвращает заголовок окна
    return "Неизвестное приложение"

def show_app_info():
    """Отображает информацию о текущем приложении в окне."""
    root = tk.Tk()
    root.title("Информация о приложении")
    label = tk.Label(root, text="Заголовок приложения: " + get_current_app_name(), font=("Arial", 14))
    label.pack(pady=20)
    root.mainloop()

# Запуск интерфейса
show_app_info()
