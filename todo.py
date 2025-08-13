import json, os, datetime as dt
from dataclasses import dataclass, asdict
from typing import List, Optional
from colorama import Fore, Style, init
init(autoreset=True)

DATA_FILE = "tasks.json"
PRIORITIES = ["low", "med", "high"]

def color_priority(priority: str) -> str:
    if priority == "high":
        return Fore.RED + priority + Style.RESET_ALL
    elif priority == "med":
        return Fore.YELLOW + priority + Style.RESET_ALL
    elif priority == "low":
        return Fore.GREEN + priority + Style.RESET_ALL
    return priority

# --- Sorting helpers / constants ---
PRI_ORDER = {"high": 0, "med": 1, "low": 2}

def sort_tasks(rows: List["Task"]) -> List["Task"]:
    def key(t: "Task"):
        pri = PRI_ORDER.get(t.priority, 99)
        due = dt.date.fromisoformat(t.due) if t.due else dt.date.max
        done = 1 if t.completed else 0   # OPEN first, DONE later
        return (done, pri, due, t.id)
    return sorted(rows, key=key)



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

def parse_date(s: str) -> Optional[str]:
    s = s.strip()
    if not s:
        return None
    try:
        return dt.date.fromisoformat(s).isoformat()
    except ValueError:
        print("⚠️ Invalid date. Use YYYY-MM-DD or leave blank.")
        return None

def add_task(tasks: List[Task]):
    title = input("Task title: ").strip()
    if not title:
        print("⚠️ Title required.")
        return
    pr = (input("Priority [low/med/high] (default med): ").strip().lower() or "med")
    if pr not in PRIORITIES:
        print("⚠️ Invalid priority; defaulting to 'med'.")
        pr = "med"
    while True:
        due_in = input("Due date (YYYY-MM-DD, optional): ")
        due = parse_date(due_in)
        if due_in == "" or due is not None:
            break
    t = Task(id=next_id(tasks), title=title, priority=pr, due=due)
    tasks.append(t)
    save_tasks(tasks)
    print(f"✅ Added #{t.id}: {t.title}")

def list_tasks(tasks: List[Task], status: str = "all", pri: Optional[str] = None):
    # Filter by status
    if status == "open":
        rows = [t for t in tasks if not t.completed]
    elif status == "done":
        rows = [t for t in tasks if t.completed]
    else:
        rows = list(tasks)

    # Optional priority filter
    if pri in {"low", "med", "high"}:
        rows = [t for t in rows if t.priority == pri]

    # Sort: OPEN first → high→med→low → earliest due date → id
    rows = sort_tasks(rows)

    if not rows:
        print("📋 No tasks.")
        return

    # Colored header
    print(Fore.CYAN + Style.BRIGHT + "\nID  Status  Pri  Due        Title" + Style.RESET_ALL)

    for t in rows:
        # Status: bold green for DONE
        status_txt = "DONE" if t.completed else "OPEN"
        if t.completed:
            status_txt = Style.BRIGHT + Fore.GREEN + "DONE" + Style.RESET_ALL

        # Priority color
        if t.priority == "high":
            pri_color = Fore.RED + t.priority[:3]
        elif t.priority == "med":
            pri_color = Fore.YELLOW + t.priority[:3]
        else:
            pri_color = Fore.GREEN + t.priority[:3]

        due = t.due or "—"
        print(f"{t.id:<3} {status_txt:<6} {pri_color:<3} {Style.RESET_ALL}{due:<10} {t.title}")




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

def remove_task(tasks: List[Task]):
    try:
        tid = int(input("Task ID: "))
    except ValueError:
        print("⚠️ Enter a number.")
        return
    before = len(tasks)
    tasks[:] = [t for t in tasks if t.id != tid]
    save_tasks(tasks)
    if len(tasks) < before:
        print(f"🗑️ Removed #{tid}.")
    else:
        print("⚠️ Not found.")

def edit_task(tasks: List[Task]):
    try:
        tid = int(input("Task ID to edit: "))
    except ValueError:
        print("⚠️ Enter a number.")
        return
    t = next((x for x in tasks if x.id == tid), None)
    if not t:
        print("⚠️ Not found.")
        return

    new_title = input(f"New title (blank to keep '{t.title}'): ").strip() or t.title
    pr_in = input(f"New priority [low/med/high] (current {t.priority}): ").strip().lower()
    if pr_in and pr_in not in PRIORITIES:
        print("⚠️ Invalid priority; keeping current.")
        pr_in = t.priority
    new_pr = pr_in or t.priority

    while True:
        due_in = input(f"New due date (YYYY-MM-DD or blank; current {t.due or '—'}): ")
        if due_in == "":
            new_due = t.due
            break
        parsed = parse_date(due_in)
        if parsed is not None:
            new_due = parsed
            break

    t.title, t.priority, t.due = new_title, new_pr, new_due
    save_tasks(tasks)
    print(f"✏️ Updated #{t.id}.")

def list_menu(tasks: List[Task]):
    print("\nFilter by status: [A]ll, [O]pen, [D]one")
    s = input("Choose status (A/O/D, default A): ").strip().lower()
    status = {"o": "open", "d": "done", "a": "all", "": "all"}.get(s, "all")

    p = input("Priority filter (low/med/high or blank): ").strip().lower()
    pri = p if p in {"low", "med", "high"} else None

    list_tasks(tasks, status=status, pri=pri)



def menu():
    tasks = load_tasks()
    actions = {
        "1": ("Add task", lambda: add_task(tasks)),
        "2": ("List tasks", lambda: list_menu(tasks)),
        "3": ("Mark complete", lambda: mark_done(tasks)),
        "4": ("Remove task", lambda: remove_task(tasks)),
        "5": ("Edit task", lambda: edit_task(tasks)),
        "0": ("Exit", None),
    }
    while True:
        print("\n=== To-Do List ===")
        for k,(label,_) in actions.items():
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
