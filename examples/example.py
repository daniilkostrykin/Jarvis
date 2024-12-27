import pyttsx3
import speech_recognition as sr
import os

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
            speak("Извините, я вас не понял.")
            return ""
        except sr.RequestError:
            speak("Проблема с подключением к интернету.")
            return ""
        except sr.WaitTimeoutError:
            speak("Вы ничего не сказали.")
            return ""

def execute_command(command):
    """Обработка команд."""
    if "открой папку" in command:
        folder_path = "C:\\Users\\Daniil"
        os.startfile(folder_path)
        speak(f"Открываю папку")
    elif "до связи" in command:
        speak("До встречи!")
        exit()
    else:
        speak("Команда не распознана.")

# Основной цикл программы
if __name__ == "__main__":
    speak("Привет! Я ваш ассистент. Чем могу помочь?")
    while True:
        command = listen()
        if command:
            execute_command(command)
