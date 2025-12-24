import tkinter as tk
from tkinter import ttk, messagebox as mb
from datetime import datetime as dt
import mysql.connector as mc

try:
    db = mc.connect(host='localhost', user='root', password='7208', database='mfc')
    cur = db.cursor(dictionary=True)
except:
    print("ошибка подключения к бд")
    db = None
    cur = None

def load(tree):
    for i in tree.get_children():
        tree.delete(i)
    try:
        cur.execute("""
            SELECT sc.id, a.full_name, sc.temp_card_issued, sc.temp_card_expires
            FROM social_cards sc
            JOIN applicants a ON sc.applicant_id = a.id
            ORDER BY sc.temp_card_expires
        """)

        for row in cur.fetchall():
            tree.insert('', 'end', values=(
                row['id'],
                row['full_name'],
                row['temp_card_issued'],
                row['temp_card_expires']
            ))
    except:
        pass

def popular_docs():
    """список типов документов в порядке убывания количества поданных заявок"""
    if not cur:
        mb.showerror("ошибка", "нет подключения к бд")
        return

    dialog = tk.Toplevel()
    dialog.title("популярные документы")
    dialog.geometry("400x200")

    tk.Label(dialog, text="начальная дата (гггг-мм-дд):").pack(pady=5)
    d1_entry = tk.Entry(dialog, width=15)
    d1_entry.insert(0, "2024-12-01")
    d1_entry.pack()

    tk.Label(dialog, text="конечная дата (гггг-мм-дд):").pack(pady=5)
    d2_entry = tk.Entry(dialog, width=15)
    d2_entry.insert(0, dt.now().strftime("%Y-%m-%d"))
    d2_entry.pack()

    def show():
        d1 = d1_entry.get()
        d2 = d2_entry.get()

        try:
            cur.execute("""
                select dt.name, count(a.id) as cnt
                from applications a
                join doc_types dt on a.doc_type_id = dt.id
                where a.application_date between %s and %s
                group by dt.name
                order by cnt desc
            """, (d1, d2))

            res = "популярные документы:\n\n"
            for r in cur.fetchall():
                res += f"{r['name']}: {r['cnt']} заявок\n"

            mb.showinfo("результат", res)

        except Exception as e:
            mb.showerror("ошибка", f"ошибка: {e}")

    tk.Button(dialog, text="показать", command=show).pack(pady=15)


def card_date():
    """определить, когда заявитель может получить социальную карту"""
    if not cur:
        mb.showerror("ошибка", "нет подключения к бд")
        return

    dialog = tk.Toplevel()
    dialog.title("дата получения карты")
    dialog.geometry("400x200")

    tk.Label(dialog, text="фио заявителя:").pack(pady=5)
    name_entry = tk.Entry(dialog, width=30)
    name_entry.pack()

    def check():
        name = name_entry.get()

        try:
            cur.execute("""
                select sc.temp_card_expires, a.full_name, sc.temp_card_issued
                from social_cards sc
                join applicants a on sc.applicant_id = a.id
                where a.full_name like %s
            """, (f"%{name}%",))

            row = cur.fetchone()

            if row:
                res = f"заявитель: {row['full_name']}\n"
                res += f"временная карта выдана: {row['temp_card_issued']}\n"
                res += f"действует до: {row['temp_card_expires']}\n"
                res += f"постоянную карту можно получить после: {row['temp_card_expires']}"
            else:
                res = "заявитель не найден"

            mb.showinfo("информация о карте", res)

        except Exception as e:
            mb.showerror("ошибка", f"ошибка: {e}")

    tk.Button(dialog, text="проверить", command=check).pack(pady=15)