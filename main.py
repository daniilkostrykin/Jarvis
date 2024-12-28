from switch_window import switch_to_application, select_window_from_list
from open_apps import perform_action
import speech_recognition as sr
import pyttsx3

# Инициализация модуля синтеза речи
engine = pyttsx3.init()


def speak(text):
    """Функция для озвучивания текста."""
    engine.say(text)
    engine.runAndWait()


def listen():
    """Функция для распознавания голоса."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Слушаю...")
        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio, language='ru-RU')
            print(f"Вы сказали: {command}")
            return command.lower()
        except sr.UnknownValueError:
            print("Не удалось распознать речь.")
            return ""
        except sr.RequestError:
            print("Проблема с подключением к интернету.")
            return ""
        except sr.WaitTimeoutError:
            print("Вы ничего не сказали.")
            return ""


def get_command_input():
    """Функция для выбора способа ввода команды (только голосом)."""
    print("Голосовой ввод активирован. Слушаю...")
    return listen  # Возвращаем функцию для голосового ввода


def execute_command(command):
    """Обработка команд."""
    if command.startswith("открой") or command.startswith("запусти"):
        perform_action(command)
        return

    if "переключись на" in command:
        window_name = command.replace("переключись на", "").strip()
        switch_to_application(window_name)
        return

    print(f"Команда '{command}' не распознана.")


# Основная программа
if __name__ == "__main__":
    print("Привет! Я ваш ассистент. Чем могу помочь?")
    command_input_method = get_command_input()

    while True:
        command = command_input_method()
        if command in ["стоп", "выход", "до связи"]:
            print("Работа ассистента завершена.")
            break
        execute_command(command)
