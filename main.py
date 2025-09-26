import tkinter as tk
from tkinter import ttk
from db import engine, metadata, insert, select, delete, update
from tables import tasks

metadata.create_all(engine)

def get_tasks(table):

    for frame in (tasks_in_progress, tasks_done, tasks_to_do):
        for element in frame.winfo_children():
            element.destroy()

    with engine.begin() as conn:
        tasks_list = conn.execute(select(table))

    for task in tasks_list:
        parent_frame = tasks_to_do if task.statut == "To do" else tasks_in_progress if task.statut == "En cours" else tasks_done
        task_frame = tk.Frame(parent_frame, width=300, relief="solid", borderwidth=1)
        task_frame.pack(pady=5, padx=10, fill="x")

        my_data = tk.StringVar(
            value=f"{task.id} | {task.description} | {task.priorite} | {task.statut}"
        )
        data_label = tk.Label(task_frame, textvariable=my_data)
        data_label.pack(side="left", padx=10)

        delete_button = tk.Button(
            task_frame, text="X", command=lambda id=task.id: delete_task(id),
            bg="#F40C0C", fg="white", activebackground="#ab1f09",
            font=("Arial", 11, "bold"), relief="flat", cursor="hand2"
        )
        delete_button.pack(side="right", padx=5)

        edit_button = tk.Button(
            task_frame, text="Edit", command=lambda t=task: edit_task_popup(t),
            bg="#FFA500", fg="white", activebackground="#cc8400",
            font=("Arial", 11, "bold"), relief="flat", cursor="hand2"
        )
        edit_button.pack(side="right", padx=5)

        if task.statut != "Done":
            check_button = tk.Button(
                task_frame, text="En cours" if task.statut == "To do" else "Done",
                command=lambda id=task.id: check_task(id),
                bg="#004AF8", fg="white", activebackground="#0521b0",
                font=("Arial", 11, "bold"), relief="flat", cursor="hand2"
            )
            check_button.pack(side="right", padx=5)

def add_task():
    priorite = selected_option.get()
    description = description_input.get("1.0", tk.END).strip()
    if description:
        with engine.begin() as conn:
            conn.execute(insert(tasks), [{"priorite": priorite, "description": description}])
        description_input.delete("1.0", tk.END)
        get_tasks(tasks)

def delete_task(id):
    with engine.begin() as conn:
        conn.execute(delete(tasks).where(tasks.c.id == id))
    get_tasks(tasks)

def check_task(id):
    with engine.begin() as conn:
        task = conn.execute(select(tasks).where(tasks.c.id == id)).fetchone()
        if task.statut == "To do":
            conn.execute(update(tasks).where(tasks.c.id == id).values(statut="En cours"))
        else:
            conn.execute(update(tasks).where(tasks.c.id == id).values(statut="Done"))
    get_tasks(tasks)

def edit_task_popup(task):
    popup = tk.Toplevel(root)
    popup.title("Edit Task")
    popup.geometry("400x250")

    tk.Label(popup, text="Description:", font=("Arial", 10)).pack(pady=5)
    desc_input = tk.Text(popup, width=40, height=5)
    desc_input.insert(tk.END, task.description)
    desc_input.pack(pady=5)

    tk.Label(popup, text="Priorite:", font=("Arial", 10)).pack(pady=5)
    priority_var = tk.StringVar(popup)
    priority_var.set(task.priorite)
    tk.OptionMenu(popup, priority_var, "Low", "Medium", "High").pack(pady=5)

    def save_changes():
        new_desc = desc_input.get("1.0", tk.END).strip()
        new_priorite = priority_var.get()
        if new_desc:
            with engine.begin() as conn:
                conn.execute(update(tasks).where(tasks.c.id == task.id).values(description=new_desc, priorite=new_priorite))
            popup.destroy()
            get_tasks(tasks)

    tk.Button(popup, text="Save", command=save_changes,
              bg="#4CAF50", fg="white", font=("Arial", 11, "bold"),
              relief="flat", cursor="hand2").pack(pady=10)


root = tk.Tk()
root.title("My App")
root.geometry("1200x660")

label = tk.Label(root, text="To Do List!", font=("Arial", 24, "bold"))
label.pack(pady=10)

data_frame = tk.Frame(root, relief="solid", bd=1)
data_frame.pack(pady=5, padx=20, fill="x")

description_frame = tk.Frame(data_frame)
description_frame.pack(pady=5)

select_frame = tk.Frame(data_frame)
select_frame.pack(pady=5)

tasks_frame = tk.Frame(root)
tasks_frame.pack(fill="both", expand=True, pady=10)

tasks_to_do = tk.LabelFrame(tasks_frame, text="To do", padx=10, pady=10)
tasks_to_do.pack(side="left", fill="both", expand=True, padx=10)

tasks_in_progress = tk.LabelFrame(tasks_frame, text="En cours", padx=10, pady=10)
tasks_in_progress.pack(side="left", fill="both", expand=True, padx=10)

tasks_done = tk.LabelFrame(tasks_frame, text="Done", padx=10, pady=10)
tasks_done.pack(side="right", fill="both", expand=True, padx=10)

select_label = tk.Label(select_frame, text="Priorite : ", font=("Arial", 10))
select_label.pack(side="left", padx=50)

selected_option = tk.StringVar(root)
selected_option.set("Medium")
options = ["Low", "Medium", "High"]
tk.OptionMenu(select_frame, selected_option, *options).pack(pady=10)

description_label = tk.Label(description_frame, text="Description : ", font=("Arial", 10))
description_label.pack(side="left", padx=10)

description_input = tk.Text(description_frame, width=50, height=5)
description_input.pack(side="left", padx=10)

button = tk.Button(data_frame, text="Add Task", command=add_task,
                   bg="#4CAF50", fg="white", activebackground="#45a049",
                   font=("Arial", 11, "bold"), relief="flat",
                   padx=15, pady=5, cursor="hand2")
button.pack(side="right", padx=15, pady=15)

get_tasks(tasks)
root.mainloop()
