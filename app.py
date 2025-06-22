from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

TASKS_FILE = 'tasks.json'

def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []  # return empty list if file is empty or invalid
    return []


def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)

@app.route("/", methods=["GET", "POST"])
def index():
    tasks = load_tasks()
    if request.method == "POST":
        task = request.form.get("task")
        if task:
            tasks.append({"task": task})
            save_tasks(tasks)
        return redirect("/")
    return render_template("index.html", tasks=tasks)

@app.route("/delete/<int:index>")
def delete(index):
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        tasks.pop(index)
        save_tasks(tasks)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
