import pygetwindow as gw
import tkinter as tk
from tkinter import simpledialog, messagebox

# Словарь с пользовательскими названиями для поиска окон
app_mapping = {
    "блокнот": "Блокнот",
    "telegram": "AyuGram",
    "вс код": "Visual Studio Code",
    "браузер": "Yandex",
    "яндекс": "Yandex Browser",
    "зона": "Zona",
    "чат": "ChatGPT",
}


def get_application_window(app_name):
    """Найти окно, связанное с приложением, по названию окна."""
    # Получаем реальное название окна из словаря
    real_window_name = app_mapping.get(app_name.lower())

    if not real_window_name:
        print(f"Приложение '{app_name}' не найдено в словаре.")
        return None

    # Перебираем все окна и ищем, у кого в названии есть нужное слово
    for window in gw.getAllWindows():
        if real_window_name.lower() in window.title.lower():  # Фильтруем окна по названию
            print(f"Найдено окно: {window.title}")
            return window  # Возвращаем первое подходящее окно

    print(f"Не найдено окно для запроса '{app_name}'.")
    return None


def select_window_from_list():
    """Показывает список всех окон и позволяет выбрать порядковый номер."""
    windows = gw.getAllWindows()
    window_titles = [win.title for win in windows if win.title.strip()]

    if not window_titles:
        print("Нет доступных окон.")
        return None

    # Создаём графический интерфейс с Tkinter
    root = tk.Tk()
    root.withdraw()  # Скрываем основное окно

    # Создаём строку с нумерованным списком окон
    window_list = "\n".join([f"{i + 1}. {title}" for i, title in enumerate(window_titles)])
    prompt = f"Выберите окно из списка (введите номер):\n\n{window_list}"
    choice = simpledialog.askinteger("Выбор окна", prompt, minvalue=1, maxvalue=len(window_titles))

    if choice is None:  # Если выбор отменён
        print("Выбор окна отменён.")
        return None

    selected_window = windows[choice - 1]
    return selected_window


def switch_to_application(app_name):
    """Переключиться на окно приложения по названию или через список окон."""
    window = get_application_window(app_name)
    if not window:
        print(f"Приложение '{app_name}' не найдено. Предлагаем выбрать из списка окон.")
        window = select_window_from_list()

    if window:
        try:
            if window.isMinimized:
                window.restore()  # Восстанавливаем окно, если оно минимизировано
            window.activate()  # Переключаемся на окно
            print(f"Переключено на окно: {window.title}")
        except Exception as e:
            print(f"Ошибка при активации окна: {e}")
    else:
        print("Окно для переключения не выбрано.")


if __name__ == "__main__":
    # Пример использования
    switch_to_application("браузер")  # Например, ищем окно по слову "браузер"
