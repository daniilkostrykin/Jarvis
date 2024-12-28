import speech_recognition as sr
import pyttsx3
import os

def speak(text):
    """Озвучивает текст."""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen_for_keyword(keyword="джарвис"):
    """Слушает ключевое слово и запускает программу."""
    recognizer = sr.Recognizer()
    print(f"Скажите '{keyword}', чтобы запустить программу.")
    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                print("Слушаю...")
                audio = recognizer.listen(source, timeout=100)  # Ожидает максимум 10 секунд
                command = recognizer.recognize_google(audio, language="ru-RU").lower()
                print(f"Вы сказали: {command}")
                if keyword in command:
                    speak("Я вас слушаю.")
                    run_jarvis()  # Запуск основной программы
        except sr.UnknownValueError:
            print("Не удалось распознать. Скажите снова.")
        except sr.RequestError:
            print("Проблема с подключением к интернету.")
        except sr.WaitTimeoutError:
            print("Временное ожидание завершено. Слушаю снова.")

def run_jarvis():
    """Ваша основная программа."""
    # Здесь вставьте основной код программы
    speak("Запускаю программу.")
    os.system("python main.py")  # Запускает вашу программу

# Основной запуск
if __name__ == "__main__":
    listen_for_keyword("алиса")

    
    
