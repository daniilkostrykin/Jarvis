from switch_window import switch_to_application, select_window_from_list
from open_apps import perform_action
import speech_recognition as sr
import pyttsx3
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

# Инициализация модуля синтеза речи
engine = pyttsx3.init()

# Создаем окно для отображения сообщений
root = tk.Tk()
root.title("Ассистент")
text_area = ScrolledText(root, wrap=tk.WORD, width=60, height=20, state='disabled')
text_area.pack(padx=10, pady=10)

def update_output(message):
    """Обновляет текст в окне."""
    text_area.config(state='normal')
    text_area.insert(tk.END, message + "\n")
    text_area.see(tk.END)  # Автопрокрутка к последнему сообщению
    text_area.config(state='disabled')

def speak(text):
    """Функция для озвучивания текста."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Функция для распознавания голоса."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        update_output("Слушаю...")
        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio, language='ru-RU')
            update_output(f"Вы сказали: {command}")
            return command.lower()
        except sr.UnknownValueError:
            update_output("Не удалось распознать речь.")
            return ""
        except sr.RequestError:
            update_output("Проблема с подключением к интернету.")
            return ""
        except sr.WaitTimeoutError:
            update_output("Вы ничего не сказали.")
            return ""

def get_command_input():
    """Функция для выбора способа ввода команды (только голосом)."""
    update_output("Голосовой ввод активирован. Слушаю...")
    return listen  # Возвращаем функцию для голосового ввода

def execute_command(command):
    """Обработка команд."""
    if command.startswith("открой") or command.startswith("запусти") or command.startswith("включи") or command.startswith("выключи"):
        perform_action(command)
        return

    if "переключись на" in command:
        window_name = command.replace("переключись на", "").strip()
        switch_to_application(window_name)
        return

    update_output(f"Команда '{command}' не распознана.")

# Основная программа
def main_loop():
    update_output("Привет! Я ваш ассистент. Чем могу помочь?")
    command_input_method = get_command_input()

    while True:
        command = command_input_method()
        if command in ["стоп", "выход", "до связи"]:
            update_output("Работа ассистента завершена.")
            root.destroy() 
            break
        execute_command(command)

# Запускаем основной цикл в отдельном потоке, чтобы окно оставалось отзывчивым
import threading
threading.Thread(target=main_loop, daemon=True).start()

root.mainloop()
