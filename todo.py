import json, os, datetime as dt
from dataclasses import dataclass, asdict
from typing import List, Optional

DATA_FILE = "tasks.json"
PRIORITIES = ["low", "med", "high"]

@dataclass
class Task:
    id: int
    title: str
    priority: str = "med"
    due: Optional[str] = None
    completed: bool = False
    created: str = dt.datetime.now().isoformat(timespec="seconds")

def load_tasks() -> List[Task]:
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        raw = json.load(f)
    return [Task(**t) for t in raw]

def save_tasks(tasks: List[Task]) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([asdict(t) for t in tasks], f, indent=2)

def next_id(tasks: List[Task]) -> int:
    return (max((t.id for t in tasks), default=0) + 1)

def prompt_due_date(current: Optional[str] = None) -> Optional[str]:
    while True:
        if current is not None:
            due_str = input(
                f"Due date (YYYY-MM-DD, blank keeps '{current}', 'none' clears): "
            ).strip()
            if not due_str:
                return current
            if due_str.lower() == "none":
                return None
        else:
            due_str = input("Due date (YYYY-MM-DD, optional): ").strip()
            if not due_str:
                return None
        try:
            dt.datetime.strptime(due_str, "%Y-%m-%d")
            return due_str
        except ValueError:
            print("⚠️ Invalid date; use YYYY-MM-DD.")

def add_task(tasks: List[Task]):
    title = input("Task title: ").strip()
    if not title:
        print("⚠️ Title required.")
        return
    pr = input("Priority [low/med/high] (default med): ").strip().lower() or "med"
    if pr not in PRIORITIES:
        print("⚠️ Invalid priority; defaulting to 'med'.")
        pr = "med"
    due = prompt_due_date()
    t = Task(id=next_id(tasks), title=title, priority=pr, due=due)
    tasks.append(t)
    save_tasks(tasks)
    print(f"✅ Added #{t.id}: {t.title}")

def list_tasks(tasks: List[Task]):
    if not tasks:
        print("📭 No tasks.")
        return
    print("\nID  Status  Pri  Due        Title")
    for t in tasks:
        status = "DONE" if t.completed else "OPEN"
        due = t.due or "—"
        print(f"{t.id:<3} {status:<6}  {t.priority[:3]:<3}  {due:<10} {t.title}")

def mark_done(tasks: List[Task]):
    try:
        tid = int(input("Task ID: "))
    except ValueError:
        print("⚠️ Enter a number.")
        return
    for t in tasks:
        if t.id == tid:
            t.completed = True
            save_tasks(tasks)
            print(f"✅ Marked #{tid} complete.")
            return
    print("⚠️ Not found.")

def edit_task(tasks: List[Task]):
    try:
        tid = int(input("Task ID: "))
    except ValueError:
        print("⚠️ Enter a number.")
        return
    for t in tasks:
        if t.id == tid:
            title = input(f"Title [{t.title}]: ").strip() or t.title
            pr = input(f"Priority [low/med/high] [{t.priority}]: ").strip().lower()
            if pr:
                if pr in PRIORITIES:
                    t.priority = pr
                else:
                    print("⚠️ Invalid priority; keeping current.")
            t.due = prompt_due_date(t.due)
            t.title = title
            save_tasks(tasks)
            print(f"✏️ Edited #{tid}.")
            return
    print("⚠️ Not found.")

def remove_task(tasks: List[Task]):
    try:
        tid = int(input("Task ID: "))
    except ValueError:
        print("⚠️ Enter a number.")
        return
    tasks[:] = [t for t in tasks if t.id != tid]
    save_tasks(tasks)
    print(f"🗑️ Removed #{tid}.")

def menu():
    tasks = load_tasks()
    actions = {
        "1": ("Add task", lambda: add_task(tasks)),
        "2": ("List tasks", lambda: list_tasks(tasks)),
        "3": ("Mark complete", lambda: mark_done(tasks)),
        "4": ("Edit task", lambda: edit_task(tasks)),
        "5": ("Remove task", lambda: remove_task(tasks)),
        "0": ("Exit", None),
    }
    while True:
        print("\n=== To-Do List ===")
        for k, (label, _) in actions.items():
            print(f"{k}. {label}")
        choice = input("Choose: ").strip()
        if choice == "0":
            break
        if choice in actions:
            actions[choice][1]()
        else:
            print("⚠️ Invalid choice.")

if __name__ == "__main__":
    menu()
