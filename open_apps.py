# open_apps.py
import os
import subprocess

# Словарь с приложениями и путями
translations = {
    "рабочий стол": os.path.join(os.path.expanduser("~"), "Desktop"),
    "загрузки": os.path.join(os.path.expanduser("~"), "Downloads"),
    "документы": os.path.join(os.path.expanduser("~"), "Documents"),
    "изображения": os.path.join(os.path.expanduser("~"), "Pictures"),
    "музыка": os.path.join(os.path.expanduser("~"), "Music"),
    "видео": os.path.join(os.path.expanduser("~"), "Videos"),
    "telegram": "C:\\Users\\Daniil\\Downloads\\Telegram Desktop\\AyuGram\\AyuGram.exe",  # Пример для Telegram
    "телеграм": "C:\\Users\\Daniil\\Downloads\\Telegram Desktop\\AyuGram\\AyuGram.exe",  # Пример для Telegram
    "браузер": "C:\\Users\\Daniil\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Yandex.lnk",  # Пример для браузера
    "блокнот": "C:\\Windows\\System32\\notepad.exe",  # Пример для Блокнота
}

def open_application(command):
    """Открывает приложение по указанной команде."""
    command = command.lower()
    for key, path in translations.items():
        if key in command:
            if os.path.exists(path):
                if path.endswith(".exe"):  # Если это исполнимый файл
                    try:
                        subprocess.run(path)
                        print(f"Открываю {key}...")
                        return
                    except Exception as e:
                        print(f"Не удалось открыть {key}: {e}")
                else:  # Если это папка
                    try:
                        os.startfile(path)
                        print(f"Открываю папку {key}...")
                        return
                    except Exception as e:
                        print(f"Не удалось открыть папку {key}: {e}")
            else:
                print(f"Путь для {key} не существует.")
    print(f"Приложение или папка для команды '{command}' не найдено.")
