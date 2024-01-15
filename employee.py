import tkinter as tk
from tkinter import messagebox
import mysql.connector
import random

# Создание подключения к MySQL
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="base"
)

# Создание курсора для работы с базой данных
db_cursor = db_connection.cursor()

# Создание таблицы, если она не существует
db_cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INT AUTO_INCREMENT PRIMARY KEY,
        task_name VARCHAR(255) NOT NULL,
        employee_name VARCHAR(255) NOT NULL
    )
""")
db_connection.commit()

# Функция для добавления задачи
def add_task():
    task_name = task_entry.get()
    employee_name = employee_entry.get()

    if not task_name or not employee_name:
        messagebox.showerror("Ошибка", "Заполните все поля")
        return

    # Добавление задачи в базу данных
    db_cursor.execute("INSERT INTO tasks (task_name, employee_name) VALUES (%s, %s)", (task_name, employee_name))
    db_connection.commit()

    messagebox.showinfo("Успех", "Задача добавлена успешно")

# Функция для генерации случайного распределения задач
def generate_tasks():
    # Получение списка всех сотрудников
    db_cursor.execute("SELECT DISTINCT employee_name FROM tasks")
    employees = db_cursor.fetchall()

    # Получение списка задач
    db_cursor.execute("SELECT task_name FROM tasks")
    tasks = db_cursor.fetchall()

    if not employees or not tasks:
        messagebox.showerror("Ошибка", "Добавьте сотрудников и задачи перед генерацией")
        return

    # Распределение задач случайным образом
    for task in tasks:
        random_employee = random.choice(employees)
        db_cursor.execute("UPDATE tasks SET employee_name = %s WHERE task_name = %s",
                          (random_employee[0], task[0]))

    db_connection.commit()
    messagebox.showinfo("Успех", "Задачи распределены успешно")

# Функция для отображения списка задач
def show_tasks():
    # Получение списка задач
    db_cursor.execute("SELECT task_name, employee_name FROM tasks")
    tasks = db_cursor.fetchall()

    if not tasks:
        messagebox.showinfo("Информация", "Список задач пуст")
        return

    # Отображение списка задач в новом окне
    tasks_window = tk.Toplevel(root)
    tasks_window.title("Список задач")

    for i, (task_name, employee_name) in enumerate(tasks, start=1):
        label = tk.Label(tasks_window, text=f"{i}. Задача: {task_name}, Сотрудник: {employee_name}",
                         font=("Calibri", 14), padx=10, pady=5, bg="white", fg="black")
        label.pack()

# Создание главного окна
root = tk.Tk()
root.title("Сервис автоматического распределения задач")

# Настройка шрифтов и цветов
font_description = ("Calibri", 20)
font_normal = ("Calibri", 14)

bg_color = "white"
fg_color = "black"

# Создание и размещение элементов интерфейса
task_label = tk.Label(root, text="Название задачи:", font=font_normal, bg=bg_color, fg=fg_color)
task_label.grid(row=0, column=0, pady=10, padx=10)

task_entry = tk.Entry(root, font=font_normal)
task_entry.grid(row=0, column=1, pady=10, padx=10)

employee_label = tk.Label(root, text="Имя сотрудника:", font=font_normal, bg=bg_color, fg=fg_color)
employee_label.grid(row=1, column=0, pady=10, padx=10)

employee_entry = tk.Entry(root, font=font_normal)
employee_entry.grid(row=1, column=1, pady=10, padx=10)

add_task_button = tk.Button(root, text="Добавить задачу", command=add_task, font=font_normal, bg="blue", fg="white")
add_task_button.grid(row=2, column=0, columnspan=2, pady=10)

generate_button = tk.Button(root, text="Генератор распределения задач", command=generate_tasks, font=font_normal, bg="orange", fg="white")
generate_button.grid(row=3, column=0, columnspan=2, pady=10)

show_tasks_button = tk.Button(root, text="Показать список задач из БД", command=show_tasks, font=font_normal, bg="purple", fg="white")
show_tasks_button.grid(row=4, column=0, columnspan=2, pady=10)

# Запуск основного цикла
root.mainloop()
