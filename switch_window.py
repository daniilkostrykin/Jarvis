import pygetwindow as gw

# Словарь с пользовательскими названиями приложений и их исполнимыми именами
app_mapping = {
    "блокнот": "notepad.exe",  # для блокнота
    "telegram": "AyuGram.exe",  # для Telegram
    "вс код": "Code.exe",  # для Visual Studio Code
    "браузер": "chrome.exe",  # для Chrome
    "яндекс": "browser.exe",  # для Яндекс браузера
    "зона": "Zona",  # для Zona - имя должно быть реальным названием exe процесса в системе!
    "чат": "ChatGPT.exe", 
}

def get_application_window(app_name):
    """Найти окно, связанное с приложением, по названию окна."""
    # Перебираем все окна
    for window in gw.getAllWindows():
        if app_name.lower() in window.title.lower():  # Фильтруем окна по названию
            print(f"Найдено окно: {window.title}")
            return window  # Возвращаем первое подходящее окно

    print(f"Не найдено окно для запроса '{app_name}'.")
    return None

def switch_to_application(app_name):
    """Переключиться на окно приложения по названию."""
    window = get_application_window(app_name)
    if window:
        try:
            if window.isMinimized:
                window.restore()  # Восстанавливаем окно, если оно минимизировано
            window.activate()  # Переключаемся на окно
            print(f"Переключено на окно приложения '{app_name}'.")
            return True
        except Exception as e:
            print(f"Ошибка при активации окна: {e}")
            return False
    return False


if __name__ == "__main__":
    # Пример использования
    switch_to_application("Блокнот")  # Например, ищем окно по слову "telegram"
