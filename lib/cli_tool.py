import argparse
import json
import os
from models import Task, User

DATA_FILE = "tasks_data.json"

def load_users():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    users = {}
    for username, user_data in data.items():
        user = User(username)
        for task_info in user_data.get("tasks", []):
            task = Task(task_info["title"])
            task.completed = task_info["completed"]
            user.tasks.append(task)
        users[username] = user
    return users

def save_users(users):
    data = {}
    for username, user in users.items():
        data[username] = {
            "tasks": [{"title": t.title, "completed": t.completed} for t in user.tasks]
        }
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

users = load_users()

def add_task(args):
    user = users.get(args.user)
    if not user:
        user = User(args.user)
        users[args.user] = user
    task = Task(args.title)
    user.add_task(task)
    save_users(users)

def complete_task(args):
    user = users.get(args.user)
    if not user:
        print(f"❌ User '{args.user}' not found.")
        return
    for task in user.tasks:
        if task.title == args.title:
            if task.completed:
                print(f"⚠️ Task '{args.title}' is already completed.")
            else:
                task.complete()
                save_users(users)
            return
    print(f"❌ Task '{args.title}' not found for user '{args.user}'.")

def list_tasks(args):
    user = users.get(args.user)
    if not user:
        print(f"❌ User '{args.user}' not found.")
        return
    if not user.tasks:
        print(f"ℹ️ User '{args.user}' has no tasks.")
        return
    print(f"Tasks for {user.name}:")
    for idx, task in enumerate(user.tasks, 1):
        status = "✔" if task.completed else "✘"
        print(f" {idx}. [{status}] {task.title}")

def main():
    parser = argparse.ArgumentParser(description="Task Manager CLI")
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add-task", help="Add a task for a user")
    add_parser.add_argument("user")
    add_parser.add_argument("title")
    add_parser.set_defaults(func=add_task)

    complete_parser = subparsers.add_parser("complete-task", help="Complete a user's task")
    complete_parser.add_argument("user")
    complete_parser.add_argument("title")
    complete_parser.set_defaults(func=complete_task)

    list_parser = subparsers.add_parser("list-tasks", help="List all tasks for a user")
    list_parser.add_argument("user")
    list_parser.set_defaults(func=list_tasks)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
