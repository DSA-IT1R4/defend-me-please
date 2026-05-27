import tkinter as tk
from tkinter import messagebox
from datetime import datetime

tasks = []
undo_stack = []

# ---------- COLORS ----------
BG = "#020F43"          # dark navy background
FG = "#e2e8f0"          # light text
ACCENT = "#38bdf8"      # blue accent
DANGER = "#ef4444"      # red
SUCCESS = "#22c55e"     # green
CARD = "#1e293b"        # container bg

# ---------- FUNCTIONS ----------

def add_task():
    title = title_entry.get().strip()
    subject = subject_entry.get().strip()
    due = due_entry.get().strip()
    priority = priority_var.get()
    task_type = type_var.get()

    if not title:
        messagebox.showwarning("Warning", "Enter a task title")
        return

    task = {
        "id": len(tasks),
        "title": title,
        "subject": subject,
        "due": due,
        "priority": priority,
        "type": task_type,
        "done": False
    }

    tasks.append(task)
    undo_stack.append(("add", task))

    clear_inputs()
    render_tasks()
    update_stats()


def clear_inputs():
    title_entry.delete(0, tk.END)
    subject_entry.delete(0, tk.END)
    due_entry.delete(0, tk.END)


def render_tasks():
    task_list.delete(0, tk.END)

    for task in tasks:
        status = "✔" if task["done"] else "✗"
        text = f"{status} {task['title']} | {task['subject']} | {task['priority']} | {task['due']}"
        task_list.insert(tk.END, text)


def toggle_done():
    if not task_list.curselection():
        return

    i = task_list.curselection()[0]
    task = tasks[i]

    undo_stack.append(("toggle", i, task["done"]))
    task["done"] = not task["done"]

    render_tasks()
    update_stats()


def delete_task():
    if not task_list.curselection():
        return

    i = task_list.curselection()[0]
    task = tasks[i]

    undo_stack.append(("delete", task))
    tasks.pop(i)

    render_tasks()
    update_stats()


def clear_done():
    global tasks
    tasks = [t for t in tasks if not t["done"]]

    render_tasks()
    update_stats()


def undo():
    if not undo_stack:
        return

    action = undo_stack.pop()

    if action[0] == "add":
        tasks.remove(action[1])

    elif action[0] == "delete":
        tasks.append(action[1])

    elif action[0] == "toggle":
        i, prev = action[1], action[2]
        if i < len(tasks):
            tasks[i]["done"] = prev

    render_tasks()
    update_stats()


def update_stats():
    total = len(tasks)
    done = sum(t["done"] for t in tasks)
    pending = total - done

    today = datetime.now()

    overdue = 0
    for t in tasks:
        if t["due"] and not t["done"]:
            try:
                if datetime.strptime(t["due"], "%Y-%m-%d") < today:
                    overdue += 1
            except:
                pass

    total_lbl.config(text=f"Total: {total}")
    pending_lbl.config(text=f"Pending: {pending}")
    done_lbl.config(text=f"Done: {done}")
    overdue_lbl.config(text=f"Overdue: {overdue}")
    
def add_placeholder(entry, placeholder):
    entry.insert(0, placeholder)
    entry.config(fg="gray")

    def on_focus_in(event):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg="white")

    def on_focus_out(event):
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.config(fg="gray")

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

# ---------- GUI ----------
root = tk.Tk()
root.title("Student Task Manager")
root.geometry("700x600")
root.configure(bg=BG)

tk.Label(root, text="Student Task Manager", font=("Sans Serif", 25, "bold"), bg=BG, fg=ACCENT).pack(pady=10)

# Stats
frame_stats = tk.Frame(root, bg=BG)
frame_stats.pack()

total_lbl = tk.Label(frame_stats, text="Total: 0", width=15, bg=BG, fg=FG, font=("Sans Serif", 10, "bold"))
pending_lbl = tk.Label(frame_stats, text="Pending: 0", width=15, bg=BG, fg=FG, font=("Sans Serif", 10, "bold"))
done_lbl = tk.Label(frame_stats, text="Done: 0", width=15, bg=BG, fg=SUCCESS, font=("Sans Serif", 10, "bold"))
overdue_lbl = tk.Label(frame_stats, text="Overdue: 0", width=15, bg=BG, fg=DANGER, font=("Sans Serif", 10, "bold"))

total_lbl.grid(row=0, column=0)
pending_lbl.grid(row=0, column=1)
done_lbl.grid(row=0, column=2)
overdue_lbl.grid(row=0, column=3)

# Inputs
# Inputs
frame_input = tk.Frame(root, bg=CARD)
frame_input.pack(pady=10)

title_entry = tk.Entry(frame_input, width=20, font=("Sans Serif", 11), bg="#0b1220", fg=FG, insertbackground=FG)
subject_entry = tk.Entry(frame_input, width=20, font=("Sans Serif", 11), bg="#0b1220", fg=FG, insertbackground=FG)

due_entry = DateEntry(frame_input, width=15, font=("Sans Serif", 11), background=ACCENT, foreground="black", borderwidth=2, date_pattern="yyyy-mm-dd")

add_placeholder(title_entry, "Task Title")
add_placeholder(subject_entry, "Subject")

title_entry.grid(row=0, column=0, padx=6, pady=5)
subject_entry.grid(row=0, column=1, padx=6, pady=5)
due_entry.grid(row=0, column=2, padx=6, pady=5)

priority_var = tk.StringVar(value="High")
type_var = tk.StringVar(value="Assignment")

tk.OptionMenu(frame_input, priority_var, "High", "Medium", "Low").grid(row=1, column=0)
tk.OptionMenu(frame_input, type_var, "Assignment", "Exam", "Project", "Reading", "Lab").grid(row=1, column=1)

tk.Button(frame_input, text="Add Task", command=add_task, bg=ACCENT, fg="black", activebackground="#0ea5e9").grid(row=1, column=2)

# Task list
task_list = tk.Listbox( root, width=90, height=15, bg="#0b1220", fg=FG, selectbackground=ACCENT, selectforeground="black")
task_list.pack(pady=10)

# Buttons
frame_btn = tk.Frame(root, bg=BG)
frame_btn.pack()

tk.Button(frame_btn, text="Done/Undo", command=toggle_done, bg=SUCCESS, fg="black").grid(row=0, column=0, padx=5)
tk.Button(frame_btn, text="Delete", command=delete_task, bg=DANGER, fg="white").grid(row=0, column=1, padx=5)
tk.Button(frame_btn, text="Undo Action", command=undo, bg=ACCENT, fg="black").grid(row=0, column=2, padx=5)
tk.Button(frame_btn, text="Clear Done", command=clear_done, bg="#f59e0b", fg="black").grid(row=0, column=3, padx=5)

render_tasks()
update_stats()

root.mainloop()