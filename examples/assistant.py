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

def find_folders(folder_name, start_path):
    """Ищет все папки с указанным именем, игнорируя регистр."""
    print(f"DEBUG: Ищу папки '{folder_name}' в '{start_path}'")
    folder_name = folder_name.lower()
    matching_folders = []
    for root, dirs, _ in os.walk(start_path):
        for directory in dirs:
            if folder_name == directory.lower():
                matching_folders.append(os.path.join(root, directory))
    return matching_folders

def find_files(file_name, start_path):
    """Ищет все файлы с указанным именем, игнорируя регистр и расширение."""
    print(f"DEBUG: Ищу файлы '{file_name}' в '{start_path}'")
    file_name = file_name.lower()
    matching_files = []
    for root, _, files in os.walk(start_path):
        for file in files:
            file_name_no_ext, _ = os.path.splitext(file)  # убираем расширение
            if file_name == file_name_no_ext.lower():
                matching_files.append(os.path.join(root, file))
    return matching_files

def translate_folder_name(folder_name):
    """Преобразует русское название папки в английский путь."""
    translations = {
        "рабочий стол": os.path.join(os.path.expanduser("~"), "Desktop"),
        "загрузки": os.path.join(os.path.expanduser("~"), "Downloads"),
        "документы": os.path.join(os.path.expanduser("~"), "Documents"),
        "изображения": os.path.join(os.path.expanduser("~"), "Pictures"),
        "музыка": os.path.join(os.path.expanduser("~"), "Music"),
        "видео": os.path.join(os.path.expanduser("~"), "Videos"),
    }
    return translations.get(folder_name)

def open_folder_or_file(path):
    """Открывает указанную папку или файл (только для Windows)."""
    print(f"DEBUG: Пытаюсь открыть: {path}")
    if os.path.exists(path):
        try:
            os.startfile(path)
            print(f"DEBUG: Объект {os.path.basename(path)} успешно открыт.")
        except Exception as e:
            print(f"DEBUG: Ошибка при открытии {os.path.basename(path)}: {e}")
    else:
        print(f"DEBUG: Объект '{path}' не существует.")

def prompt_user_choice(options):
    """Запрашивает у пользователя выбор объекта из нескольких вариантов."""
    print("Найдено несколько объектов. Выберите, что хотите открыть:")
    for idx, option in enumerate(options, start=1):
        print(f"{idx}. {option}")
    while True:
        choice = input("Введите номер объекта для открытия: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return options[int(choice) - 1]
        else:
            print("Некорректный выбор. Попробуйте снова.")

def execute_command(command, start_path):
    """Обработка команды для открытия папок или файлов."""
    if "открой папку" in command:
        # Если команда связана с папкой
        folder_name = command.replace("открой папку", "").strip()
        translated_path = translate_folder_name(folder_name)
        if translated_path:
            print(f"DEBUG: Открыта папка: {translated_path}.")
            open_folder_or_file(translated_path)
        else:
            matching_folders = find_folders(folder_name, start_path)
            if matching_folders:
                if len(matching_folders) == 1:
                    # Если найдена одна папка, открыть её
                    open_folder_or_file(matching_folders[0])
                else:
                    # Если найдено несколько папок, предложить выбор
                    selected_folder = prompt_user_choice(matching_folders)
                    open_folder_or_file(selected_folder)
            else:
                print(f"DEBUG: Папка '{folder_name}' не найдена.")
    elif "открой" in command:
        # Если команда связана с файлом
        item_name = command.replace("открой", "").strip()
        matching_folders = find_folders(item_name, start_path)
        matching_files = find_files(item_name, start_path)
        
        all_matches = matching_folders + matching_files
        
        if all_matches:
            if len(all_matches) == 1:
                # Если найден один объект (папка или файл), открыть его
                open_folder_or_file(all_matches[0])
            else:
                # Если найдено несколько объектов, предложить выбор
                selected_item = prompt_user_choice(all_matches)
                open_folder_or_file(selected_item)
        else:
            print(f"DEBUG: Объект '{item_name}' не найден.")
    else:
        print("DEBUG: Команда не распознана.")

# Основной код
if __name__ == "__main__":
    if os.name != 'nt':
        print("Этот скрипт работает только на Windows.")
        exit()
    
    # Новый стартовый путь
    start_path = "C:\\"  # Замените на свой путь

    print("Привет! Я ваш ассистент. Чем могу помочь?")
    command_input_method = get_command_input()
    
    while True:
        first_command = command_input_method()
        execute_command(first_command, start_path)
