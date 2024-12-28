import pyautogui
import time

print("Наведите курсор на нужное место. Нажмите Ctrl+C для выхода.")
try:
    while True:
        # Получение текущих координат курсора
        x, y = pyautogui.position()
        print(f"Координаты курсора: X={x}, Y={y}", end="\r")  # Вывод координат
        time.sleep(0.1)  # Задержка для обновления
except KeyboardInterrupt:
    print("\nПрограмма завершена.")
