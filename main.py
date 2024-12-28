# main.py
import pyttsx3
import speech_recognition as sr
from switch_window import switch_to_application
from open_apps import open_application

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
    """Функция для выбора способа ввода команды."""
    while True:
        print("Выберите способ ввода: 1 - голосом, 2 - текстом")
        choice = input("Ваш выбор (1/2): ").strip()
        if choice == "1":
            return listen
        elif choice == "2":
            return lambda: input("Введите команду: ").strip().lower()
        else:
            print("Некорректный выбор. Попробуйте снова.")

def execute_command(command):
    """Обработка команд."""
    if command.startswith("открой"):
      app_name = command.replace("открой", "").strip()
      open_application(app_name)
      return
   
    if "переключись на" in command:
     window_name = command.replace("переключись на", "").strip()
     switch_to_application(window_name)
     return

    print(f"Команда '{command}' не распознана.")

# Обновленный вызов программы
if __name__ == "__main__":
    print("Привет! Я ваш ассистент. Чем могу помочь?")
    command_input_method = get_command_input()

    while True:
        command = command_input_method()
        if command == "стоп":
            print("Работа ассистента завершена.")
            break
        execute_command(command)