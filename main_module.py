import tkinter as tk
from tkinter import messagebox
from ui import MainWindow


def main():
    # Спросить пользователя, использовать ли CSV файлы
    use_csv = messagebox.askyesno("Режим работы",
                                  "Использовать CSV файлы для тестирования?\n\n"
                                  "ДА - использовать тестовые CSV файлы\n"
                                  "НЕТ - использовать базу данных")

    app = MainWindow(use_csv=use_csv)
    app.run()


if __name__ == "__main__":
    main()