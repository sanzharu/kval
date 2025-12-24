import tkinter as tk
from tkinter import messagebox as mb
import mysql.connector as mc

try:
    db = mc.connect(host='localhost', user='root', password='7208', database='newspaper')
    cur = db.cursor(dictionary=True)
except:
    print("ошибка подключения")

def load(tree):
    for i in tree.get_children():
        tree.delete(i)
    try:
        cur.execute(
            "select a.id, a.title, au.full_name from articles a join authors au on a.author_id=au.id where a.status='pending'")
        for r in cur.fetchall():
            tree.insert('', 'end', values=(r['id'], r['title'], r['full_name']))
    except:
        pass


def check():
    """Отпечатать список статей на рассмотрении на указанную дату"""
    # Создаем диалог для ввода даты
    dialog = tk.Toplevel()
    dialog.title("Статьи на рассмотрении")
    dialog.geometry("300x150")

    tk.Label(dialog, text="Введите дату (ГГГГ-ММ-ДД):").pack(pady=10)
    date_entry = tk.Entry(dialog, width=15)
    date_entry.pack(pady=5)

    def print_articles():
        date = date_entry.get()
        if not date:
            mb.showerror("Ошибка", "Введите дату")
            return

        try:
            cur.execute("""
                SELECT a.id, a.title, au.full_name, a.created_date, a.line_count 
                FROM articles a 
                JOIN authors au ON a.author_id = au.id 
                WHERE a.status = 'pending' AND DATE(a.created_date) = %s
                ORDER BY a.created_date
            """, (date,))
            articles = cur.fetchall()

            if not articles:
                mb.showinfo("Результат", f"На {date} статей на рассмотрении нет")
                return

            result = f"Статьи на рассмотрении на {date}:\n\n"
            for art in articles:
                result += f"ID: {art['id']}\n"
                result += f"Название: {art['title']}\n"
                result += f"Автор: {art['full_name']}\n"
                result += f"Дата: {art['created_date']}\n"
                result += f"Строк: {art['line_count']}\n"
                result += "-" * 30 + "\n"

            mb.showinfo("Список статей", result)
        except Exception as e:
            mb.showerror("Ошибка", f"Ошибка: {e}")

    tk.Button(dialog, text="Отпечатать", command=print_articles).pack(pady=10)


def payments():
    """Отпечатать таблицу выплат авторам за период"""
    dialog = tk.Toplevel()
    dialog.title("Выплаты авторам")
    dialog.geometry("350x200")

    tk.Label(dialog, text="Начальная дата (ГГГГ-ММ-ДД):").pack(pady=5)
    date1_entry = tk.Entry(dialog, width=15)
    date1_entry.pack()

    tk.Label(dialog, text="Конечная дата (ГГГГ-ММ-ДД):").pack(pady=5)
    date2_entry = tk.Entry(dialog, width=15)
    date2_entry.pack()

    def print_payments():
        d1 = date1_entry.get()
        d2 = date2_entry.get()
        if not d1 or not d2:
            mb.showerror("Ошибка", "Введите обе даты")
            return

        try:
            cur.execute("""
                SELECT au.full_name, SUM(p.amount) as total, 
                       COUNT(p.article_id) as count, MIN(p.payment_date) as first_date
                FROM payments p 
                JOIN authors au ON p.author_id = au.id 
                WHERE p.payment_date BETWEEN %s AND %s
                GROUP BY au.full_name
                ORDER BY total DESC
            """, (d1, d2))
            payments_data = cur.fetchall()

            if not payments_data:
                mb.showinfo("Результат", f"За период {d1}-{d2} выплат нет")
                return

            result = f"Выплаты за период {d1} - {d2}:\n\n"
            total_all = 0
            for pay in payments_data:
                result += f"Автор: {pay['full_name']}\n"
                result += f"Сумма: {pay['total']} руб.\n"
                result += f"Статей: {pay['count']}\n"
                result += f"Первая выплата: {pay['first_date']}\n"
                result += "-" * 30 + "\n"
                total_all += float(pay['total'])

            result += f"\nВСЕГО ВЫПЛАЧЕНО: {total_all} руб."

            mb.showinfo("Таблица выплат", result)

            try:
                filename = f"выплаты_{d1}_по_{d2}.txt"

                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(result)

                mb.showinfo("Файл создан",
                            f"Отчет сохранен в файл:\n{filename}\n\n"
                            f"Файл находится в папке с программой.")

            except Exception as file_error:
                mb.showwarning("Ошибка файла",
                               f"Не удалось сохранить в файл:\n{file_error}")
        except Exception as e:
            mb.showerror("Ошибка", f"Ошибка: {e}")

    tk.Button(dialog, text="Отпечатать отчет", command=print_payments).pack(pady=10)