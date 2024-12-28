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
import subprocess

def run_task(task_name):
    """Запускает задачу из Планировщика задач."""
    try:
        result = subprocess.run(
            ["schtasks", "/run", "/tn", task_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode == 0:
            print(f"Задача '{task_name}' успешно запущена.")
            return True
        else:
            print(f"Ошибка при запуске задачи '{task_name}': {result.stderr}")
            return False
    except Exception as e:
        print(f"Ошибка выполнения: {e}")
        return False

def open_link(command, task_name=None):
    """Открывает ссылку по указанной команде и запускает задачу, если указано."""
    command = command.lower().strip()
    for key, url in links.items():
        if key in command:
            # Если указано задание в планировщике задач
            if task_name:
                if not run_task(task_name):
                    return False
                print(f"Запускаю задачу: {task_name}")
            # Открытие ссылки
            try:
                webbrowser.open(url)
                print(f"Открываю ссылку: {url}")
                return True
            except Exception as e:
                print(f"Ошибка при открытии ссылки {key}: {e}")
                return False
    print(f"Ссылка для команды '{command}' не найдена.")
    return False

def perform_action(command):
    """Обрабатывает команды для открытия приложений, папок или ссылок."""
    if command.startswith("открой") or command.startswith("запусти"):
        # Проверяем приложения и папки
        if open_application(command):
            return
        # Если команда для ссылки с запуском задачи
        if "youtube" in command:
            task_name = "RunAppAsAdmin"  # Имя задачи в Планировщике задач
            if open_link(command, task_name=task_name):
                return
        # Если приложение не найдено, пробуем открыть ссылку
        if open_link(command):
            return
    print(f"Команда '{command}' не распознана.")
