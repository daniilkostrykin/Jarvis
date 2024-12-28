import pygetwindow as gw
import tkinter as tk
import speech_recognition as sr
import threading
import time

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

# Расширенный маппинг для порядковых числительных
ordinals = {
    "первое": 0,
    "первый": 0,
    "первая": 0,
    "второе": 1,
    "второй": 1,
    "вторая": 1,
    "третье": 2,
    "третий": 2,
    "третья": 2,
    "четвертое": 3,
    "четвертый": 3,
    "четвертая": 3,
    "пятое": 4,
    "пятый": 4,
    "пятая": 4,
    "шестое": 5,
    "шестой": 5,
    "шестая": 5,
    "седьмое": 6,
    "седьмой": 6,
    "седьмая": 6,
    "восьмое": 7,
    "восьмой": 7,
    "восьмая": 7,
    "девятое": 8,
    "девятый": 8,
    "девятая": 8,
    "десятое": 9,
    "десятый": 9,
    "десятая": 9,
    "одиннадцатое": 10,
    "одиннадцатый": 10,
    "одиннадцатая": 10,
    "двенадцатое": 11,
    "двенадцатый": 11,
    "двенадцатая": 11,
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

def select_window_from_list(on_selection_callback):
    """Показывает список всех окон и ожидает выбора голосом."""
    windows = [win for win in gw.getAllWindows() if win.title.strip()]
    if not windows:
        print("Нет доступных окон.")
        return None

    window_titles = [win.title for win in windows]
    root = tk.Tk()
    root.title("Выбор окна")
    root.geometry("600x400")

    label = tk.Label(
        root,
        text="Список доступных окон. Назовите порядковый номер окна, например: 'третье':",
        font=("Arial", 14)
    )
    label.pack(pady=10)
    text = tk.Text(root, font=("Arial", 12), wrap="word")
    text.insert("1.0", "\n".join(
        [f"{i + 1}. {title}" for i, title in enumerate(window_titles)]))
    text.config(state="disabled")
    text.pack(expand=True, fill="both", padx=10, pady=10)
    root.update()
    root.deiconify()

    def listen_for_selection(root, windows):
        """Слушает номер окна от пользователя в отдельном потоке."""
        recognizer = sr.Recognizer()
        stop_listening = False
        while not stop_listening:
            with sr.Microphone() as source:
                print("Слушаю номер окна...")
                try:
                    audio = recognizer.listen(source, timeout=5)
                    command = recognizer.recognize_google(audio, language='ru-RU')
                    print(f"Вы сказали: {command}")
                    stop_listening = process_selection(command, windows, root)
                except sr.UnknownValueError:
                    print("Не удалось распознать речь. Попробуйте снова.")
                except sr.RequestError:
                    print("Проблема с подключением к интернету. Попробуйте снова.")
                except sr.WaitTimeoutError:
                    print("Вы ничего не сказали. Попробуйте снова.")

    def process_selection(command, windows, root):
        """Обрабатывает выбранное окно на основе порядкового номера."""
        if command == "стоп":
            on_selection_callback(False)
            root.after(0, lambda: root.destroy())
            return True

        if command:
            command = command.lower().strip()
            command = command.replace("окно", "").strip()
            parts = command.split()

            if parts[0] in ordinals:
                choice = ordinals[parts[0]]
                if 0 <= choice < len(windows):
                    selected_window = windows[choice]
                    print(
                        f"Переключение на: {selected_window.title}, минимизировано ли оно: {selected_window.isMinimized}"
                    )

                    if selected_window.isMinimized:
                        selected_window.restore()

                    try:
                        selected_window.activate()
                        selected_window.bringToFront()
                        print(f"Окно активно: {selected_window.title}")
                    except Exception as e:
                        print(f"Ошибка активации {e}")

                    on_selection_callback(True)
                    root.after(0, lambda: root.destroy())
                    return True
                else:
                    print("Выбранный номер окна не существует.")
            else:
                print("Не распознано порядковое число. Пожалуйста, скажите, например, 'первое' или 'третье'.")
        return False

    threading.Thread(target=listen_for_selection, args=(root, windows), daemon=True).start()
    root.mainloop()


def switch_to_application(app_name):
    """Переключиться на окно приложения по названию или через список окон."""
    window = get_application_window(app_name)
    if not window:
        print(f"Приложение '{app_name}' не найдено. Выберите окно из списка.")
        # <-отладочная инфа- не должно  быть проблем.
        print(f"Сейчас вызываем окно со списком: {app_name=}")

        def on_selection_complete(selected):
            if selected:
                print("Переключение завершено")
            else:
                print("Переключение не произошло")

        select_window_from_list(on_selection_complete)
        return

    try:
        if window.isMinimized:
            window.restore()  # Восстанавливаем окно, если оно минимизировано
        window.activate()  # Переключаемся на окно
        window.bringToFront()  # Переводим окно на передний план
        print(f"Переключено на окно: {window.title}")
    except Exception as e:
        print(f"Ошибка при активации окна: {e}")