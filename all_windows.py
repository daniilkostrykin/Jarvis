import pygetwindow as gw

def list_all_windows():
    """Вывод всех открытых окон и их заголовков."""
    windows = gw.getAllWindows()
    for window in windows:
        print(f"Название окна: {window.title}")

# Выводим все окна
if __name__ == "__main__":
    list_all_windows()