import os
import subprocess
import webbrowser

# Словарь с приложениями и путями
translations = {
    "рабочий стол": os.path.join(os.path.expanduser("~"), "Desktop"),
    "загрузки": os.path.join(os.path.expanduser("~"), "Downloads"),
    "документы": os.path.join(os.path.expanduser("~"), "Documents"),
    "изображения": os.path.join(os.path.expanduser("~"), "Pictures"),
    "музыка": os.path.join(os.path.expanduser("~"), "Music"),
    "видео": os.path.join(os.path.expanduser("~"), "Videos"),
    "telegram": "C:\\Users\\Daniil\\Downloads\\Telegram Desktop\\AyuGram\\AyuGram.exe",
    "телеграм": "C:\\Users\\Daniil\\Downloads\\Telegram Desktop\\AyuGram\\AyuGram.exe",
    "браузер": "C:\\Users\\Daniil\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Yandex.lnk",
    "блокнот": "C:\\Windows\\System32\\notepad.exe",
}

# Словарь с полезными ссылками
links = {
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "github": "https://github.com/daniilkostrykin?tab=repositories",
    "почта": "https://mail.google.com",
    "новости": "https://news.google.com",
}

def open_application(command):
    """Открывает приложение или папку по указанной команде."""
    command = command.lower().strip()
    for key, path in translations.items():
        if key in command:
            if os.path.exists(path):
                if path.endswith(".exe"):  # Если это исполняемый файл
                    try:
                        subprocess.Popen([path])
                        print(f"Открываю {key}...")
                        return True
                    except Exception as e:
                        print(f"Ошибка при открытии {key}: {e}")
                else:  # Если это папка
                    try:
                        os.startfile(path)
                        print(f"Открываю папку {key}...")
                        return True
                    except Exception as e:
                        print(f"Ошибка при открытии папки {key}: {e}")
            else:
                print(f"Путь для {key} не существует: {path}")
    return False

def open_link(command):
    """Открывает ссылку по указанной команде."""
    command = command.lower().strip()
    for key, url in links.items():
        if key in command:
            try:
                webbrowser.open(url)
                print(f"Открываю ссылку: {url}")
                return True
            except Exception as e:
                print(f"Ошибка при открытии ссылки {key}: {e}")
    return False

def perform_action(command):
    """Обрабатывает команды для открытия приложений, папок или ссылок."""
    if command.startswith("открой") or command.startswith("запусти"):
        # Сначала проверяем приложения и папки
        if open_application(command):
            return
        # Если приложение не найдено, пробуем открыть ссылку
        if open_link(command):
            return
    print(f"Команда '{command}' не распознана.")
